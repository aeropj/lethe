# bitchat — architecture, and what Lethe should borrow

Checked 2026-10-01. Sources: the repo README and `WHITEPAPER.md`, Trail of Bits' review, reporting on
Alex Radocea's impersonation finding.

## What bitchat is

Jack Dorsey's open-source messenger with **no accounts, no phone numbers and no servers**. Phones talk
over a Bluetooth LE mesh, and over Nostr relays when they need internet reach.

## How it works

| Layer | What it does | Specifics |
|---|---|---|
| Transports | Two transports behind one `Transport` interface, coordinated by a `MessageRouter` | BLE mesh locally; Nostr relays (440+) for global reach |
| Identity | No account. Each device holds two Keychain keys | Curve25519 static key for Noise, Ed25519 for signing. Peer ID = first 8 bytes of SHA-256 of the static key |
| Encryption | Noise `XX` for live sessions, with forward secrecy | Curve25519 / ChaCha20-Poly1305 / SHA-256. Offline mail uses one-way Noise `X`, **no forward secrecy** |
| Relaying | Every phone relays for everyone else | TTL 7; capped at 5 in dense graphs. Random **10–220 ms** delay before each retransmit |
| Padding | Encrypted packets padded to fixed buckets | **256 / 512 / 1024 / 2048 bytes**, PKCS#7. Other packet types are *not* padded and leak size |
| Store-and-forward | Couriers carry sealed mail for offline peers | 100 messages per peer, 24 h TTL, up to 8 retries. Recipient tags are HMAC-derived and **rotate daily** |
| Abuse limits | Quotas instead of identity | Favourites may deposit 5 envelopes, verified strangers 2, into a bounded pool |
| Dedup | Seen-set | LRU of 1000 entries, 5-minute expiry |
| Nostr | Fresh keypair per location channel | Timestamps randomised ±15 minutes |
| Panic | Triple-tap wipes everything | Identity keys, favourites, carried mail, outbox, history, metrics |

## Where it went wrong

- **Identity authentication was broken at launch.** Radocea showed an attacker could impersonate a
  trusted contact; the Noise handshake did not bind keys to identity properly. Fixed within days.
- **Its own whitepaper names metadata as the weakest part.** The peer ID never rotates (only a panic
  wipe changes it), static keys are announced in cleartext, and neighbour lists expose local topology.
- **Partial padding.** Only Noise packets are padded, so every other packet type reveals its size.
- **Claims outran review.** Trail of Bits' point: the code shipped with an honest warning, and was then
  pitched for protests before anyone had reviewed it. "Actions will matter more than promises."

What it got right: everything open, a whitepaper that states plainly what leaks, and fixes shipped in
hours.

## What Lethe should borrow

1. **The crowd is the infrastructure.** In bitchat every phone relays for everyone else. Lethe's pool
   currently leans on commercial relays (Fastly, Cloudflare) — the same company that fronts seven of the
   providers. Members who opt in could carry each other's encrypted requests, so the pool becomes its
   own relay network. Desktop members only, commercial relays as fallback. Later phase, not launch.
2. **Pad everything into fixed buckets.** Bitchat's 256/512/1024/2048 scheme, applied to *every*
   request and every response frame, not just some packet types. That closes the gap bitchat left open
   and the token-length side channel (27% of streamed responses reconstructable unpadded).
3. **Jitter every send.** A random 10–220 ms hold before dispatch, plus a short batching window, breaks
   timing correlation at almost no cost to the user.
4. **Pluggable transports behind one interface.** Same `Transport` and router split: Oblivious HTTP
   first, member relays and Tor later, chosen per provider.
5. **Quotas instead of identity.** Bitchat limits abuse with bounded deposit quotas, not accounts. Our
   rate-limited anonymous tokens are the same idea; it is the answer to "how do you stop abuse without
   knowing who anyone is".
6. **Rotating tags.** Bitchat derives recipient tags by HMAC and rotates them daily. Lethe should derive
   any identifier that must persist (memory scopes, session keys) the same way, and rotate it.
7. **Panic wipe, with one exception.** One action destroys keys, memory and outbox for people. For firms
   it must not touch the compliance ledger, which regulation requires them to keep; there it seals the
   local memory instead.
8. **Publish a whitepaper that says what leaks.** Bitchat's is the right model: it names its own
   weakest point. Ours should state what the provider, the relay and the issuer each still see.

## What Lethe must not copy

- **A stable client identifier on the wire.** Bitchat's never-rotating peer ID is its biggest leak.
  Single-use tokens mean Lethe never has one.
- **Stored data without forward secrecy.** Use a fresh key per request, which Oblivious HTTP already does.
- **Unverified issuer keys.** Bitchat's identity bug has a direct analogue in our design: an issuer could
  hand each member a *different* signing key and use it to tell them apart. Members must check they all
  see the same issuer key, through a published key log. This is a known Privacy Pass problem ("key
  consistency"), and it is the single most important thing to get reviewed.
- **Claims before review.** No "cannot" on the page until an outside firm has audited the protocol.

## Sources

- Repo: https://github.com/permissionlesstech/bitchat
- Whitepaper: https://github.com/permissionlesstech/bitchat/blob/main/WHITEPAPER.md
- Trail of Bits, 18 July 2025: https://blog.trailofbits.com/2025/07/18/building-secure-messaging-is-hard-a-nuanced-take-on-the-bitchat-security-debate/
- Impersonation finding, coverage: https://medium.com/coinmonks/jack-dorseys-bitchat-claims-to-be-secure-but-security-experts-say-absolutely-not-42f3c214a62b
