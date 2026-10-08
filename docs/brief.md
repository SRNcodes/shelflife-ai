# ShelfLife AI — Project Brief

Handoff brief for building this project. Read the whole thing before starting. This file lives at `docs/brief.md` in the repo.

## About me

- Srithan Nalla, UW Informatics & Data Science student (class of 2028), Seattle.
- Experience: SWE intern at FlintLab (device test infra, Ubuntu, test scripts), CV/ML undergrad researcher at UW ARC Lab (Python inference pipeline), React bug fixing at Bloomz, Python/Scilab sim work at Robodub.
- Comfortable with: Python, Java, C++, SQL, TypeScript, React, Next.js, FastAPI, Postgres, MongoDB, Docker, Linux, Claude API, basic RAG.
- Goal: a portfolio project for internship recruiting that shows production-grade engineering, not just a tutorial app. It will appear on my personal portfolio site.
- **I'm building this to learn.** I need to be able to explain every core design decision and line of core logic in an interview.

## Working with Claude Code (read before writing any code)

Tooling in this repo:
- **Superpowers plugin**: use `brainstorming` and `writing-plans` for design and planning. Use `test-driven-development` for core logic: Claude writes the failing tests, I write the code that makes them pass.
- **Karpathy guidelines plugin**: think before coding, simplicity first, surgical changes, goal-driven execution.

Rules (these override plugin defaults):
- **I write the core logic myself.** That means the Pydantic schemas, the extraction prompt and Claude API call, the parsed-item → pantry-row mapping (including expiration math), abbreviation learning, the eval/accuracy script, and the agent tools. For these, Claude provides stubs with signatures, docstrings, `raise NotImplementedError`, and tests, not implementations, unless I explicitly ask.
- **Do not run `subagent-driven-development` or `executing-plans` on core-logic tasks.** Claude may fully implement boilerplate: project config, ruff/black, `.env.example`, Docker Compose, SQLAlchemy/Alembic wiring, FastAPI app setup and CORS, Next.js scaffolding.
- **Never rewrite, reformat, or "improve" code I wrote** unless I ask. Point out bugs or concerns instead.
- **Explain design choices in 1–2 sentences** as you make them, so I can talk about them in interviews.
- Use a current Claude model (not retired 3.x model strings), the async Anthropic client (`AsyncAnthropic`) in async FastAPI routes, and a `max_tokens` large enough for long receipts.
- Keep secrets in `.env`, never committed.

## The problem

Groceries go bad before I use them, and I lose track of what I bought and when. I also want to see how much money I'm wasting on food.

## Concept

A multimodal food tracker. I upload a photo of a receipt (or groceries), vision AI extracts structured items, each item gets a shelf life, and I get reminders before things expire. An agent suggests meals that use up the soonest-expiring food first.

## What makes it stand out (prioritize these)

Pantry trackers are a common student project. The architecture alone won't stand out; solving the hard parts well will.

1. **Receipt decoding is the star.** Real receipts say things like "GV ORG BNNA 2@.69" or "KS RTSRY CHKN". Reliable extraction is the core problem. That includes:
   - **Weighed items**: "1.23 lb @ $2.99/lb" → decimal quantity plus unit.
   - **Discount, coupon, and instant-savings lines** (e.g., Costco): attach to the item they apply to, or record as receipt-level discounts. They are never pantry items.
   - **Non-food items** (paper towels, detergent): tagged `Household` and excluded from the pantry by default.
2. **Self-checking extraction.** Extract the printed subtotal and total. If the sum of extracted item prices (minus discounts) doesn't match the subtotal within a small tolerance, flag the receipt `needs_review`. This validates LLM output without a human.
3. **Eval set with published numbers.** Collect 30–50 of my own receipts, hand-label them, and measure field-level accuracy (item name, category, quantity, unit, price) plus subtotal-match rate. Compare prompts and models. Put results in the README, e.g., "item extraction: 94% accuracy, $0.003/receipt".
4. **Learned store abbreviations.** When I correct a parsed item, save the mapping per store so future receipts from that store improve. Measure the effect in the eval: accuracy before vs. after learned mappings.
5. **Observability.** Log tokens, latency, and cost per receipt.
6. **"$ wasted this month."** Items marked `wasted` roll up into a money-wasted stat. This is the hook for the portfolio card.
7. **Use-it-up agent.** Instead of a SQL recipe matcher, a Claude tool-use agent with tools like `get_pantry`, `get_expiring_items`, and `mark_item` that suggests meals prioritizing soonest-expiring items.

## Tech stack

| Area | Choice |
| --- | --- |
| Frontend | Next.js (web app; phone camera upload works fine). React Native/Expo later only if needed for push. |
| API | FastAPI, Pydantic for strict schema validation of LLM output |
| Vision / LLM | Claude vision with structured output. Start with forced tool use (`tool_choice`). Check the current Claude API docs for native structured outputs and compare both approaches in the eval. |
| Models to compare | Claude Haiku 4.5 (cheap baseline) vs. Claude Sonnet 5.5 vs. Gemini Flash, on accuracy, latency, and cost per receipt. Verify current model names and prices in the docs before running evals. |
| Database | PostgreSQL + SQLAlchemy + Alembic migrations. Index on `(user_id, expiration_date, status)`. |
| Async jobs | Redis + Celery (or RQ). Upload returns `202 Accepted` with a job ID; worker does extraction. |
| Scheduler | Celery Beat or APScheduler: daily idempotent job for items expiring in 1–3 days |
| Notifications | Email or web push first; Expo Push / FCM if going native |
| Caching | Redis for USDA shelf-life lookup tables |
| Testing / CI | pytest with DB fixtures, GitHub Actions running lint (ruff/black) + tests on every PR, target 80%+ coverage |
| Deploy | Docker Compose (API, worker, Postgres, Redis); deploy to Render or AWS (EC2 + RDS + S3) |

## Data model (starting point)

- `users`
- `receipts` / `receipt_jobs`: image URL, store, purchase date, **subtotal, tax, total**, **status (`processing`, `parsed`, `needs_review`, `confirmed`, `failed`)**, model used, prompt version, raw model output, input/output tokens, latency, cost
- `receipt_discounts`: receipt_id, raw_text, amount, optional pantry_item_id it applies to
- `pantry_items`: name, raw_text, category, **quantity (decimal), unit (`each`, `lb`, `oz`, `kg`, `g`, …)**, price, purchased_at, expiration_date, status (`active`, `consumed`, `expired`, `wasted`)
- `store_abbreviations`: store, raw_text, corrected_name, category (unique on store + raw_text)
- `shelf_life_rules`: category → days (seeded from USDA FoodKeeper data)

Notes:
- `price` is the line total paid; keep unit price separately if the receipt shows it.
- Use `NUMERIC` for money and weights, never float.

## Eval set format

- `evals/receipts/<id>.jpg`: **redacted** receipt image
- `evals/labels/<id>.json`: ground truth: store, date, subtotal, total, and items (raw_text, name, category, quantity, unit, price), plus discount lines
- `evals/run_eval.py`: runs a model + prompt version over the set and writes a results table: per-field accuracy, subtotal-match rate, avg tokens, latency, cost per receipt
- Results go in `evals/results/` and the best numbers go in the README.

## Privacy and security

- **Redact receipt images before committing** to the public repo: card last-4 digits, loyalty/member IDs, cashier names, barcodes, and anything else identifying. Keep originals out of git (`.gitignore`).
- **Protect the live demo.** A public upload button spends my API key. Require auth and rate-limit uploads per user, and offer a **demo mode** with preloaded sample receipts so recruiters can try it without uploading. Set a spending limit on the API key.
- API keys and DB credentials only in environment variables.

## Build plan

**Week 1: Rough end-to-end version (no infra yet).**
Upload a receipt → Claude extracts items → show an editable list → save to Postgres → one reminder works. Ugly is fine. The goal is a working loop. Use decimal quantity + unit from day one so the schema doesn't need rework.

**Phase 2: Extraction quality.**
Pydantic schemas, subtotal self-check and `needs_review` flow, discount and non-food handling, store abbreviation learning, USDA shelf-life mapping, the eval set (redacted) and accuracy script, model/prompt comparisons, cost/latency logging.

**Phase 3: Async + scheduling.**
Move extraction to a Redis-backed worker queue, add the daily expiration job, notifications, item status updates, and the "$ wasted" stat.

**Phase 4: Agent + polish + deploy.**
Use-it-up meal agent with tool use, GitHub Actions CI, test coverage, Docker Compose, auth + rate limiting + demo mode, deployment, and a README with architecture diagram, eval results, and a demo GIF.

## Deliverables for the portfolio

- Live demo link (with demo mode)
- Demo GIF (upload receipt → items appear → agent suggests a meal)
- README: problem, architecture diagram, eval results table (models × prompts), cost per receipt, subtotal-match rate, what I learned

## How I'd like help

Start with Superpowers `brainstorming` on the Week 1 slice using this brief, then `writing-plans`. Follow the "Working with Claude Code" rules above: scaffold the boilerplate, stub the core logic with tests, and explain decisions as we go so I can talk about them in interviews.
