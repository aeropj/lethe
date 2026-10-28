"""Find personal details in any prompt, on this machine.

Three local layers, merged:
- A multilingual PII model (GLiNER, urchade/gliner_multi_pii-v1, ~80-300 ms on a laptop CPU). It tags people,
  organisations, places, street addresses, ages, occupations and ID numbers whatever the casing, country or
  language: "i'm pranjal joshi ... surat gujarat ... 60 years old ... martial art tutor".
- Checksummed patterns for identifiers a model can miss: emails, phone numbers for any country
  (libphonenumber), card numbers, IBANs, social handles, and national IDs (US SSN, India PAN and Aadhaar,
  UK NINO, Brazil CPF, Canada SIN), plus street addresses and postcodes from several countries.
- A GeoNames gazetteer (34k cities) that finds well-known cities by name and maps any city to its state and
  country, so a place can be generalised instead of deleted.

Without the model (gliner not installed, or LETHE_MODEL=off) the patterns and gazetteer still run, and the
mode string says so.
"""
import csv
import os
import re
import threading
import time
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = Path(os.getenv("LETHE_DATA", HERE / "data"))
MODEL_NAME = os.getenv("LETHE_MODEL", "urchade/gliner_multi_pii-v1")

# model label -> (kind, threshold)
LABELS = {
    "person": ("person", 0.50),
    "organization": ("org", 0.80),
    "city": ("location", 0.55),
    "state or province": ("location", 0.55),
    "street address": ("address", 0.50),
    "postal code": ("postcode", 0.50),
    "age": ("age", 0.60),
    "occupation": ("occupation", 0.85),
    "phone number": ("phone", 0.50),
    "email": ("email", 0.50),
    "id number": ("id", 0.50),
    "date of birth": ("dob", 0.50),
    "bank account number": ("id", 0.50),
}
PRONOUNS = set("""i me my mine myself we us our ours you your yours he him his she her hers they them their theirs it
its im i'm ive i've id i'd ill i'll one someone somebody anyone everyone people person mom dad mum son daughter wife
husband kid kids child children boss manager friend doctor sir madam""".split())
# public institutions and financial or legal concepts: naming them identifies no one, and the answer needs them
PUBLIC = set("""lrs irs hmrc sec rbi sebi nhs fbi cia un eu who imf nasa adhd gst itr ppf nps elss epf uan 401k ira
roth medicare medicaid fema usps ssa dmv cra ato ncert cbse icse upsc neet jee sat gre gmat toefl ielts uif fbr
nadra sars hsa fsa isa sip etf reit cd ulip tfsa rrsp superannuation pension provident fund""".split())
# words that make a phrase a product, scheme or institution type, not a job or a named organisation
GENERIC_NOUNS = set("""ira fund funds account accounts card cards loan loans mortgage tax taxes policy plan plans scheme
schemes insurance stock stocks share shares bond bonds index etf court courts visa visas pension regime deposit interest
benefit benefits allowance subsidy permit license licence certificate degree course exam test""".split())
PUBLIC_PHRASES = {"roth ira", "traditional ira", "401(k)", "mutual fund", "social security", "income tax", "provident fund"}

EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
HANDLE_RE = re.compile(r"(?<![\w@])@[A-Za-z0-9_]{3,30}\b")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
CPF_RE = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
PAN_RE = re.compile(r"\b[A-Za-z]{5}\d{4}[A-Za-z]\b")
AADHAAR_RE = re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}\b")
NINO_RE = re.compile(r"\b[A-CEGHJ-PR-TW-Za-ceghj-pr-tw-z]{2} ?\d{2} ?\d{2} ?\d{2} ?[A-Da-d]\b")
SIN_RE = re.compile(r"\b\d{3}[- ]\d{3}[- ]\d{3}\b")
CARD_RE = re.compile(r"\b(?:\d[ -]?){12,18}\d\b")
IBAN_RE = re.compile(r"\b[A-Za-z]{2}\d{2}(?:[ ]?[A-Za-z0-9]){11,30}\b")
LONGNUM_RE = re.compile(r"\b\d{9,18}\b")
CODE_RE = re.compile(r"\b(?=[A-Za-z0-9-]*\d)(?=[A-Za-z0-9-]*[A-Za-z])[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b")
WALLET_RE = re.compile(r"\b0x[0-9a-fA-F]{40}\b")
NHS_RE = re.compile(r"\b\d{3} ?\d{3} ?\d{4}\b")
CONTEXT_ID_RE = re.compile(r"\b(?:number|no\.?|id|crn|cnic|rfc|ppo|permit|account|acct|passport|licen[cs]e|plate|"
                           r"registration|reg\.?|policy|member|patient|customer|aadhaar|pan|ssn|sin|nino|nhs|tfn|"
                           r"cpf|curp|dni|nie|nif|codice fiscale)\b\s*(?:is|es|est|ist|è|:|#|number|no\.?)?\s*[:#]?\s*"
                           r"([A-Za-z]{0,4}[- ]?[A-Za-z]{0,4}\d[\dA-Za-z -]{2,22}[\dA-Za-z])", re.I)
UK_POST_RE = re.compile(r"\b[A-Za-z]{1,2}\d[A-Za-z\d]? ?\d[A-Za-z]{2}\b")
CA_POST_RE = re.compile(r"\b[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d\b")
PIN_RE = re.compile(r"\b(?:pin|pincode|pin code|zip|zip code|postcode|postal code)[:\s#-]*(\d{5,6}(?:-\d{4})?)\b", re.I)
US_ZIP_RE = re.compile(r"\b(?:AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|"
                       r"NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC),?\s+(\d{5}(?:-\d{4})?)\b")
STREET_WORDS = (r"street|st(?!\.?\s+[A-Z])|road|rd|avenue|ave|lane|ln|drive|dr(?!\.?\s+[A-Z])|way|grove|close|crescent|cres|court|ct|place|pl|"
                r"terrace|boulevard|blvd|parkway|pkwy|highway|hwy|marg|nagar|colony|society|sector|apartments?|apt|"
                r"flat|rua|calle|avenida|strasse|straße")
ADDRESS_RE = re.compile(r"\b(?:(?:flat|apt|unit|house|plot|h\.?no\.?)\s*#?\s*)?\d{1,5}[a-z]?,?\s+"
                        r"(?:[A-Za-zÀ-ɏ][\w'À-ɏ-]*\s+){0,4}(?:" + STREET_WORDS + r")\b\.?", re.I)
DOB_RE = re.compile(r"(?:born on|born|dob:?|date of birth:?|birthday is|birthday:?)\s+"
                    r"((?:\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4})|(?:\d{1,2}(?:st|nd|rd|th)? [A-Za-z]+,? \d{4})|"
                    r"(?:[A-Za-z]+\.? \d{1,2}(?:st|nd|rd|th)?,? \d{4}))", re.I)
AGE_RE = re.compile(r"\b(\d{1,3})\s*(?:years? old|yrs? old|y/?o|-year-old)\b|\b(?:i am|i'm|im|aged|age)\s+(\d{1,3})\b", re.I)

KNOWN_ORGS = ["google", "alphabet", "meta", "facebook", "apple", "amazon", "microsoft", "netflix", "nvidia", "tesla",
              "salesforce", "oracle", "ibm", "intel", "uber", "airbnb", "stripe", "openai", "infosys", "tcs", "wipro",
              "flipkart", "accenture", "panasonic", "samsung", "sony", "huawei", "华为", "alibaba", "阿里巴巴",
              "tencent", "腾讯", "walmart", "costco", "fedex", "dhl", "ikea", "geico", "allstate", "state farm",
              "binance", "coinbase", "goldman sachs", "jpmorgan", "morgan stanley", "blackrock", "bank of america",
              "wells fargo", "citibank", "hsbc", "barclays", "state bank of india", "hdfc bank", "icici bank",
              "mckinsey", "deloitte", "kpmg", "pwc", "kaiser permanente", "kaiser", "aetna", "cigna", "humana"]
KNOWN_ORGS_RE = re.compile(r"(?<![\w-])(" + "|".join(map(re.escape, sorted(KNOWN_ORGS, key=len, reverse=True))) +
                           r")(?![\w-])|华为|阿里巴巴|腾讯", re.I)

PHONE_REGIONS = ["US", "IN", "GB", "NG", "BR", "CA", "AU", "DE", "FR", "ES", "MX", "ZA", "KE", "PK", "BD", "PH",
                 "ID", "SG", "AE", "CN", "JP", "IT", "NL", "IE", "NZ"]


# ---------------------------------------------------------------- checksums
def luhn(digits: str) -> bool:
    total, alt = 0, False
    for d in reversed(digits):
        n = int(d) * (2 if alt else 1)
        total += n - 9 if n > 9 else n
        alt = not alt
    return total % 10 == 0


_V_D = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
_V_P = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]


def verhoeff(digits: str) -> bool:
    c = 0
    for i, d in enumerate(reversed(digits)):
        c = _V_D[c][_V_P[i % 8][int(d)]]
    return c == 0


def nhs_ok(digits: str) -> bool:
    if len(digits) != 10:
        return False
    total = sum(int(d) * (10 - i) for i, d in enumerate(digits[:9]))
    check = 11 - total % 11
    return (0 if check == 11 else check) == int(digits[9]) and check != 10


def iban_ok(s: str) -> bool:
    s = s.replace(" ", "").upper()
    if not 15 <= len(s) <= 34:
        return False
    n = "".join(str(int(ch, 36)) for ch in s[4:] + s[:4])
    return int(n) % 97 == 1


# ---------------------------------------------------------------- gazetteer
class Gazetteer:
    """GeoNames cities with population >= 15k: name -> (region, country). Well-known cities are also found by name."""

    COMMON = set("""of nice split mobile reading bath worth march may sale most hope victoria florence aurora
    independence orange garden grove columbia lincoln marion union jackson mesa page""".split())

    def __init__(self, folder: Path):
        self.city = {}
        self.foreign = {}
        self.known = set()
        self.regions = set()
        self.countries = set()
        cities = folder / "cities15000.txt"
        if not cities.exists():
            return
        admin1 = {}
        for row in csv.reader(open(folder / "admin1CodesASCII.txt", encoding="utf-8"), delimiter="\t"):
            if len(row) >= 2:
                admin1[row[0]] = row[1]
        country = {}
        for line in open(folder / "countryInfo.txt", encoding="utf-8"):
            if not line.startswith("#"):
                f = line.rstrip("\n").split("\t")
                if len(f) > 4:
                    country[f[0]] = f[4]
        self.regions = {v.lower() for v in admin1.values()}
        self.countries = {v.lower() for v in country.values()}
        for f in csv.reader(open(cities, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE):
            name, ascii_name, cc, a1, pop = f[1], f[2], f[8], f[10], int(f[14] or 0)
            if pop >= 1_000_000:              # big cities: also their names in other scripts (上海, القاهرة, Москва)
                for alt in f[3].split(","):
                    if alt and not re.match(r"^[A-Za-z .'-]*$", alt) and len(alt) >= 2 and not alt.isdigit():
                        self.foreign[alt.lower()] = (admin1.get(f"{cc}.{a1}", ""), country.get(cc, cc), pop)
            region, ctry = admin1.get(f"{cc}.{a1}", ""), country.get(cc, cc)
            names = {name.lower(), ascii_name.lower()}
            names |= {re.sub(r"\s+(city|town)$", "", n) for n in names}
            for n in names:
                if n and (n not in self.city or self.city[n][2] < pop):
                    self.city[n] = (region, ctry, pop)
                if pop >= 250_000 and len(n) > 3 and n not in self.COMMON:
                    self.known.add(n)
        known = sorted(self.known, key=len, reverse=True)
        self.known_re = re.compile(r"(?<![\w-])(" + "|".join(map(re.escape, known)) + r")(?![\w-])", re.I) if known else None
        for k, v in self.foreign.items():
            if k not in self.city or self.city[k][2] < v[2]:
                self.city[k] = v
        foreign = sorted(self.foreign, key=len, reverse=True)
        self.foreign_re = re.compile("|".join(map(re.escape, foreign))) if foreign else None

    def region_of(self, text: str):
        """Best (region, country) for a place mention such as 'surat gujarat' or 'ikeja, lagos'."""
        words = re.findall(r"[\wÀ-ɏ.'-]+", text.lower())
        best, name = None, ""
        for size in (3, 2, 1):
            for i in range(len(words) - size + 1):
                key = " ".join(words[i:i + size])
                hit = self.city.get(key)
                if hit and (best is None or hit[2] > best[2]):
                    best, name = hit, key
            if best:
                break
        if not best:
            return None
        region, country = best[0], best[1]
        if not region or name in region.lower():     # Lagos/Lagos, Nairobi/Nairobi County: the region names the city
            return ("", country)
        return (region, country)

    def is_region_or_country(self, text: str) -> bool:
        t = text.lower().strip(" .,")
        return t in self.regions or t in self.countries


def fetch_geonames(folder: Path):
    """First start only: download the GeoNames city list (CC BY 4.0, ~3 MB zipped) into demo/data."""
    if (folder / "cities15000.txt").exists():
        return
    import io
    import urllib.request
    import zipfile
    base = "https://download.geonames.org/export/dump/"
    try:
        folder.mkdir(parents=True, exist_ok=True)
        print("[detector] downloading the GeoNames city list (first start only)…", flush=True)
        zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(base + "cities15000.zip", timeout=60).read())).extractall(folder)
        for f in ("admin1CodesASCII.txt", "countryInfo.txt"):
            (folder / f).write_bytes(urllib.request.urlopen(base + f, timeout=60).read())
    except Exception as e:  # cities then fall back to the model alone
        print(f"[detector] could not download GeoNames ({e}); places will rely on the model", flush=True)


@lru_cache(maxsize=1)
def gazetteer() -> Gazetteer:
    fetch_geonames(DATA)
    return Gazetteer(DATA)


# ---------------------------------------------------------------- the detector
class Detector:
    def __init__(self):
        self.model = None
        self.error = None
        self.load_ms = 0
        if MODEL_NAME.lower() != "off":
            try:
                t = time.perf_counter()
                from gliner import GLiNER
                local = DATA / "model"
                self.model = GLiNER.from_pretrained(str(local) if local.exists() else MODEL_NAME)
                self.model.predict_entities("warm up with Ada Lovelace in London", ["person"], threshold=0.5)
                self.load_ms = (time.perf_counter() - t) * 1000
            except Exception as e:  # keep working on patterns alone, and say so
                self.error = f"{type(e).__name__}: {e}"[:200]
        self.geo = gazetteer()
        self.lock = threading.Lock()   # one inference at a time: the live preview and a request can overlap

    @property
    def mode(self) -> str:
        parts = ["GLiNER multilingual PII model" if self.model else "patterns only (model unavailable)",
                 "worldwide ID patterns", "GeoNames" if self.geo.city else "no gazetteer"]
        return " + ".join(parts) + ", on device"

    def find(self, text: str) -> list[dict]:
        spans = []

        def add(start, end, kind, source, score=1.0, **meta):
            if end > start:
                spans.append({"start": start, "end": end, "text": text[start:end], "kind": kind,
                              "source": source, "score": round(score, 2), **meta})

        # ---- model
        if self.model is not None:
            for chunk_start, chunk in _chunks(text):
                feed, back = _spaced(chunk)
                with self.lock:
                    ents = self.model.predict_entities(feed, list(LABELS), threshold=0.35)
                for e in ents:
                    e = dict(e, start=back[e["start"]], end=back[e["end"] - 1] + 1)
                    kind, thr = LABELS[e["label"]]
                    if e["score"] < thr:
                        continue
                    s, t = chunk_start + e["start"], chunk_start + e["end"]
                    word = text[s:t].strip()
                    low = word.lower().strip(".,")
                    if kind == "person" and (low in PRONOUNS or len(low) < 2 or not re.search(r"[^\W\d_]", low)):
                        continue
                    if kind == "org" and (low in PUBLIC or low in PUBLIC_PHRASES
                                          or all(w in PUBLIC for w in re.findall(r"[\w()]+", low))):
                        continue
                    words = re.findall(r"[\w()]+", low)
                    if kind == "occupation" and any(w in GENERIC_NOUNS or w in PUBLIC for w in words):
                        continue          # "roth ira" is a product, not a job
                    if kind == "org" and word == low and any(w in GENERIC_NOUNS for w in words):
                        continue          # "family court": a lowercase generic institution, not a named one
                    if kind == "org" and word == low and re.search(r"\b(a|an)\s+$", text[max(0, s - 4):s], re.I):
                        continue          # "a textile shop": an indefinite, lowercase phrase is generic
                    if kind in ("org", "location") and len(low) < 3 and not re.search(r"[^\x00-\x7f]", low):
                        continue
                    if kind == "location" and self.geo.is_region_or_country(low):
                        continue          # a state or country identifies no one; it is what we generalise to
                    if kind == "age":
                        m = re.search(r"\d{1,3}", word)
                        if not m or int(m.group()) < 18 or int(m.group()) > 115:
                            continue
                        s, t = s + m.start(), s + m.end()
                    add(s, t, kind, "model", e["score"])

        # ---- patterns
        for m in EMAIL_RE.finditer(text):
            add(m.start(), m.end(), "email", "pattern")
        for m in HANDLE_RE.finditer(text):
            add(m.start(), m.end(), "id", "pattern", label="handle")
        for m in SSN_RE.finditer(text):
            add(m.start(), m.end(), "id", "pattern", label="SSN")
        for m in CPF_RE.finditer(text):
            add(m.start(), m.end(), "id", "pattern", label="CPF")
        for m in PAN_RE.finditer(text):
            if re.search(r"\d", m.group()) and re.search(r"[A-Za-z]{5}", m.group()):
                add(m.start(), m.end(), "id", "pattern", label="PAN")
        for m in AADHAAR_RE.finditer(text):
            if verhoeff(re.sub(r"\D", "", m.group())):
                add(m.start(), m.end(), "id", "pattern", label="Aadhaar")
        for m in NINO_RE.finditer(text):
            add(m.start(), m.end(), "id", "pattern", label="NI number")
        for m in SIN_RE.finditer(text):
            if luhn(re.sub(r"\D", "", m.group())):
                add(m.start(), m.end(), "id", "pattern", label="SIN")
        for m in CARD_RE.finditer(text):
            d = re.sub(r"\D", "", m.group())
            if 13 <= len(d) <= 19 and luhn(d):
                add(m.start(), m.end(), "card", "pattern")
        for m in IBAN_RE.finditer(text):
            cand = m.group()
            while len(cand.replace(" ", "")) >= 15 and not iban_ok(cand):
                cand = re.sub(r"\s*\S$", "", cand)          # drop trailing characters until the checksum holds
            if iban_ok(cand):
                add(m.start(), m.start() + len(cand), "id", "pattern", label="IBAN")
        for m in WALLET_RE.finditer(text):
            add(m.start(), m.end(), "id", "pattern", label="wallet")
        for m in NHS_RE.finditer(text):
            if nhs_ok(re.sub(r"\D", "", m.group())):
                add(m.start(), m.end(), "id", "pattern", label="NHS number")
        for m in CODE_RE.finditer(text):
            tok = m.group()
            if len(tok) >= 8 and sum(ch.isdigit() for ch in tok) >= 5:
                add(m.start(), m.end(), "id", "pattern", label="ID number")
        phones = [(x["start"], x["end"]) for x in spans if x["kind"] == "phone"]
        for m in CONTEXT_ID_RE.finditer(text):
            code = m.group(1).rstrip()
            if any(a < m.start(1) + len(code) and m.start(1) < b for a, b in phones):
                continue                      # a valid phone number stays a phone number
            if sum(ch.isdigit() for ch in code) >= 4:
                add(m.start(1), m.start(1) + len(code), "id", "pattern", label="ID number")
        try:
            import phonenumbers
            seen = set()
            for region in PHONE_REGIONS:
                for m in phonenumbers.PhoneNumberMatcher(text, region, leniency=phonenumbers.Leniency.VALID):
                    if (m.start, m.end) not in seen:
                        seen.add((m.start, m.end))
                        add(m.start, m.end, "phone", "pattern")
        except ImportError:
            pass
        for m in LONGNUM_RE.finditer(text):
            add(m.start(), m.end(), "id", "pattern", label="number")
        for m in ADDRESS_RE.finditer(text):
            add(m.start(), m.end(), "address", "pattern")
        for rx in (UK_POST_RE, CA_POST_RE):
            for m in rx.finditer(text):
                if re.search(r"\d", m.group()) and re.search(r"[A-Za-z]", m.group()):
                    add(m.start(), m.end(), "postcode", "pattern")
        for rx in (PIN_RE, US_ZIP_RE):
            for m in rx.finditer(text):
                add(m.start(1), m.end(1), "postcode", "pattern")
        for m in DOB_RE.finditer(text):
            add(m.start(1), m.end(1), "dob", "pattern")
        for m in AGE_RE.finditer(text):
            g = 1 if m.group(1) else 2
            if 18 <= int(m.group(g)) <= 115:
                add(m.start(g), m.end(g), "age", "pattern")
        if self.geo.known_re is not None:
            for m in self.geo.known_re.finditer(text):
                add(m.start(), m.end(), "location", "gazetteer")
        if self.geo.foreign_re is not None and re.search(r"[^\x00-\u024f]", text):
            for m in self.geo.foreign_re.finditer(text):
                add(m.start(), m.end(), "location", "gazetteer")
        for m in KNOWN_ORGS_RE.finditer(text):
            add(m.start(), m.end(), "org", "pattern")

        # ---- a 5-6 digit number right after a place is a postcode
        for s in [x for x in spans if x["kind"] in ("location", "address")]:
            m = re.match(r"[\s,-]{1,3}(\d{5,6})\b", text[s["end"]:])
            if m:
                add(s["end"] + m.start(1), s["end"] + m.end(1), "postcode", "pattern")

        return _resolve(spans)


CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]")


def _spaced(text: str):
    """The model splits words on spaces; Chinese, Japanese and Korean have none. Space those characters out
    for the model, and keep a map from each model position back to the original."""
    if not CJK.search(text):
        return text, list(range(len(text) + 1))
    out, back = [], []
    for i, ch in enumerate(text):
        if CJK.match(ch):
            if out and out[-1] != " ":
                out.append(" "); back.append(i)
            out.append(ch); back.append(i)
            out.append(" "); back.append(i)
        else:
            out.append(ch); back.append(i)
    back.append(len(text))
    return "".join(out), back


def _chunks(text: str, size: int = 1200):
    """GLiNER reads ~384 tokens at a time: feed it sentence-aligned chunks."""
    if len(text) <= size:
        yield 0, text
        return
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        if end < len(text):
            cut = max(text.rfind(". ", start, end), text.rfind("\n", start, end))
            if cut > start + size // 2:
                end = cut + 1
        yield start, text[start:end]
        start = end


PRIORITY = {"email": 0, "card": 0, "id": 0, "phone": 1, "address": 1, "postcode": 1, "dob": 1, "person": 2,
            "org": 3, "location": 3, "age": 4, "occupation": 5}


def _resolve(spans):
    """Overlaps: identifiers first, then the longer span, then the higher score."""
    kept = []
    for s in sorted(spans, key=lambda s: (PRIORITY.get(s["kind"], 9), -(s["end"] - s["start"]), -s["score"])):
        if all(s["end"] <= k["start"] or s["start"] >= k["end"] for k in kept):
            kept.append(s)
    return sorted(kept, key=lambda s: s["start"])
