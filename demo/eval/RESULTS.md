# Detector evaluation

44 prompts in 13 languages and styles (US, UK, India, Nigeria, Kenya, South Africa, Brazil, Mexico, Spain, France, Germany, Italy, China, Japan, Egypt, Pakistan, Bangladesh, the Philippines, Australia, Canada; lowercase, voice-typed, Hinglish, romaji). Detector: GLiNER multilingual PII model + worldwide ID patterns + GeoNames, on device. Run `python3 demo/eval/run_eval.py` to reproduce.

| Measure | Result |
|---|---|
| Identifiers removed (names, places, organisations, contacts, IDs) | **98.3%** (174/177) |
| Prompts with no identifier left | **95.5%** (42/44) |
| Exact adult ages generalised | 100.0% (9/9) |
| Occupations generalised | 100.0% (10/10) |
| Useful terms kept (drugs, schemes, amounts) | 98.7% (78/79) |
| Median / slowest detection time | 214 ms / 33506 ms |

## Every prompt

| Case | Left in the sent text | Sent |
|---|---|---|
| in-tax-voice | — | I. Um, I i'm Avery Holloway i need advice on my on saving my income tax and i also want to route my my indian income into foreign investment opportunity through lrs i based out of Gujarat and i am 60-something years old I am a teacher. |
| us-health | — | My son Rowan Langley, 9, has ADHD. Should he switch from Adderall to Vyvanse? We're on an HMO in California. Reach me at contact1@example.com. |
| ng-admission | — · lost: `medicine` | hey so my daughter Sienna Sutton got rejected from Larkspur, we live in Nigeria, my number is (555) 010-0001. what can she do |
| br-tax | — | My name is Avery Hayes, I work at a large bank in Brazil and my CPF is [CPF removed]. Can I deduct my kids' school fees? |
| uk-landlord | — | need help writing a complaint to my landlord mr. Holloway about mould at [street address], England [postcode] |
| ca-leave | — | my wife Esme Ashford is 30-something and pregnant, we're in British Columbia, she works as a healthcare worker at [a place]. is parental leave paid? |
| in-hinglish | — | mera naam Sloane Holloway hai, main Maharashtra mein rehta hoon, mera PAN [ID number removed] (555) 010-0001 |
| us-job-offer | — | I'm Reese Hayes, a tech worker at a big tech company in Washington. I got an offer from Halcyon for $310k. Should I negotiate? My manager is Marlowe Pryor. |
| de-visa | — | Hallo, ich heiße Rory Ashford, wohne in der [street address], [postcode]. Wie verlängere ich meine Aufenthaltserlaubnis? |
| fr-medical | — | bonjour, je suis Parker Merritt, 40-something ans, professional à Auvergne-Rhône-Alpes. Mon médecin le Dr Holloway m'a prescrit du lévothyrox, est-ce compatible avec l'ibuprofène ? |
| es-divorce | — | Me llamo Finley Hayes, vivo en [street address], mi teléfono es [SIN removed]. ¿Cómo pido la custodia de mi hijo Marlowe? |
| mx-loan | — | soy Emerson Calloway de Jalisco, trabajo en Ombella-M'Poko y quiero un préstamo de 200 mil pesos, mi rfc es [ID number removed] |
| ke-school | — | My son Theo Ellison is in form 3 at Meridian in Kiambu County. His fees are 45,000 shillings per term. Is there a bursary he can apply for? Call me on (555) 010-0001. |
| za-ubuntu | — | Parker Ashford here from Gauteng, I'm 50-something and work as a service worker at Ardent. My ID number [ID number removed]. Can I claim UIF after being retrenched? |
| ph-ofw | — | hi im Quinn Hayes, a healthcare worker in United Arab Emirates, originally from Central Visayas. how do i send money to my mom in Central Visayas cheaper? my gcash is (555) 010-0001 |
| pk-business | — | Assalam o alaikum, I am Emerson Langley, I run a textile shop in Punjab near Clock Tower. My CNIC is [ID number removed]. How do I register for FBR tax filer status? |
| bd-garment | — | my sister Juno Calloway works in a garment factory in Dhaka Division and her supervisor Finley is harassing her. what are her rights? |
| cn-chinese | — | 我叫Kai，住在Shanghai，在a big tech company工作，手机号(555) 010-0001。请问个人所得税怎么申报？ |
| jp-romaji | — | Rory Whitaker, Japan ni sunde imasu. I work at a big tech company and I'm 30-something. how do I file my nenkin? |
| au-centrelink | — | G'day, Kai Pryor from Victoria, 60-something, professional. My Centrelink CRN is [ID number removed]. Am I eligible for the pension supplement? |
| us-ssn-lower | — | my ssn is [ID number removed] account at a large bank is [number removed], can someone open a credit card in my name? |
| uk-nhs | — | My NHS number is [NHS number removed] and my GP is Dr Sutton at Juniper. Can I get a referral to a different hospital? |
| card-iban | — | Please check if this transfer looks fraudulent: from [IBAN removed] to my card [card number removed], amount 2,300 euros. |
| aadhaar | — | my aadhaar is [ID number removed]s [PAN removed], i live at [street address]. how to link them? |
| handle-url | — | someone is impersonating me on instagram, my handle is [handle removed] and the fake one is [handle removed].kapoor.official. my email contact1@example.com. what do i do |
| dob | — | I was born on [birth date] in Kerala. My passport expires next month, can I renew it from Ontario? |
| common-word-names | `hope`, `will` | Jordan Calloway Finley and will are getting married, and Parker is the professional. what should i say in my toast for hope? |
| single-first-name | — | write a sorry text to Ellis, I forgot her birthday again and she's upset |
| therapy | — | I've been seeing my therapist Dr. Brooks at Saltmarsh in Colorado for depression. Can she share notes with my employer, Kestrel? |
| student-visa | — | I'm Finley Pryor, a student at the Cinder, my study permit number [ID number removed]. Can I work off campus? |
| legal-dui | — | got a dui last night in California, Emerson Kendrick took my license, I'm a service worker for a large retailer or logistics company. will I lose my cdl? |
| elder-care | — | My mother Margo Pryor, 80-something, lives alone in Tamil Nadu. She has early dementia. What home care options are there? Her doctor is Dr. Hayes at Saltmarsh. |
| small-biz | — | We're Ardent, owned by me (Reese Hayes) and my wife Imogen, at [street address]. Can we deduct our new oven? |
| it-mortgage | — | Sono Sage Holloway, ho 20-something anni, lavoro come professional a [a place] e vorrei un mutuo. Il mio codice fiscale è [ID number removed]. |
| eg-arabic | — | اسمي Sloane Kendrick، أسكن في [street address] بCairo، رقمي [number removed]. كيف أجدد رخصة القيادة؟ |
| kids-school | — | my kids Sloane and Rory go to Kestrel in [postcode], Sloane is being bullied by a classmate named Blair. how should i talk to the principal? |
| car-accident | — | I rear-ended a car on I-35 near Texas, the other driver is Finley Sutton, plate [ID number removed], her insurer is an insurer. What should I tell my insurance? |
| crypto | — | my a crypto exchange account under Reese Calloway got frozen, wallet [wallet removed], I'm in Lesser Poland. how do i appeal? |
| wedding | `Taj Lands End` | Plan a toast for my best friend Marlowe Hayes's wedding to Ellis Ellison on June 14 at the Taj Lands End, Maharashtra. I've known him since Cinder. |
| landlord-email | — | Draft an email to my landlord Mr. Pryor (contact1@example.com) asking him to fix the boiler at [street address] before winter. |
| pension | — | I worked 22 years at the a large bank in Uttar Pradesh and retired at 50-something as a professional. My PPO number [ID number removed]. How is my family pension calculated? |
| plain-question | — | What is the difference between a Roth IRA and a traditional IRA? |
| plain-code | — | Write a python function that returns the nth fibonacci number using memoization. |
| plain-health | — | Is it safe to take ibuprofen and paracetamol together for a fever? |
