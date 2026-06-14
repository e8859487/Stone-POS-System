# Stone POS System — Claude Instructions

## Before Every Push

Always run the test suite before pushing:

```bash
python3 -m pytest tests/ -v
```

All tests must pass before pushing. Do not use `--no-verify` or skip tests.
