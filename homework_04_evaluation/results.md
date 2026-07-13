# Homework 4 Results

This file is a compact summary of verified Homework 4 outputs only. It excludes secrets, raw API payloads, local absolute paths, and large execution logs.

| Question | Exact result | Selected option |
|---|---|---|
| Q1 | Average input tokens = 1189.6666666666667 | 1400 |
| Q2 | `01-agentic-rag/lessons/03-rag.md` | Select the option with `01-agentic-rag/lessons/03-rag.md` |
| Q3 | `01-agentic-rag/lessons/01-intro.md` | Select the option with `01-agentic-rag/lessons/01-intro.md` |
| Q4 | Text-search Hit Rate = 0.7583333333333333 | 0.76 |
| Q5 | Vector-search MRR = 0.5486111111111112 | 0.55 |
| Q6 | Hybrid MRRs: k=1 -> 0.6481944444444449; k=50 -> 0.637916666666667; k=100 -> 0.637916666666667; k=200 -> 0.637916666666667 | 1 |

## Q1 Token Counts

| Filename | Input tokens | Output tokens | Questions generated |
|---|---:|---:|---:|
| `01-agentic-rag/lessons/01-intro.md` | 901 | 143 | 5 |
| `01-agentic-rag/lessons/02-environment.md` | 1125 | 150 | 5 |
| `01-agentic-rag/lessons/03-rag.md` | 1543 | 134 | 5 |

## Notes

- Q1 stores only token counts and the final average.
- Q2 and Q3 store filenames only.
- Q4 through Q6 store aggregated evaluation metrics only.
