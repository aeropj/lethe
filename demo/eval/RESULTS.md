# Detector evaluation

45 prompts in 13 languages and styles (US, UK, India, Nigeria, Kenya, South Africa, Brazil, Mexico, Spain, France, Germany, Italy, China, Japan, Egypt, Pakistan, Bangladesh, the Philippines, Australia, Canada; lowercase, voice-typed, Hinglish, romaji). Detector: GLiNER multilingual PII model + worldwide ID patterns + GeoNames, on device. Run `python3 demo/eval/run_eval.py` to reproduce.

| Measure | Result |
|---|---|
| Identifiers removed (names, places, organisations, contacts, IDs) | **98.3%** (174/177) |
| Prompts with no identifier left | **95.6%** (43/45) |
| Exact adult ages generalised | 100.0% (9/9) |
| Occupations generalised | 100.0% (10/10) |
| Useful terms kept (drugs, schemes, amounts) | 98.8% (80/81) |
| Median / slowest detection time | 101 ms / 427 ms |

## Every prompt

| Case | Left in the sent text | Sent |
|---|---|---|
| in-tax-voice | — | I. Um, I i'm Rory Brooks i need advice on my on saving my income tax and i also want to route my my indian income into foreign investment opportunity through lrs i based out of Gujarat and i am 60-something years old I am a teacher. |
| us-health | — | My son Felix Kendrick, 9, has ADHD. Should he switch from Adderall to Vyvanse? We're on an HMO in California. Reach me at contact1@example.com. |
| ng-admission | — · lost: `medicine` | hey so my daughter Freya Ellison got rejected from Bramble, we live in Nigeria, my number is (555) 010-0001. what can she do |
| br-tax | — | My name is Blair Whitaker, I work at a large bank in Brazil and my CPF is [CPF removed]. Can I deduct my kids' school fees? |
| uk-landlord | — | need help writing a complaint to my landlord mr. Ellison about mould at [street address], England [postcode] |
| ca-leave | — | my wife Freya Langley is 30-something and pregnant, we're in British Columbia, she works as a healthcare worker at [a place]. is parental leave paid? |
| in-hinglish | — | mera naam Blair Langley hai, main Maharashtra mein rehta hoon, mera PAN [PAN removed] hai aur phone (555) 010-0001 |
| us-job-offer | — | I'm Marlowe Hayes, a tech worker at a big tech company in Washington. I got an offer from Ardent for $310k. Should I negotiate? My manager is Avery Kendrick. |
| de-visa | — | Hallo, ich heiße Parker Pryor, wohne in der [street address], [postcode]. Wie verlängere ich meine Aufenthaltserlaubnis? |
| fr-medical | — | bonjour, je suis Avery Ashford, 40-something ans, professional à Auvergne-Rhône-Alpes. Mon médecin le Dr Holloway m'a prescrit du lévothyrox, est-ce compatible avec l'ibuprofène ? |
| es-divorce | — | Me llamo Jordan Merritt, vivo en [street address], Spain, mi teléfono es [SIN removed]. ¿Cómo pido la custodia de mi hijo Parker? |
| mx-loan | — | soy Marlowe Hayes de Jalisco, trabajo en Ombella-M'Poko y quiero un préstamo de 200 mil pesos, mi rfc es [ID number removed] |
| ke-school | — | My son Tobias Kendrick is in form 3 at a school in Kiambu County. His fees are 45,000 shillings per term. Is there a bursary he can apply for? Call me on (555) 010-0001. |
| za-ubuntu | — | Rory Brooks here from Gauteng, I'm 50-something and work as a service worker at Corvid. My ID number is [number removed]. Can I claim UIF after being retrenched? |
| ph-ofw | — | hi im Kai Calloway, a healthcare worker in United Arab Emirates, originally from Central Visayas. how do i send money to my mom in Central Visayas cheaper? my gcash is (555) 010-0001 |
| pk-business | — | Assalam o alaikum, I am Kai Holloway, I run a textile shop in Punjab near Clock Tower. My CNIC is [ID number removed]. How do I register for FBR tax filer status? |
| bd-garment | — | my sister Delia Langley works in a garment factory in Dhaka Division and her supervisor Sage is harassing her. what are her rights? |
| cn-chinese | — | 我叫Blair，住在Shanghai，在a big tech company工作，手机号(555) 010-0001。请问个人所得税怎么申报？ |
| jp-romaji | — | Kai Calloway, Japan ni sunde imasu. I work at a big tech company and I'm 30-something. how do I file my nenkin? |
| au-centrelink | — | G'day, Kai Sutton from Victoria, 60-something, professional. My Centrelink CRN is [ID number removed]. Am I eligible for the pension supplement? |
| us-ssn-lower | — | my ssn is [SSN removed] and my bank account at a large bank is [number removed], can someone open a credit card in my name? |
| uk-nhs | — | My NHS number is [NHS number removed] and my GP is Dr Hayes at Cinder. Can I get a referral to a different hospital? |
| card-iban | — | Please check if this transfer looks fraudulent: from [IBAN removed] to my card [card number removed], amount 2,300 euros. |
| aadhaar | — | my aadhaar is [Aadhaar removed] and pan is [PAN removed], i live at [street address], Maharashtra [postcode]. how to link them? |
| handle-url | — | someone is impersonating me on instagram, my handle is [handle removed] and the fake one is [handle removed].kapoor.official. my email contact1@example.com. what do i do |
| dob | — | I was born on [birth date] in Kerala. My passport expires next month, can I renew it from Ontario? |
| common-word-names | `hope`, `will` | Rory Ellison Finley and will are getting married, and Marlowe is the professional. what should i say in my toast for hope? |
| single-first-name | — | write a sorry text to Jordan, I forgot her birthday again and she's upset |
| therapy | — | I've been seeing my therapist Dr. Merritt at Bramble in Colorado for depression. Can she share notes with my employer, Ardent? |
| student-visa | — | I'm Finley Holloway, a student at the Solace, my study permit number is [ID number removed]. Can I work off campus? |
| legal-dui | — | got a dui last night in California, Rory Whitaker took my license, I'm a service worker for a large retailer or logistics company. will I lose my cdl? |
| elder-care | — | My mother Maeve Langley, 80-something, lives alone in Tamil Nadu. She has early dementia. What home care options are there? Her doctor is Dr. Sutton at Saltmarsh. |
| small-biz | — | We're Corvid, owned by me (Blair Merritt) and my wife Clara, at [street address], Ontario. Can we deduct our new oven? |
| it-mortgage | — | Sono Parker Ellison, ho 20-something anni, lavoro come professional a Lombardy e vorrei un mutuo. Il mio codice fiscale è [ID number removed]. |
| eg-arabic | — | اسمي Reese Langley، أسكن في [a place] بCairo، رقمي (555) 010-0001. كيف أجدد رخصة القيادة؟ |
| kids-school | — | my kids Marlowe and Sage go to a school in [postcode], Marlowe is being bullied by a classmate named Emerson. how should i talk to the principal? |
| car-accident | — | I rear-ended a car on I-35 near Texas, the other driver is Avery Hayes, plate [ID number removed], her insurer is an insurer. What should I tell my insurance? |
| crypto | — | my a crypto exchange account under Sage Ellison got frozen, wallet [wallet removed], I'm in Lesser Poland. how do i appeal? |
| wedding | `Taj Lands End` | Plan a toast for my best friend Reese Brooks's wedding to Marlowe Merritt on June 14 at the Taj Lands End, Maharashtra. I've known him since Meridian. |
| landlord-email | — | Draft an email to my landlord Mr. Hayes (contact1@example.com) asking him to fix the boiler at [street address], Central and Western before winter. |
| pension | — | I worked 22 years at the a large bank in Uttar Pradesh and retired at 50-something as a manager. My PPO number is [number removed]. How is my family pension calculated? |
| plain-question | — | What is the difference between a Roth IRA and a traditional IRA? |
| plain-code | — | Write a python function that returns the nth fibonacci number using memoization. |
| plain-health | — | Is it safe to take ibuprofen and paracetamol together for a fever? |
| plain-lowercase-finance | — | what is the difference between a roth ira and a traditional ira? which is better for a 30-something year old? |
