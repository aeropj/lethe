"""On-device scrubber: finds personal details and swaps them before a prompt leaves the device.

Rules run locally in a few milliseconds. Set LETHE_LOCAL_MODEL (an Ollama model, e.g.
qwen3:1.7b) to also ask a small local model for anything the rules miss.

Two kinds of swap:
- reversible: names, emails, phones and your "always hide" terms become consistent stand-ins;
  the vault on your device maps them back when the answer arrives.
- generalised: cities become their state, insurers and employers become their category.
  The answer stays useful and nothing needs reversing.
Stand-ins are keyed per chat, so the same person gets a different stand-in in the next chat.
"""
import hashlib
import hmac
import json
import os
import re
import secrets
import time
import urllib.request

MALE = set("""James Michael John Robert David William Richard Joseph Thomas Christopher Charles Daniel Matthew
Anthony Mark Donald Steven Andrew Paul Joshua Kenneth Kevin Brian George Timothy Ronald Jason Edward Jeffrey Ryan
Jacob Gary Nicholas Eric Jonathan Stephen Larry Justin Scott Brandon Benjamin Samuel Gregory Alexander Patrick Frank
Raymond Jack Dennis Jerry Tyler Aaron Henry Adam Nathan Zachary Kyle Ethan Noah Liam Mason Logan Lucas Jackson Aiden
Elijah Owen Caleb Dylan Luke Isaac Gabriel Carter Jayden Wyatt Grayson Leo Hunter Connor Eli Raj Wei Jose Carlos Juan
Luis Miguel Diego Mateo Arjun Rohan Omar Ali Kenji Sam Ben Max Alex Chris Mike Matt Dan Nick Tom Joe Josh""".split())
FEMALE = set("""Mary Patricia Jennifer Linda Elizabeth Barbara Susan Jessica Sarah Karen Lisa Nancy Betty Sandra
Margaret Ashley Kimberly Emily Donna Michelle Carol Amanda Melissa Deborah Stephanie Rebecca Laura Sharon Cynthia
Kathleen Amy Angela Shirley Anna Brenda Pamela Emma Nicole Helen Samantha Katherine Christine Debra Rachel Carolyn
Janet Maria Olivia Heather Diane Julie Joyce Victoria Kelly Christina Lauren Joan Evelyn Judith Megan Andrea Cheryl
Hannah Jacqueline Martha Gloria Teresa Ann Sara Madison Frances Kathryn Janice Jean Abigail Alice Judy Sophia Grace
Denise Ava Isabella Mia Charlotte Amelia Harper Chloe Ella Avery Sofia Scarlett Aria Lily Zoe Nora Riley Layla Priya
Mei Ana Camila Valentina Aisha Fatima Yuki Jess Kate Liz Jen""".split())

SUB = {
    "m": "Rowan Felix Jonah Theo Ezra Silas Miles Jasper Callum Declan Emmett Rhys Tobias Arlo Bennett".split(),
    "f": "Hazel Iris Clara Tessa Elise Maeve Ruby Wren Margo Sienna Delia Imogen Freya Esme Juno".split(),
    "n": "Quinn Reese Sage Emerson Finley Parker Rory Blair Sloane Marlowe".split(),
}
SURNAMES = "Hayes Ellison Brooks Calloway Whitaker Merritt Langley Sutton Ashford Pryor Holloway Kendrick".split()
CODENAMES = "Kestrel Juniper Halcyon Meridian Larkspur Ardent Solace Tamarind Corvid Saltmarsh".split()

RELATIONS = {"son": "m", "daughter": "f", "wife": "f", "husband": "m", "mom": "f", "mother": "f", "dad": "m",
             "father": "m", "brother": "m", "sister": "f", "boyfriend": "m", "girlfriend": "f"}
RELATION_RE = re.compile(
    r"\b(?:[Mm]y|[Oo]ur)\s+(son|daughter|kid|child|wife|husband|partner|boss|manager|friend|mom|mother|dad|father|"
    r"brother|sister|colleague|coworker|doctor|therapist|boyfriend|girlfriend)\s*,?\s+([A-Z][a-z]+)")
TITLE_RE = re.compile(r"\b(Mr|Mrs|Ms|Miss|Dr|Mx)\.?\s+([A-Z][a-z]+(?:-[A-Z][a-z]+)?)")
TITLE_GENDER = {"Mr": "m", "Mrs": "f", "Ms": "f", "Miss": "f"}
ZIP_RE = re.compile(r"\b(?:AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|"
                    r"NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC),?\s+(\d{5}(?:-\d{4})?)\b")
INTRO_RE = re.compile(r"\b(?:[Mm]y name is|[Mm]y name's)\s+([A-Z][a-z]+)")

STATES = {
    "California": "Sacramento San Francisco Los Angeles San Diego San Jose Oakland Fresno Palo Alto Berkeley Irvine Pasadena",
    "Washington": "Seattle Spokane Tacoma Bellevue Redmond", "Oregon": "Portland Eugene",
    "Texas": "Austin Dallas Houston San Antonio Fort Worth El Paso", "Illinois": "Chicago Evanston",
    "New York": "Brooklyn Manhattan Queens Bronx Buffalo Rochester", "Massachusetts": "Boston Cambridge Somerville",
    "Florida": "Miami Orlando Tampa Jacksonville", "Colorado": "Denver Boulder", "Arizona": "Phoenix Tucson Scottsdale",
    "Georgia": "Atlanta Savannah", "Pennsylvania": "Philadelphia Pittsburgh", "Michigan": "Detroit Ann Arbor",
    "Minnesota": "Minneapolis", "Tennessee": "Nashville Memphis", "Nevada": "Las Vegas Reno",
    "Utah": "Salt Lake City Provo", "Maryland": "Baltimore Bethesda", "North Carolina": "Raleigh Durham Chapel Hill",
    "Ohio": "Columbus Cleveland Cincinnati", "Indiana": "Indianapolis", "Missouri": "St. Louis Kansas City",
    "Louisiana": "New Orleans Baton Rouge", "Hawaii": "Honolulu", "New Mexico": "Albuquerque Santa Fe",
    "Kentucky": "Louisville Lexington", "Virginia": "Richmond Arlington", "New Jersey": "Newark Jersey City Hoboken",
    "Connecticut": "Hartford New Haven", "Rhode Island": "Providence", "Idaho": "Boise", "Oklahoma": "Tulsa Oklahoma City",
    "Wisconsin": "Milwaukee", "Nebraska": "Omaha", "Iowa": "Des Moines",
}
_TWO_WORD = {"San", "Los", "Palo", "Fort", "El", "Ann", "Salt", "Lake", "Chapel", "Kansas", "New", "Baton", "Santa",
             "Jersey", "Oklahoma", "Des", "Las", "St."}
CITIES = {}
for state, names in STATES.items():
    words, buf = names.split(), []
    for w in words:
        buf.append(w)
        if w not in _TWO_WORD:
            CITIES[" ".join(buf)] = state
            buf = []
CITIES["New York City"] = CITIES["NYC"] = "New York"

ORGS = {
    "an HMO": ["Kaiser Permanente", "Kaiser"],
    "a health insurer": ["Blue Cross Blue Shield", "Blue Cross", "Blue Shield", "UnitedHealthcare", "United Healthcare",
                         "Aetna", "Cigna", "Humana", "Anthem", "Oscar Health", "Molina"],
    "a big tech company": ["Google", "Alphabet", "Meta", "Facebook", "Apple", "Amazon", "Microsoft", "Netflix", "Nvidia",
                           "Tesla", "Salesforce", "Oracle", "IBM", "Intel", "Uber", "Airbnb", "Stripe", "OpenAI"],
    "a large financial firm": ["Goldman Sachs", "JPMorgan", "J.P. Morgan", "Morgan Stanley", "Citadel", "BlackRock",
                               "Bank of America", "Wells Fargo", "Citibank", "Citi"],
    "a large consulting firm": ["McKinsey", "Deloitte", "Boston Consulting Group", "BCG", "Bain", "Accenture", "PwC", "KPMG"],
    "a major hospital": ["Mayo Clinic", "Cleveland Clinic", "Johns Hopkins", "Mass General", "UCSF", "Stanford Health",
                         "Cedars-Sinai"],
}
STOP = set("""I The A An Should We We're He She They My Our Is Can What How Why When Where Who Do Does Did And But Or
So If On In At To From Please Thanks Hi Hello Dear It It's This That There Also Just Yes No Not Monday Tuesday Wednesday
Thursday Friday Saturday Sunday January February March April May June July August September October November December
ADHD""".split())

EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
PHONE_RE = re.compile(r"(?<![\d-])(?:\+1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]\d{4}(?![\d-])")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
CARD_RE = re.compile(r"\b(?:\d[ -]?){12,18}\d\b")
ADDRESS_RE = re.compile(r"\b\d{1,5}\s+(?:[A-Z][a-z]+\s){1,3}(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive|"
                        r"Ln|Lane|Way|Ct|Court|Pl|Place)\b")
DOB_RE = re.compile(r"(?:born on|born|DOB:?|date of birth:?)\s+((?:\d{1,2}/\d{1,2}/\d{2,4})|(?:[A-Z][a-z]+\.? \d{1,2}, \d{4}))")

# priority: lower wins when spans overlap
P_CUSTOM, P_ID, P_ORG, P_CITY, P_NAME, P_LOCAL = range(6)
LABELS = {"name": "person", "email": "email", "phone": "phone", "ssn": "SSN", "card": "card number",
          "address": "street address", "dob": "birth date", "zip": "ZIP code", "city": "city", "org": "organisation",
          "custom": "always hide", "local": "local model"}


def _luhn(digits: str) -> bool:
    total, alt = 0, False
    for d in reversed(digits):
        n = int(d) * (2 if alt else 1)
        total += n - 9 if n > 9 else n
        alt = not alt
    return total % 10 == 0


class Scrubber:
    def __init__(self, local_model: str | None = None):
        self.local_model = local_model if local_model is not None else os.getenv("LETHE_LOCAL_MODEL", "")
        self.new_chat()

    @property
    def mode(self) -> str:
        return f"rules + {self.local_model} (Ollama, on device)" if self.local_model else "rules, on device"

    def new_chat(self):
        self.key = secrets.token_bytes(32)  # stand-ins rotate with every chat
        self.forward: dict[str, str] = {}   # original -> stand-in
        self.vault: dict[str, tuple[str, str]] = {}  # stand-in -> (original, kind), reversible only
        self.used: set[str] = set()

    # ------------------------------------------------------------ detection
    def _spans(self, text: str, hide: list[str]):
        spans = []

        def add(m, kind, prio, meta=None, group=0):
            spans.append((m.start(group), m.end(group), kind, prio, meta or {}))

        for term in sorted({t.strip() for t in hide if t.strip()}, key=len, reverse=True):
            for m in re.finditer(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text, re.I):
                add(m, "custom", P_CUSTOM)
        for m in EMAIL_RE.finditer(text):
            add(m, "email", P_ID)
        for m in SSN_RE.finditer(text):
            add(m, "ssn", P_ID)
        for m in CARD_RE.finditer(text):
            if _luhn(re.sub(r"\D", "", m.group())):
                add(m, "card", P_ID)
        for m in PHONE_RE.finditer(text):
            add(m, "phone", P_ID)
        for m in ADDRESS_RE.finditer(text):
            add(m, "address", P_ID)
        for m in ZIP_RE.finditer(text):
            add(m, "zip", P_ID, group=1)
        for m in DOB_RE.finditer(text):
            add(m, "dob", P_ID, group=1)
        for category, names in ORGS.items():
            for name in names:
                for m in re.finditer(r"(?<!\w)" + re.escape(name) + r"(?!\w)", text):
                    add(m, "org", P_ORG, {"category": category})
        for city, state in CITIES.items():
            for m in re.finditer(r"(?<!\w)" + re.escape(city) + r"(?!\w)", text):
                add(m, "city", P_CITY, {"state": state})
        for m in RELATION_RE.finditer(text):
            first = m.group(2)
            if first not in STOP:
                gender = RELATIONS.get(m.group(1).lower()) or self._gender(first)
                spans.append(self._name_span(text, m.start(2), first, gender))
        for m in TITLE_RE.finditer(text):
            if m.group(2) not in STOP:
                spans.append(self._name_span(text, m.start(2), m.group(2), TITLE_GENDER.get(m.group(1), "n"), surname=True))
        for m in INTRO_RE.finditer(text):
            spans.append(self._name_span(text, m.start(1), m.group(1), self._gender(m.group(1))))
        for m in re.finditer(r"\b[A-Z][a-z]+\b", text):
            if m.group() in MALE or m.group() in FEMALE:
                spans.append(self._name_span(text, m.start(), m.group(), self._gender(m.group())))
        spans += self._local_model_spans(text)

        kept = []  # resolve overlaps: priority first, then the longer span
        for s in sorted(spans, key=lambda s: (s[3], -(s[1] - s[0]))):
            if all(s[1] <= k[0] or s[0] >= k[1] for k in kept):
                kept.append(s)
        return sorted(kept)

    @staticmethod
    def _gender(first: str) -> str:
        return "m" if first in MALE else "f" if first in FEMALE else "n"

    @staticmethod
    def _name_span(text, start, first, gender, surname=False):
        end = start + len(first)
        if surname:  # "Mrs. Johnson": the one word is a surname
            return (start, end, "name", P_NAME, {"first": first, "last": None, "gender": gender, "surname": True})
        m = re.match(r"[ ]([A-Z][a-z]+(?:-[A-Z][a-z]+)?)\b", text[end:])
        last = m.group(1) if m else None
        if last and (last in STOP or last in CITIES or last in MALE or last in FEMALE
                     or any(last in names for names in ORGS.values())):
            last = None
        if last:
            end += 1 + len(last)
        return (start, end, "name", P_NAME, {"first": first, "last": last, "gender": gender})

    def _local_model_spans(self, text):
        if not self.local_model:
            return []
        prompt = ("List every personal identifier in the text below: people, organisations, places and ID numbers. "
                  'Reply only as JSON {"entities":[{"text":"<exact substring>","type":"PERSON|ORG|PLACE|ID"}]}.\n\n' + text)
        body = json.dumps({"model": self.local_model, "prompt": prompt, "format": "json", "stream": False}).encode()
        req = urllib.request.Request("http://localhost:11434/api/generate", data=body,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                entities = json.loads(json.load(r)["response"]).get("entities", [])
        except Exception:
            return []
        spans = []
        for e in entities:
            t = str(e.get("text", "")).strip()
            if len(t) > 1:
                for m in re.finditer(re.escape(t), text):
                    spans.append((m.start(), m.end(), "local", P_LOCAL, {"type": str(e.get("type", "")).upper()}))
        return spans

    # ------------------------------------------------------------ replacement
    def _pick(self, pool, original, avoid):
        h = int.from_bytes(hmac.new(self.key, original.encode(), hashlib.sha256).digest()[:4], "big")
        for i in range(len(pool)):
            c = pool[(h + i) % len(pool)]
            if c not in self.used and c not in avoid:
                self.used.add(c)
                return c
        return f"{pool[h % len(pool)]}{len(self.used)}"

    def _remember(self, original, standin, kind):
        self.forward[original] = standin
        self.vault[standin] = (original, kind)
        return standin

    def _replace(self, kind, original, meta, text):
        if original in self.forward:
            return self.forward[original], kind not in ("city", "org", "ssn", "card", "address", "dob", "zip")
        if kind == "name" and meta.get("surname"):
            return self._remember(original, self._pick(SURNAMES, original, text), kind), True
        if kind == "name":
            first = self.forward.get(meta["first"]) or self._remember(
                meta["first"], self._pick(SUB[meta["gender"]], meta["first"], text), "name")
            if not meta["last"]:
                return first, True
            last = self.forward.get(meta["last"]) or self._remember(
                meta["last"], self._pick(SURNAMES, meta["last"], text), "name")
            return self._remember(original, f"{first} {last}", "name"), True
        if kind == "email":
            n = sum(k == "email" for _, k in self.vault.values()) + 1
            return self._remember(original, f"contact{n}@example.com", kind), True
        if kind == "phone":
            n = sum(k == "phone" for _, k in self.vault.values()) + 1
            return self._remember(original, f"(555) 010-{n:04d}", kind), True
        if kind == "custom":
            return self._remember(original, self._pick(CODENAMES, original.lower(), text), kind), True
        if kind == "city":
            return meta["state"], False
        if kind == "org":
            return meta["category"], False
        if kind == "local":
            t = meta["type"]
            if t == "PERSON":
                return self._remember(original, self._pick(SUB["n"], original, text), "name"), True
            if t == "ORG":
                return self._remember(original, self._pick(CODENAMES, original, text), "custom"), True
            return ("a nearby town" if t == "PLACE" else "[ID removed]"), False
        return {"ssn": "[SSN removed]", "card": "[card number removed]", "address": "[street address]",
                "dob": "[birth date]", "zip": "[ZIP]"}[kind], False

    def scrub(self, text: str, hide: list[str] | None = None) -> dict:
        t0 = time.perf_counter()
        spans = self._spans(text, hide or [])
        out, orig_segs, scrub_segs, found, pos = [], [], [], [], 0
        for start, end, kind, _, meta in spans:
            original = text[start:end]
            standin, reversible = self._replace(kind, original, meta, text)
            if start > pos:
                orig_segs.append({"t": text[pos:start]})
                scrub_segs.append({"t": text[pos:start]})
                out.append(text[pos:start])
            label = LABELS[kind]
            orig_segs.append({"t": original, "k": label})
            scrub_segs.append({"t": standin, "k": label, "r": reversible})
            out.append(standin)
            found.append({"original": original, "standin": standin, "kind": label, "reversible": reversible})
            pos = end
        orig_segs.append({"t": text[pos:]})
        scrub_segs.append({"t": text[pos:]})
        out.append(text[pos:])
        return {"text": "".join(out), "orig_segments": orig_segs, "scrub_segments": scrub_segs, "found": found,
                "ms": round((time.perf_counter() - t0) * 1000, 2)}

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
