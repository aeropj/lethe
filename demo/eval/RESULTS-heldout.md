# Detector evaluation

30 prompts in 13 languages and styles (US, UK, India, Nigeria, Kenya, South Africa, Brazil, Mexico, Spain, France, Germany, Italy, China, Japan, Egypt, Pakistan, Bangladesh, the Philippines, Australia, Canada; lowercase, voice-typed, Hinglish, romaji). Detector: GLiNER multilingual PII model + worldwide ID patterns + GeoNames, on device. Run `python3 demo/eval/run_eval.py` to reproduce.

| Measure | Result |
|---|---|
| Identifiers removed (names, places, organisations, contacts, IDs) | **100.0%** (104/104) |
| Prompts with no identifier left | **100.0%** (30/30) |
| Exact adult ages generalised | 100.0% (7/7) |
| Occupations generalised | 100.0% (7/7) |
| Useful terms kept (drugs, schemes, amounts) | 94.2% (49/52) |
| Median / slowest detection time | 229 ms / 414 ms |

## Every prompt

| Case | Left in the sent text | Sent |
|---|---|---|
| h-us-custody | — · lost: `family court` | my ex husband Declan Calloway won't let me see our daughter Elise on weekends, we're in Ohio. can i go to Ardent without a lawyer? |
| h-in-salary | — | Hi, I am Emerson Hayes, working as a tech worker at Ardent in [a place], 20-something yrs old, CTC 14 LPA. Should I opt for the new tax regime? |
| h-uk-council | — | Hi, Blair Hayes, 70-something, from [street address]. My council tax went up and I live alone. Am I entitled to single person discount? |
| h-ng-loan | — | abeg i be Kai Hayes, i dey sell phones for Solace, i wan collect loan from my Tamarind, wetin i need? |
| h-br-pix | — · lost: `Pix` | Oi, sou a Emerson Ellison de Minas Gerais, caí num golpe do Saltmarsh, transferi 3 mil reais pra uma conta do Corvid. Meu CPF é [CPF removed]. O que faço? |
| h-de-arbeit | — | Mein Chef Blair Holloway bei Larkspur in Bavaria will mir kündigen, ich bin 50-something und professional. Habe ich Anspruch auf eine Abfindung? |
| h-us-medical-bill | — | I got a $14,200 bill from Kestrel in Arizona after my appendectomy. My insurance member ID is [ID number removed]. How do I dispute it? |
| h-ph-sss | — | good day, im Ellis Pryor from National Capital Region, 40-something years old, a service worker. my sss number is [ID number removed]. how to apply for sss pension loan? |
| h-ca-tenant | — | My landlord, Sloane Whitaker, wants to evict me from [street address] for renovations. I've lived here 11 years. What can I do? |
| h-au-visa | — | I'm Avery Sutton on a 482 visa sponsored by Tamarind in New South Wales. If I resign, how long can I stay? |
| h-ke-mpesa | — | Mtu anaitwa Sloane Ashford alinitumia ujumbe akidai nimeshinda pesa, namba yake ni (555) 010-0001, niko Kenya. ni utapeli? |
| h-fr-caf | — | Bonjour, je m'appelle Avery Sutton, j'habite au [street address] à New Aquitaine, je suis au chômage depuis 3 mois. Ai-je droit au RSA ? |
| h-us-tax-lower | — | im a tech worker in Texas, made about 85k last year, my wife Iris is a teacher at Solace. can we file jointly and deduct my home office? |
| h-in-property | — | My father Bennett Pryor passed away in Rajasthan leaving a flat at [street address]. My brother Emmett refuses to sign. How do we transfer the property? |
| h-mx-imss | — | me llamo Avery Brooks, tengo 30-something años, trabajo de professional en el Solace, mi curp es [ID number removed]. puedo pedir licencia de maternidad? |
| h-za-matric | — · lost: `engineering` | My son Ezra Merritt wrote matric at Halcyon last year and got a bachelor pass. Can he apply to Larkspur for tech worker? My email is contact1@example.com |
| h-uk-nhs-lower | — | my gp dr Merritt at Halcyon in England won't refer me for an mri. my nhs number [ID number removed]. can i self refer? |
| h-es-hipoteca | — | Soy Marlowe Sutton, vivo en [street address], mi DNI es [ID number removed]. ¿Me conviene una hipoteca fija o variable? |
| h-jp-english | — | My name is Marlowe Brooks, I teacher at a high school in Hokkaido. My visa is sponsored by the Kestrel. Can I switch jobs? |
| h-crypto-wallet | — | a guy called Avery Langley on telegram ([handle removed]) took 2 eth from my wallet [wallet removed]. can police trace it? i'm in Colorado |
| h-it-pensione | — | Mi chiamo Quinn Kendrick, ho 60-something anni, sono stato professional alla Bramble per 30-something anni. Quando posso andare in pensione? |
| h-pk-hindi-urdu | — | mera naam Parker Ashford hai, main Sindh mein [a place] mein rehti hoon, mere shohar Blair ko naukri se nikal diya. kya hum zakat le sakte hain? |
| h-us-school-email | — | Write an contact1@example.com to Mrs. Ashford, my son Rhys's teacher at Tamarind, saying he'll miss school Friday for a dentist appointment. |
| h-in-hinglish-health | — | meri mummy Kai Brooks ko sugar hai, umar 60-something, hum Uttar Pradesh mein hain, unka phone [number removed]. kya woh roza rakh sakti hain? |
| h-employer-review | — | My manager Reese Merritt at Solace gave me a bad performance review after I reported harassment by Sloane Calloway. Is this retaliation? |
| h-plain-1 | — | Explain how compound interest works with a simple example. |
| h-plain-2 | — | What are the symptoms of vitamin D deficiency? |
| h-plain-3 | — | Translate 'good morning, how are you?' into Spanish and Hindi. |
| h-plain-4 | — | Is a big tech company stock a good long-term investment compared to an S&P 500 index fund? |
| h-plain-5 | — | Summarise the main causes of World War I in five bullet points. |
