# Contributing

OZM Skills is a governance skill package. Contributions should improve clarity, safety, evidence discipline, or deterministic checks without weakening claim ceilings or trust boundaries.

Good first contributions:

- clarify a specific skill's activation effect;
- add a source-backed example for correct skill use;
- improve deterministic fixture coverage for a known failure mode;
- tighten overbroad claim wording;
- document a recurring failure family with prevention criteria.

High-risk changes:

- changing `ozone-manager` T0 stops;
- weakening hydration, truth-boundary, dispatch, review, closeout, or claim-ceiling rules;
- adding network, provider, secret, browser, publishing, or hosted-runtime assumptions;
- adding broad Agent OS, production-ready, self-evolving, or fully autonomous claims.

Review expectation:

> A skill change is not accepted because it reads well. It needs a clear activation effect, downstream consumer, claim-ceiling effect, and at least one check or review path.

Before submitting a pull request, run relevant local deterministic checks where available and include the exact command outputs or scoped limitations in the PR description.
