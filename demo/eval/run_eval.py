#!/usr/bin/env python3
"""Score the on-device detector on demo/eval/cases.jsonl and write demo/eval/RESULTS.md.

For each prompt we check the text that would leave the device:
- identifiers: every listed name, place, organisation, contact or ID must be gone (word match, any case);
- quasi-identifiers: exact adult ages must become a decade, listed occupations must be generalised;
- usefulness: listed terms the answer needs (drug names, tax schemes, amounts) must survive.
"""
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scrub  # noqa: E402


def present(term: str, text: str) -> bool:
    if re.match(r"^[A-Za-z0-9\u00C0-\u024F\s.'-]+$", term):
        return re.search(r"(?<![\w])" + re.escape(term) + r"(?![\w])", text, re.I) is not None
    return term.lower() in text.lower()


def main():
    t = time.time()
    scrub.load_detector()
    print(f"detector: {scrub.detector().mode} (loaded in {time.time() - t:.1f}s)")
    name = sys.argv[1] if len(sys.argv) > 1 else "cases"
    cases = [json.loads(l) for l in open(HERE / f"{name}.jsonl", encoding="utf-8") if l.strip()]
    rows, tot = [], {"hide": 0, "hide_ok": 0, "age": 0, "age_ok": 0, "occ": 0, "occ_ok": 0, "keep": 0, "keep_ok": 0,
                     "clean": 0, "ms": []}
    for c in cases:
        sc = scrub.Scrubber()
        r = sc.scrub(c["text"])
        sent = r["text"]
        tot["ms"].append(r["ms"])
        leaks = [h for h in c.get("hide", []) if present(h, sent)]
        ages = [a for a in c.get("age", []) if re.search(rf"(?<!\d){a}(?![\d-])", sent)]
        occs = [o for o in c.get("occupation", []) if present(o, sent)]
        lost = [k for k in c.get("keep", []) if not present(k, sent)]
        for k, n, bad in (("hide", len(c.get("hide", [])), leaks), ("age", len(c.get("age", [])), ages),
                          ("occ", len(c.get("occupation", [])), occs), ("keep", len(c.get("keep", [])), lost)):
            tot[k] += n
            tot[k + "_ok"] += n - len(bad)
        tot["clean"] += not leaks
        rows.append((c["id"], c["text"], sent, leaks, ages, occs, lost, r["ms"]))

    pct = lambda a, b: f"{100 * a / b:.1f}%" if b else "n/a"
    ms = sorted(tot["ms"])
    summary = [
        f"| Identifiers removed (names, places, organisations, contacts, IDs) | **{pct(tot['hide_ok'], tot['hide'])}** "
        f"({tot['hide_ok']}/{tot['hide']}) |",
        f"| Prompts with no identifier left | **{pct(tot['clean'], len(cases))}** ({tot['clean']}/{len(cases)}) |",
        f"| Exact adult ages generalised | {pct(tot['age_ok'], tot['age'])} ({tot['age_ok']}/{tot['age']}) |",
        f"| Occupations generalised | {pct(tot['occ_ok'], tot['occ'])} ({tot['occ_ok']}/{tot['occ']}) |",
        f"| Useful terms kept (drugs, schemes, amounts) | {pct(tot['keep_ok'], tot['keep'])} ({tot['keep_ok']}/{tot['keep']}) |",
        f"| Median / slowest detection time | {ms[len(ms) // 2]:.0f} ms / {ms[-1]:.0f} ms |",
    ]
    md = [f"# Detector evaluation\n\n{len(cases)} prompts in 13 languages and styles (US, UK, India, Nigeria, Kenya, "
          "South Africa, Brazil, Mexico, Spain, France, Germany, Italy, China, Japan, Egypt, Pakistan, Bangladesh, "
          "the Philippines, Australia, Canada; lowercase, voice-typed, Hinglish, romaji). Detector: "
          f"{scrub.detector().mode}. Run `python3 demo/eval/run_eval.py` to reproduce.\n\n| Measure | Result |\n|---|---|"]
    md += summary
    md.append("\n## Every prompt\n\n| Case | Left in the sent text | Sent |\n|---|---|---|")
    for cid, text, sent, leaks, ages, occs, lost, t_ms in rows:
        miss = ", ".join([f"`{x}`" for x in leaks] + [f"age {a}" for a in ages] + [f"job `{o}`" for o in occs]) or "—"
        if lost:
            miss += " · lost: " + ", ".join(f"`{x}`" for x in lost)
        md.append(f"| {cid} | {miss} | {sent.replace('|', '/')} |")
    (HERE / ("RESULTS.md" if name == "cases" else f"RESULTS-{name}.md")).write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(summary))
    for cid, _, sent, leaks, ages, occs, lost, _ in rows:
        if leaks or ages or occs or lost:
            print(f"  {cid}: leaks={leaks} ages={ages} jobs={occs} lost={lost}\n     -> {sent}")


if __name__ == "__main__":
    main()
