# Kalkan

Kalkan is a security layer that sits in front of an LLM: it masks Turkish personal data in
outgoing messages and blocks prompt attacks. Full spec: [SPEC.md](SPEC.md).

## Commands
Run from the repo root, inside the `kalkan` conda env (on Windows, use Anaconda Prompt; plain
PowerShell has no conda init).

```
conda activate kalkan
python -m pytest
ruff check .
ruff format .
```

## Layout
- `src/kalkan/`: the package (src layout).
- `src/kalkan/pii/`: Turkish PII detection (e.g. `tckn.py`).
- `tests/`: pytest tests. The only place pytest collects from.
- `deneyler/`: learning experiments. Not collected by pytest and excluded from ruff.
- `SPEC.md`, `LEARNING_LOG.md`: project spec and learning log (Turkish).

## Rules
a) Never change an expected value in a test on your own. If a test fails, fix the code. If you
   believe the expected value is wrong, stop and ask.
b) Never use real personal data. Tests use only synthetic, algorithm-generated numbers.
c) Never read or commit .env files or secrets.
d) Ask before adding a new dependency.
e) Code, comments and commit messages in English. SPEC.md and LEARNING_LOG.md stay in Turkish.
   Reply to the developer in Turkish, but keep technical terms in English (agent, hook, test, commit).
f) Run python -m pytest and ruff check . after every change.
g) Red-team scope: only public, published attack datasets. Never generate new harmful content.
h) Keep steps small: one feature at a time. Use plan mode before larger changes.
