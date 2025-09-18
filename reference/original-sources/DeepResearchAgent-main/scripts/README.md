# Scripts directory

Canonical test runner

This repository uses `scripts/run_comprehensive_tests.py` as the canonical, consolidated test and validation runner. It provides flags to run:

- `--unit-only` - run unit tests
- `--integration-only` - run integration tests
- `--app-only` - run application-level checks and smoke tests

Policy and guidance

- Small, one-off Python test scripts should delegate to `run_comprehensive_tests.py` rather than implementing standalone runners. See `smoke_logger.py` which now delegates to the comprehensive runner.
- Larger, specialized scripts (such as `test_migration.py` and `validate_migration.py`) remain in this directory because they implement comprehensive suites not currently covered by the runner. If you want these checks integrated into `run_comprehensive_tests.py`, I can either:
  - fold their logic into the runner as optional phases (preferred), or
  - keep them as archived/legacy scripts under `scripts/legacy/` and provide stubs that forward to the runner.

How to run the canonical runner

```bash
# From repository root
uv run python scripts/run_comprehensive_tests.py --app-only
# or run the full suite
uv run python scripts/run_comprehensive_tests.py
```

If you'd like, I can now:

- Fold `test_migration.py` and/or `validate_migration.py` into `run_comprehensive_tests.py` as optional phases (I will prepare a proposal and implement it), or
- Move large legacy scripts into `scripts/legacy/` and leave small stubs in place. 

Tell me which approach you prefer and I'll proceed.