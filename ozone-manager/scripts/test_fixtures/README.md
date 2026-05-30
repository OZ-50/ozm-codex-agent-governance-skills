# OZM Eval Fixture Scripts

This directory contains deterministic negative and smoke fixtures used by `ozm_eval_suite.py`.

Fixture scripts are not normal OZM operators. They create temporary inputs, call the owning validator, and return a narrow pass/fail result for one regression case. Keep new fixtures small, side-effect-local, and listed in `ozone-manager/references/package-manifest.json` when they are executable Python files.
