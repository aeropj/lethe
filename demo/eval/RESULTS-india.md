# Detector evaluation

12 prompts in 13 languages and styles (US, UK, India, Nigeria, Kenya, South Africa, Brazil, Mexico, Spain, France, Germany, Italy, China, Japan, Egypt, Pakistan, Bangladesh, the Philippines, Australia, Canada; lowercase, voice-typed, Hinglish, romaji). Detector: GLiNER multilingual PII model + worldwide ID patterns + GeoNames, on device. Run `python3 demo/eval/run_eval.py` to reproduce.

| Measure | Result |
|---|---|
| Identifiers removed (names, places, organisations, contacts, IDs) | **100.0%** (57/57) |
| Prompts with no identifier left | **100.0%** (12/12) |
| Exact adult ages generalised | 100.0% (9/9) |
| Occupations generalised | 100.0% (5/5) |
| Useful terms kept (drugs, schemes, amounts) | 100.0% (33/33) |
| Median / slowest detection time | 336 ms / 712 ms |

## Every prompt

| Case | Left in the sent text | Sent |
|---|---|---|
| in-ltcg-flat | — | Hi, I'm Blair Sutton, 30-something, a tech worker at a big tech company in Maharashtra. My PAN is [PAN removed] and Aadhaar [Aadhaar removed]. I sold my flat in [a place] for 1.2 crore and bought it in 2017 for 68 lakh. Can I save LTCG by buying a new flat under Section 54? Call me on (555) 010-0001 or contact1@example.com. |
| in-hinglish-mf | — | bhai main Rory Ashford hoon, Madhya Pradesh se, age 40-something, kirana store chalata hoon. mera pan [PAN removed] hai. 25 lakh ka mutual fund redeem kiya, kitna tax lagega? |
| in-ltcg-short | — | completely failed, again i am Quinn Whitaker, from Odisha. need to have information about my 40 lakhs ltcg complaince |
| in-80d | — | my name is Marlowe Holloway, 20-something, I work as a healthcare worker at a hospital in Tamil Nadu. my mobile is (555) 010-0001. I want to claim 80D for my parents' health insurance, what is the limit? |
| in-farmer-frozen | — | sir i am Blair Kendrick from Andhra Pradesh, agricultural worker, 50-something years old. my sbi account no [ID number removed] got frozen after i received 3 lakh from my son in United Arab Emirates. what to do? |
| in-esop | — | Hello, this is Marlowe Whitaker from Karnataka. I'm 30-something and a manager at Cinder. My ESOPs worth 18 lakh vested this year, how are they taxed? |
| in-defence-loan | — | im Jordan Merritt, 30-something, public servant posted in Ladakh. my wife Sienna Merritt and I want to buy a house in Uttarakhand for 90 lakh. which home loan is best for defence personnel? |
| in-gst | — | my gst number is [ID number removed] and my shop is in India. I file GSTR-3B monthly. can I switch to quarterly under QRMP? |
| in-family-salary | — | Hey I'm Ellis Ellison, a 20-something year old CA student from Maharashtra. My father Jasper Ellison runs a textile business. Can I be paid salary from his firm and claim it as an expense? |
| in-hinglish-fno | — | mera naam Sage Whitaker hai, Rajasthan mein rehta hoon, 40-something saal ka hoon, CA hoon. mera email contact1@example.com hai. client ka ITR-3 file karna hai, F&O loss carry forward kaise karein? |
| in-nri | — | My UAN is [number removed] and my passport number is [ID number removed]. I'm Rory Ellison, 30-something, moving from Kerala to Ontario. What happens to my EPF and PPF if I become an NRI? |
| in-deposit | — | I live in [street address], Uttar Pradesh. My landlord Mr Sutton refuses to return my 1.5 lakh deposit. What can I do legally? |
