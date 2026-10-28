# Verify it on OpenAI's side

The demo shows you what it sends. This guide shows you how to confirm, from OpenAI's own records, that
OpenAI received stand-ins and never your real names, places or IDs.

**What this proves.** The text OpenAI received and stored.
**What this POC cannot prove.** Network anonymity. Here the gateway runs on your machine with your key, so
OpenAI sees your organisation, project, key and IP. In production the gateway runs at Lethe with Lethe's
pooled key, behind a relay run by someone else.

## 1. Make a dedicated project and key

So Logs and Usage show only this demo.

1. Go to [platform.openai.com](https://platform.openai.com). In the project picker at the top left, choose
   **Create project** and name it `lethe-demo`.
2. With `lethe-demo` selected, open [API keys](https://platform.openai.com/api-keys), click
   **Create new secret key**, pick project `lethe-demo`, and copy the key.
3. Optional: set a low monthly budget for the project under its **Limits** settings.

## 2. Run with verification mode on

Verification mode sends `"store": true`, which tells OpenAI to keep each request for up to 30 days so you
can inspect it. It is on by default. Every request shows `"store": true` in the trace.

```bash
./demo/run.sh
```

Open http://localhost:8787, paste the `lethe-demo` key, leave **Verification mode** on, and press
**Connect**. The key stays in the server's memory only. To skip the key screen, pass it as a preset
instead: `OPENAI_API_KEY=sk-… ./demo/run.sh`, or put it in
`demo/.env`.

The server listens on localhost only. It spends your key and has no login, so do not expose it.

## 3. Ask, and note the two IDs

Press **Ask privately**, then **Open trace**. The trace's "Prove it" panel shows, each with a copy button:

- `resp_…`: the response ID. This is how you look the request up.
- `req_…`: the request ID from OpenAI's `x-request-id` header. OpenAI support uses it to find one call.

The server also logs both for every request, in the terminal where `run.sh` is running:

```
[gateway] credential ok · gpt-5.6-luna · response resp_0313b5… · request req_cdf884… · store=True
```

## 4. Check 1: in the app

In the trace's "Prove it" panel press **Verify with OpenAI** (the Lab card on the Ask page has the same
check). The server calls OpenAI's `GET /v1/responses/{id}/input_items` and shows exactly the input OpenAI
holds. It then searches that input for every private detail you typed in this chat. You should see:

> 0 of 5 private details found, in the input OpenAI stored for resp_…

with each detail it searched for, and the stand-ins OpenAI holds instead.

## 5. Check 2: yourself, without the app

The same call from your own terminal, with the same key ("Copy curl" in the trace gives you this line):

```bash
curl -s https://api.openai.com/v1/responses/resp_XXXX/input_items -H "Authorization: Bearer $OPENAI_API_KEY" | python3 -m json.tool
```

Search it for something real you typed. It should print nothing:

```bash
curl -s https://api.openai.com/v1/responses/resp_XXXX/input_items -H "Authorization: Bearer $OPENAI_API_KEY" | grep -i "robert kim"
```

The full record, with model, output and token usage:

```bash
curl -s https://api.openai.com/v1/responses/resp_XXXX -H "Authorization: Bearer $OPENAI_API_KEY" | python3 -m json.tool
```

The output there contains stand-ins too. Your real names were put back only in your browser.

## 6. Check 3: the dashboard

1. Open [Logs → Responses](https://platform.openai.com/logs?api=responses).
2. Select the `lethe-demo` project in the top-left picker. Logs are listed per project.
3. Find the row by its `resp_…` ID or time and open it. **Input** shows the stand-ins.

Logs can take a while to appear. If the list is empty, check the organisation and project selection. An
organisation owner may also need to allow log visibility in the organisation's data-control settings.

## 7. Check 4: usage

Open [Usage](https://platform.openai.com/usage) and filter to project `lethe-demo`. The request count matches
the number of questions you asked. Input and output tokens match the "Tokens" figure in each trace.
Usage also updates with a delay.

## 8. Clean up

Delete a stored response:

```bash
curl -X DELETE https://api.openai.com/v1/responses/resp_XXXX -H "Authorization: Bearer $OPENAI_API_KEY"
```

For normal use turn **Verification mode** off in the key menu (or preset `LETHE_OPENAI_STORE=0`), so
requests carry `"store": false`. OpenAI may still keep
API data for up to 30 days for abuse monitoring
([OpenAI: your data](https://developers.openai.com/api/docs/guides/your-data)), which is why the stand-ins
matter: whatever is kept has no real details in it. "Forget key" in the key menu drops it from the server's memory. Revoke the demo key when you are done.

## What each check proves

| Check | Proves | Does not prove |
|---|---|---|
| In-app button | OpenAI's stored input has no private detail you typed | That the app is honest; use check 2 for that |
| `curl` input_items | The same, straight from OpenAI, with no demo code involved | Anything about identity |
| Dashboard Logs | The same, in OpenAI's own UI | That logs appear instantly |
| Usage | Every request the demo made is accounted for | What was in them |
