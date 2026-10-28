"""On-device scrubber: finds personal details in any prompt and swaps them before it leaves the device.

Detection is detect.Detector: a multilingual PII model, worldwide ID patterns and a city gazetteer, all local.
Three kinds of swap:
- reversible: people, emails, phones, organisations and your "always hide" terms become consistent stand-ins;
  the vault on your device maps them back when the answer arrives.
- generalised: a city becomes its state ("surat gujarat" -> "Gujarat"), an exact adult age becomes a decade
  ("60" -> "60-something"), an occupation becomes its category ("martial art tutor" -> "teacher"),
  well-known employers become their kind. The answer stays useful and nothing needs reversing.
- removed: ID numbers, card numbers, street addresses, postcodes and birth dates.
Stand-ins are keyed per chat, so the same person gets a different stand-in in the next chat.
You stay in control: "keep" un-hides anything the detector flagged, "hide" adds anything it missed.
"""
import copy
import hashlib
import hmac
import re
import secrets
import threading
import time

from detect import Detector

SUB = {
    "m": "Rowan Felix Jonah Theo Ezra Silas Miles Jasper Callum Declan Emmett Rhys Tobias Arlo Bennett".split(),
    "f": "Hazel Iris Clara Tessa Elise Maeve Ruby Wren Margo Sienna Delia Imogen Freya Esme Juno".split(),
    "n": "Quinn Reese Sage Emerson Finley Parker Rory Blair Sloane Marlowe Ellis Jordan Avery Kai".split(),
}
SURNAMES = "Hayes Ellison Brooks Calloway Whitaker Merritt Langley Sutton Ashford Pryor Holloway Kendrick".split()
CODENAMES = "Kestrel Juniper Halcyon Meridian Larkspur Ardent Solace Tamarind Corvid Saltmarsh Bramble Cinder".split()
FEMALE_HINT = r"daughter|wife|mom|mother|mum|sister|girlfriend|aunt|niece|grandmother|grandma|she|her|mrs|ms|miss"
MALE_HINT = r"son|husband|dad|father|brother|boyfriend|uncle|nephew|grandfather|grandpa|he|him|his|mr"
TITLE_RE = re.compile(r"^(mr|mrs|ms|miss|mx|dr|prof)\.?\s+", re.I)

ORGS = {
    "an HMO": ["kaiser permanente", "kaiser"],
    "a health insurer": ["blue cross blue shield", "blue cross", "blue shield", "unitedhealthcare", "united healthcare",
                         "aetna", "cigna", "humana", "anthem", "oscar health", "molina", "star health", "hdfc ergo"],
    "a big tech company": ["google", "alphabet", "meta", "facebook", "apple", "amazon", "microsoft", "netflix", "nvidia",
                           "tesla", "salesforce", "oracle", "ibm", "intel", "uber", "airbnb", "stripe", "openai",
                           "infosys", "tcs", "tata consultancy services", "wipro", "hcl", "flipkart", "accenture",
                           "panasonic", "samsung", "sony", "huawei", "华为", "alibaba", "tencent"],
    "a large retailer or logistics company": ["walmart", "target", "costco", "fedex", "ups", "dhl", "ikea", "bimbo"],
    "an insurer": ["geico", "allstate", "state farm", "progressive", "lic", "axa", "allianz", "prudential"],
    "a crypto exchange": ["binance", "coinbase", "kraken", "wazirx"],
    "a large bank": ["goldman sachs", "jpmorgan", "j.p. morgan", "morgan stanley", "citadel", "blackrock",
                     "bank of america", "wells fargo", "citibank", "citi", "hsbc", "barclays", "sbi", "chase",
                     "state bank of india", "hdfc bank", "icici bank", "axis bank", "itaú", "itau", "bradesco"],
    "a large consulting firm": ["mckinsey", "deloitte", "boston consulting group", "bcg", "bain", "pwc", "kpmg", "ey"],
}
ORG_CATEGORY = {name: cat for cat, names in ORGS.items() for name in names}
OCCUPATIONS = [
    ("teacher", r"teach|tutor|instructor|lecturer|professor|coach|trainer|educator|sensei|guru"),
    ("healthcare worker", r"nurse|doctor|physician|surgeon|dentist|pharmac|therap|paramedic|midwife|caregiver|medic"),
    ("tech worker", r"engineer|developer|programmer|coder|software|data scien|analyst|designer|devops|it "),
    ("legal professional", r"lawyer|attorney|advocate|solicitor|barrister|paralegal|judge|notary"),
    ("finance professional", r"accountant|banker|auditor|actuar|trader|broker|financ|\bca\b|cpa"),
    ("tradesperson", r"electrician|plumber|carpenter|mechanic|welder|mason|painter|technician|builder|contractor"),
    ("business owner", r"owner|founder|entrepreneur|shopkeeper|merchant|business|ceo|proprietor"),
    ("public servant", r"officer|police|clerk|civil serv|government|military|soldier|army|navy|firefighter"),
    ("creative professional", r"artist|writer|author|musician|actor|photographer|journalist|editor|filmmaker"),
    ("service worker", r"driver|cashier|waiter|chef|cook|barista|cleaner|guard|delivery|retail|salesperson"),
    ("student", r"student|undergrad|graduate|phd|intern"),
]
REMOVED = {"address": "[street address]", "postcode": "[postcode]", "dob": "[birth date]", "card": "[card number removed]"}
LABELS = {"person": "person", "org": "organisation", "location": "place", "address": "street address",
          "postcode": "postcode", "age": "age", "occupation": "occupation", "phone": "phone", "email": "email",
          "id": "ID number", "card": "card number", "dob": "birth date", "custom": "always hide"}
REVERSIBLE = {"person", "email", "phone", "org", "custom"}

_detector = None
_ready = threading.Event()


def load_detector():
    """Load the model once, in the background; requests wait for it."""
    global _detector
    t = time.perf_counter()
    try:
        _detector = Detector()
        print(f"[detector] ready in {time.perf_counter() - t:.1f}s: {_detector.mode}"
              + (f" ({_detector.error})" if _detector.error else ""), flush=True)
    finally:
        _ready.set()


def detector(timeout=180):
    _ready.wait(timeout)
    return _detector


class Scrubber:
    def __init__(self):
        self.new_chat()

    @property
    def mode(self) -> str:
        if not _ready.is_set():
            return "loading the on-device model…"
        return _detector.mode if _detector else "patterns only"

    def new_chat(self):
        self.key = secrets.token_bytes(32)          # stand-ins rotate with every chat
        self.forward: dict[str, str] = {}           # original (lowercase) -> stand-in
        self.vault: dict[str, tuple[str, str]] = {}  # stand-in -> (original, kind), reversible only
        self.used: set[str] = set()

    # ------------------------------------------------------------ choosing stand-ins
    def _pick(self, pool, original, avoid):
        h = int.from_bytes(hmac.new(self.key, original.lower().encode(), hashlib.sha256).digest()[:4], "big")
        for i in range(len(pool)):
            c = pool[(h + i) % len(pool)]
            if c not in self.used and c.lower() not in avoid.lower():
                self.used.add(c)
                return c
        return f"{pool[h % len(pool)]}{len(self.used)}"

    def _remember(self, original, standin, kind):
        self.forward[original.lower()] = standin
        self.vault[standin] = (original, kind)
        return standin

    def _gender(self, text, start):
        before = text[max(0, start - 30):start].lower()
        if re.search(rf"\b({FEMALE_HINT})\b\.?\W*$", before):
            return "f"
        if re.search(rf"\b({MALE_HINT})\b\.?\W*$", before):
            return "m"
        return "n"

    def _person(self, original, text, start):
        title = ""
        m = TITLE_RE.match(original)
        if m:
            title, core = original[:m.end()], original[m.end():]
            gender = {"mr": "m", "mrs": "f", "ms": "f", "miss": "f"}.get(m.group(1).lower(), "n")
        else:
            core, gender = original, self._gender(text, start)
        words = core.split()
        if not words:
            return original
        first, last = words[0], words[-1] if len(words) > 1 else None
        if title:                                   # "mr. derek whitfield" -> "mr. Hayes"
            sur = self.forward.get(last.lower() if last else first.lower()) or self._remember(
                last or first, self._pick(SURNAMES, last or first, text), "person")
            if last:
                self._remember(core, f"{self.forward.get(first.lower()) or self._remember(first, self._pick(SUB[gender], first, text), 'person')} {sur}", "person")
            return f"{title}{sur}"
        f_sub = self.forward.get(first.lower()) or self._remember(first, self._pick(SUB[gender], first, text), "person")
        if not last:
            return f_sub
        l_sub = self.forward.get(last.lower()) or self._remember(last, self._pick(SURNAMES, last, text), "person")
        return self._remember(core, f"{f_sub} {l_sub}", "person")

    def _replace(self, span, text, geo):
        kind, original = span["kind"], span["text"]
        if original.lower() in self.forward:
            return self.forward[original.lower()], kind in REVERSIBLE
        if kind == "person":
            return self._person(original, text, span["start"]), True
        if kind == "custom":
            return self._remember(original, self._pick(CODENAMES, original, text), kind), True
        if kind == "org":
            cat = ORG_CATEGORY.get(original.lower().strip(" .,"))
            if cat:
                return cat, False
            return self._remember(original, self._pick(CODENAMES, original, text), kind), True
        if kind == "email":
            n = sum(k == "email" for _, k in self.vault.values()) + 1
            return self._remember(original, f"contact{n}@example.com", kind), True
        if kind == "phone":
            n = sum(k == "phone" for _, k in self.vault.values()) + 1
            return self._remember(original, f"(555) 010-{n:04d}", kind), True
        if kind == "location":
            hit = geo.region_of(original) if geo else None
            if hit:
                region, country = hit
                if not region:
                    return country, False
                return region, False
            return "[a place]", False
        if kind == "age":
            n = int(re.sub(r"\D", "", original) or 0)
            return f"{n // 10 * 10}-something", False
        if kind == "occupation":
            low = original.lower() + " "
            for cat, rx in OCCUPATIONS:
                if re.search(rx, low):
                    return cat, False
            return "professional", False
        if kind == "id":
            return f"[{span.get('label', 'ID number')} removed]" if span.get("label") not in (None, "number") \
                else "[number removed]", False
        return REMOVED.get(kind, "[removed]"), False

    # ------------------------------------------------------------ the swap
    def scrub(self, text: str, hide: list[str] | None = None, keep: list[str] | None = None,
              preview: bool = False) -> dict:
        """Swap personal details. preview=True leaves the vault untouched (for the live preview as you type)."""
        if preview:
            saved = (copy.deepcopy(self.forward), copy.deepcopy(self.vault), set(self.used))
        t0 = time.perf_counter()
        det = detector()
        spans = det.find(text) if det else []
        model_ms = (time.perf_counter() - t0) * 1000
        keep_set = {k.strip().lower() for k in (keep or []) if k.strip()}
        spans = [s for s in spans if s["text"].strip().lower() not in keep_set]
        custom = []
        for term in sorted({t.strip() for t in (hide or []) if t.strip()}, key=len, reverse=True):
            for m in re.finditer(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text, re.I):
                custom.append({"start": m.start(), "end": m.end(), "text": m.group(), "kind": "custom",
                               "source": "you", "score": 1.0})
        for c in custom:                               # your choices win over the detector
            spans = [s for s in spans if s["end"] <= c["start"] or s["start"] >= c["end"]]
        spans = sorted(spans + custom, key=lambda s: s["start"])

        geo = det.geo if det else None
        out, orig_segs, scrub_segs, found, pos = [], [], [], [], 0
        for s in spans:
            standin, reversible = self._replace(s, text, geo)
            if s["start"] > pos:
                gap = text[pos:s["start"]]
                orig_segs.append({"t": gap})
                scrub_segs.append({"t": gap})
                out.append(gap)
            label = LABELS.get(s["kind"], s["kind"])
            orig_segs.append({"t": s["text"], "k": label})
            scrub_segs.append({"t": standin, "k": label, "r": reversible})
            if s["kind"] == "occupation" and out and re.search(r"\b(a|an)\s+$", out[-1], re.I):   # "a nurse" -> "an healthcare worker" -> "a ..."
                art = "an" if re.match(r"[aeiou]", standin, re.I) else "a"
                out[-1] = re.sub(r"\b(a|an)(\s+)$", lambda m: (art.capitalize() if m.group(1)[0].isupper() else art) + m.group(2), out[-1])
            out.append(standin)
            found.append({"original": s["text"], "standin": standin, "kind": label, "reversible": reversible,
                          "source": s["source"], "score": s["score"]})
            pos = s["end"]
        orig_segs.append({"t": text[pos:]})
        scrub_segs.append({"t": text[pos:]})
        out.append(text[pos:])
        result = {"text": "".join(out), "orig_segments": orig_segs, "scrub_segments": scrub_segs, "found": found,
                  "ms": round((time.perf_counter() - t0) * 1000, 2), "model_ms": round(model_ms, 2),
                  "detector": self.mode}
        if preview:
            self.forward, self.vault, self.used = saved
        return result

    def restore(self, answer: str):
        """Put the originals back. Restored spans are wrapped in U+E000 .. U+E001 for the UI."""
        if not self.vault:
            return answer, []
        standins = sorted(self.vault, key=len, reverse=True)
        pattern = re.compile(r"(?<![\w@.-])(" + "|".join(map(re.escape, standins)) + r")(?![\w@-])")
        restored = []

        def sub(m):
            restored.append(m.group(1))
            return "" + self.vault[m.group(1)][0] + ""
        return pattern.sub(sub, answer), restored

    def vault_view(self):
        return [{"standin": s, "original": o, "kind": LABELS.get(k, k)} for s, (o, k) in self.vault.items()]
