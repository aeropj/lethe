# Detector evaluation

30 prompts in 13 languages and styles (US, UK, India, Nigeria, Kenya, South Africa, Brazil, Mexico, Spain, France, Germany, Italy, China, Japan, Egypt, Pakistan, Bangladesh, the Philippines, Australia, Canada; lowercase, voice-typed, Hinglish, romaji). Detector: GLiNER multilingual PII model + worldwide ID patterns + GeoNames, on device. Run `python3 demo/eval/run_eval.py` to reproduce.

| Measure | Result |
|---|---|
| Identifiers removed (names, places, organisations, contacts, IDs) | **100.0%** (104/104) |
| Prompts with no identifier left | **100.0%** (30/30) |
| Exact adult ages generalised | 100.0% (7/7) |
| Occupations generalised | 100.0% (7/7) |
| Useful terms kept (drugs, schemes, amounts) | 96.2% (50/52) |
| Median / slowest detection time | 87 ms / 131 ms |

## Every prompt

| Case | Left in the sent text | Sent |
|---|---|---|
| h-us-custody | — | my ex husband Theo Pryor won't let me see our daughter Hazel on weekends, we're in Ohio. can i go to family court without a lawyer? |
| h-in-salary | — | Hi, I am Rory Merritt, working as a tech worker at Meridian in [a place], 20-something yrs old, CTC 14 LPA. Should I opt for the new tax regime? |
| h-uk-council | — | Hi, Finley Kendrick, 70-something, from [street address]. My council tax went up and I live alone. Am I entitled to single person discount? |
| h-ng-loan | — | abeg i be Sloane Kendrick, i dey sell phones for Juniper, i wan collect loan from my Tamarind, wetin i need? |
| h-br-pix | — · lost: `Pix` | Oi, sou a Quinn Ellison de Minas Gerais, caí num golpe do Kestrel, transferi 3 mil reais pra uma conta do Juniper. Meu CPF é [CPF removed]. O que faço? |
| h-de-arbeit | — | Mein Chef Parker Pryor bei Juniper in Bavaria will mir kündigen, ich bin 50-something und professional. Habe ich Anspruch auf eine Abfindung? |
| h-us-medical-bill | — | I got a $14,200 bill from Tamarind in Arizona after my appendectomy. My insurance member ID is [ID number removed]. How do I dispute it? |
| h-ph-sss | — | good day, im Reese Brooks from National Capital Region, 40-something years old, a service worker. my sss number is [ID number removed]. how to apply for sss pension loan? |
| h-ca-tenant | — | My landlord, Avery Langley, wants to evict me from [street address] for renovations. I've lived here 11 years. What can I do? |
| h-au-visa | — | I'm Blair Kendrick on a 482 visa sponsored by Ardent in New South Wales. If I resign, how long can I stay? |
| h-ke-mpesa | — | Mtu anaitwa Quinn Merritt alinitumia ujumbe akidai nimeshinda pesa, namba yake ni (555) 010-0001, niko Kenya. ni utapeli? |
| h-fr-caf | — | Bonjour, je m'appelle Rory Hayes, j'habite au [street address] à New Aquitaine, je suis au chômage depuis 3 mois. Ai-je droit au RSA ? |
| h-us-tax-lower | — | im a tech worker in Texas, made about 85k last year, my wife Delia is a teacher at Kestrel. can we file jointly and deduct my home office? |
| h-in-property | — | My father Rowan Whitaker passed away in Rajasthan leaving a flat at [street address]. My brother Rhys refuses to sign. How do we transfer the property? |
| h-mx-imss | — | me llamo Parker Calloway, tengo 30-something años, trabajo de professional en el Ardent, mi curp es [ID number removed]. puedo pedir licencia de maternidad? |
| h-za-matric | — · lost: `engineering` | My son Callum Merritt wrote matric at Larkspur last year and got a bachelor pass. Can he apply to Kestrel for tech worker? My email is contact1@example.com |
| h-uk-nhs-lower | — | my gp dr Whitaker at Juniper in England won't refer me for an mri. my nhs number [ID number removed]. can i self refer? |
| h-es-hipoteca | — | Soy Rory Pryor, vivo en [street address], mi DNI es [ID number removed]. ¿Me conviene una hipoteca fija o variable? |
| h-jp-english | — | My name is Quinn Ashford, I teacher at a high school in Hokkaido. My visa is sponsored by the Meridian. Can I switch jobs? |
| h-crypto-wallet | — | a guy called Avery Langley on telegram ([handle removed]) took 2 eth from my wallet [wallet removed]. can police trace it? i'm in Colorado |
| h-it-pensione | — | Mi chiamo Reese Calloway, ho 60-something anni, sono stato professional alla Saltmarsh per 30-something anni. Quando posso andare in pensione? |
| h-pk-hindi-urdu | — | mera naam Rory Merritt hai, main Sindh mein [a place] mein rehti hoon, mere shohar Ellis ko naukri se nikal diya. kya hum zakat le sakte hain? |
| h-us-school-email | — | Write an contact1@example.com to Mrs. Sutton, my son Miles's teacher at Juniper, saying he'll miss school Friday for a dentist appointment. |
| h-in-hinglish-health | — | meri mummy Kai Ashford ko sugar hai, umar 60-something, hum Uttar Pradesh mein hain, unka phone [number removed]. kya woh roza rakh sakti hain? |
| h-employer-review | — | My manager Avery Merritt at Larkspur gave me a bad performance review after I reported harassment by Sloane Sutton. Is this retaliation? |
| h-plain-1 | — | Explain how compound interest works with a simple example. |
| h-plain-2 | — | What are the symptoms of vitamin D deficiency? |
| h-plain-3 | — | Translate 'good morning, how are you?' into Spanish and Hindi. |
| h-plain-4 | — | Is a big tech company stock a good long-term investment compared to an S&P 500 index fund? |
| h-plain-5 | — | Summarise the main causes of World War I in five bullet points. |
