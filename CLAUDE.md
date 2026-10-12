# Working with Claude Code

Full project context lives in [`docs/brief.md`](docs/brief.md) — read that
first. These are the standing rules for every session in this repo.

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
- **I commit my own work.** Claude may stage and describe changes, but I write and run the actual `git commit` for code I wrote.
