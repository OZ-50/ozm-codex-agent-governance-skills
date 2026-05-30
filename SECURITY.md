# Security Policy

## Reporting

For security issues, use GitHub private vulnerability reporting if enabled on this repository. If private reporting is not available, open a minimal public issue that does not include exploit payloads, secrets, private paths, or sensitive logs.

## Trust Boundaries

This repository contains agent-facing instructions. Treat README files, `AGENTS.md`, skill files, fixtures, and generated documentation as privileged inputs for AI coding agents.

Do not place secrets, credentials, provider keys, cookies, private session transcripts, personal data, or production logs in this repository.

## Supported Security Posture

This public package is a pre-1.0 reference package. Publication does not prove production readiness, safe execution in every repository, or legal/compliance suitability.

Security-sensitive changes should name:

- affected instruction or script surfaces;
- secret and path handling posture;
- expected negative or misuse case;
- rollback or revert path;
- claim ceiling after the change.

## Out Of Scope

This repository does not provide a hosted runtime, remote execution service, production agent control plane, or commercial SLA.
