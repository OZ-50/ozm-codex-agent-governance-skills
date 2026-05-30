# Discord Community Kit

This kit keeps the OZ-Sir Discord server consistent with the public README and support policy.

## Research Basis

The setup follows Discord's official community-server guidance and online-community research:

- Discord Community servers require safety checks, a rules/guidelines channel, and an updates channel; Community also unlocks onboarding and insights. Source: https://support.discord.com/hc/en-us/articles/360047132851-Enabling-Your-Community-Server
- Discord Onboarding recommends default channels that are useful to most new members and warns against irrelevant default channels. Source: https://support.discord.com/hc/en-us/articles/11074987197975-Community-Onboarding-FAQ
- Server Guide should give new members a welcome sign, 3-5 starter tasks, and resource pages. Source: https://support.discord.com/hc/en-us/articles/13497665141655-Server-Guide-FAQ
- Discord permissions are role-based, category/channel overrides can narrow access, and channel permissions override server permissions. Source: https://support.discord.com/hc/en-us/articles/206029707-Setting-Up-Permissions-FAQ
- Discord role hierarchy and private-channel behavior matter for secure community operations. Source: https://support.discord.com/hc/en-us/articles/214836687-Discord-Roles-and-Permissions
- AutoMod can block risky content and alert moderators; custom keyword matching works across languages, while some built-in filters are English-focused. Source: https://support.discord.com/hc/en-us/articles/4421269296535-AutoMod-FAQ
- Discord voice moderation is harder because voice behavior is ephemeral and evidence is harder to capture. Source: https://arxiv.org/abs/2101.05258
- Research on large newcomer surges suggests communities scale better when administrators are coordinated, norms are shared, and technical moderation systems reduce norm violations. Source: https://www.microsoft.com/en-us/research/publication/surviving-an-eternal-september/
- Newcomer treatment affects retention and contribution quality, so reminders to be considerate should be explicit in welcome/rules text. Source: https://aisel.aisnet.org/misq/vol49/iss2/16/
- Online community design should support both shared identity and individual bonds. Source: https://journals.sagepub.com/doi/abs/10.1177/0170840607076007
- Open-source onboarding benefits from easy, scoped first tasks. Source: https://arxiv.org/abs/1806.02592
- OSS newcomer retention is associated with interaction quality, moderate discussion intensity, and visible project-member participation, so early questions should be routed to human-readable channels rather than buried in many specialized rooms. Source: https://arxiv.org/abs/2603.27136

## Server Positioning

Short description:

> OZ-Sir is the community space for OZM Skills: Codex-native AI coding agent governance, claim ceilings, evidence gates, and AGENTS.md-aware workflows.

Boundary line:

> OZM Skills is a public pre-1.0 governance skill pack, not a production Agent OS, hosted runtime, scheduler, MCP marketplace, or commercial support service.

## Existing Channel Map

Recommended use for the current server structure:

| Channel | Purpose |
| --- | --- |
| `#欢迎-和-规则` | welcome, boundaries, security, and where to ask |
| `#公告` | maintainers only, repository updates and release notes |
| `#综合` | general OZM Skills and AI coding-agent governance discussion |
| `#活动` | reading sessions, review sessions, and live coordination |
| `#想法-和-反馈` | ideas, feedback, docs gaps, governance conflicts |
| voice channels | informal calls only; decisions should be written back to GitHub |

Keep the default channel list small while the community is early. `#欢迎-和-规则`, `#公告`, `#综合`, and `#想法-和-反馈` are enough for a first public pass. Add specialized channels only when repeated traffic proves the need.

## Channel Topics

Use these channel descriptions where Discord exposes a channel topic field:

| Channel | Topic |
| --- | --- |
| `#欢迎-和-规则` | Start here. OZM Skills boundaries, safety rules, GitHub links, and how Discord discussion maps back to repository truth. |
| `#公告` | Maintainer updates for OZM Skills releases, README changes, governance notes, and public repo milestones. |
| `#综合` | General OZM Skills, AI coding agent governance, AGENTS.md, MCP/tool boundary, context engineering, and claim-ceiling discussion. |
| `#活动` | Reading sessions, review sessions, deterministic-check walkthroughs, and community coordination. |
| `#想法-和-反馈` | Focused ideas, docs gaps, confusing rules, weak claim-ceiling language, and feedback for GitHub follow-up. |

## Permission Baseline

Use a conservative permission baseline:

| Surface | `@everyone` | Maintainers / moderators |
| --- | --- | --- |
| `#欢迎-和-规则` | view + read history; no normal posting after seed text | manage/update rules and links |
| `#公告` | view + read history; no normal posting | post announcements |
| `#综合` | view, send, react, thread | moderate |
| `#活动` | view, send, react, thread | moderate |
| `#想法-和-反馈` | view, send, react, thread | moderate |
| voice channels | join/speak for informal calls; avoid treating voice decisions as final | move/mute/deafen when needed |

If Discord Community features are enabled, use Rules Screening for agreement to the boundaries below. Use Server Guide or Onboarding only for the small default channel set; do not expose every specialized channel to new members by default.

Suggested Rules Screening copy:

```text
1. Keep discussion specific, respectful, and evidence-aware.
2. Do not post secrets, cookies, provider keys, private sessions, private logs, exploit payloads, or local machine paths.
3. Discord discussion is not repository truth until converted into tracked GitHub issues, pull requests, releases, or maintainer-reviewed docs.
4. Do not present OZM Skills as a production Agent OS, hosted runtime, scheduler, MCP marketplace, or commercial support SLA.
5. For security issues, use the GitHub security policy and avoid public payload details.
```

Suggested Server Guide tasks:

1. Read `#欢迎-和-规则`.
2. Check the GitHub README and release page.
3. Say hello or ask a scoped question in `#综合`.
4. Put docs gaps or governance feedback in `#想法-和-反馈`.

Suggested AutoMod posture:

- Enable spam/content filters where available.
- Add custom blocked terms only for obvious secret/key leakage or abuse patterns; keep false-positive risk visible.
- Keep moderator alerts private to maintainers/moderators.
- Do not use AutoMod results as repository evidence by themselves.

## Seed Messages

### `#欢迎-和-规则`

```text
Welcome to OZ-Sir.

This server supports OZM Skills: a Codex-native governance skill pack for AI coding agent governance, agentic coding loop control, claim ceilings, evidence gates, and AGENTS.md-aware workflows.

Boundaries:
- OZM Skills is a public pre-1.0 reference package.
- It is not a production Agent OS, hosted runtime, scheduler, MCP marketplace, or commercial support SLA.
- Do not post secrets, cookies, provider keys, private sessions, exploit payloads, private logs, or local machine paths.
- Community discussion is not repository truth until it is converted into tracked GitHub issues, pull requests, releases, or maintainer-reviewed docs.

Links:
- GitHub: https://github.com/OZ-50/ozm-codex-agent-governance-skills
- Discussions: https://github.com/OZ-50/ozm-codex-agent-governance-skills/discussions
- Security policy: https://github.com/OZ-50/ozm-codex-agent-governance-skills/security/policy
```

### `#公告`

```text
OZM Skills public repository is live:
https://github.com/OZ-50/ozm-codex-agent-governance-skills

Scope: Codex-native AI coding agent governance, agentic coding loop control, claim ceilings, evidence gates, reentry rules, context engineering discipline, and AGENTS.md-aware workflows.

Current claim ceiling: artifact-present. The repository publishes the package and supporting docs; it does not claim production readiness, Agent OS completeness, commercial support, improved search ranking, or accepted governance behavior.
```

### `#综合`

```text
Use this channel for general OZM Skills discussion:
- AI coding agent governance
- agentic coding loop boundaries
- claim ceilings and evidence gates
- AGENTS.md instruction surfaces
- MCP/tool-protocol governance boundaries
- context engineering and reentry rules

For reproducible bugs or docs gaps, open a GitHub issue. For broader design questions, GitHub Discussions is easier to preserve and cite.
```

### `#活动`

```text
Use this channel for lightweight coordination:
- README or skill review sessions
- paper/reference reading sessions
- governance checklist walkthroughs
- deterministic-check review sessions

Decisions from activities should be written back to GitHub as issues, pull requests, docs, or release notes before they become repository truth.
```

### `#想法-和-反馈`

```text
Share focused feedback here:
- unclear README or AGENTS.md wording
- weak claim-ceiling language
- missing evidence or check surfaces
- confusing skill boundaries
- ideas for examples or docs

Please include the affected file or section when possible. Do not include secrets, private logs, local absolute paths, or screenshots with sensitive information.
```
