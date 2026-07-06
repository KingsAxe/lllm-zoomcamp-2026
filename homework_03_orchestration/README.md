# Homework 3: AI Orchestration with Kestra

This folder isolates the Week 3 coursework from the Week 1 and Week 2 Qwen-based work already in this repository.

Course source commit:
`9efc9fc756737b0ed776d4876a386dd72b06efc7`

Requirements for running the scored flows:
- Docker Desktop installed and running
- A local `.env` file created from `.env.example`
- A valid Gemini API key for the Gemini-based flows used in the homework

Notes:
- Qwen usage in Weeks 1 and 2 is separate and unchanged by anything in this folder.
- `.env` is local-only and must never be committed.
- The official course flow files are preserved unchanged.
- `flows/4_simple_agent_three_sentences.yaml` is the only local derivative flow, created for the Homework 3 reproducible three-sentence comparison.
- Some preserved stock flows reference additional providers or tools from the course source, such as Tavily or OpenAI. They are kept unchanged for course fidelity.

## Start and stop Kestra

From this folder:

```powershell
docker compose up -d
```

Stop Kestra:

```powershell
docker compose down
```

## Import flows

After Kestra is running, import the YAML files from the UI or with the CLI inside the Kestra container, using the files in `flows/`.

## Homework run guide

Q1:
- Manual comparison only.
- In a private browser window, compare the course prompt in ChatGPT versus Kestra AI Copilot.
- Record only your short observation and selected option in `results.md`.

Q2:
- Import and run `flows/1_chat_without_rag.yaml`.
- Import and run `flows/2_chat_with_rag.yaml`.
- Compare the observed answers for the Kestra 1.1 features question and record the selected option.

Q3:
- Run `flows/4_simple_agent.yaml` with `summary_length = short`.
- Record the `multilingual_agent` output-token count from the execution output.
- Do not guess the answer; use the logged value.

Q4:
- Run the original `flows/4_simple_agent.yaml` with `summary_length = long`.
- Compare the `multilingual_agent` output-token count against Q3 using the actual execution logs.

Q5:
- Run `flows/4_simple_agent_three_sentences.yaml` with `summary_length = long`.
- Compare its `english_brevity` output-token count against the original long-summary run from Q4.
- Use the observed execution logs only.

Q6:
- Conceptual best-practice question only.
- No flow execution is required.

Important:
- Q1 requires a manual private-window ChatGPT vs Kestra Copilot comparison.
- Q3, Q4, and Q5 must be based on observed token counts, not guessed values.
- Docker/Kestra execution for Q2 through Q5 is still pending until you run the flows locally and inspect the actual Kestra logs.
- Keep screenshots, raw logs, API keys, and local absolute paths out of committed files.
