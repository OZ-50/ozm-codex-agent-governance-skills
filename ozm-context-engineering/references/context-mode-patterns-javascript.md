# JavaScript Patterns

Use JavaScript in context-mode when the analysis is easiest to express with native JSON, arrays, regex, or HTTP.

## Good Patterns

- fetch an endpoint, parse JSON, print only findings
- read a saved artifact and extract failures, IDs, counts, or suspicious values
- summarize repeated structures rather than dumping objects
- print concrete evidence such as line numbers, keys, routes, or error codes

## Output Rules

- always `console.log` findings
- print summaries, not raw payloads
- include exact offending values when diagnosing bugs

## Common Uses

- API debugging
- JSON validation
- test-result summarization
- browser snapshot post-processing
- doc indexing follow-up extraction

## Avoid

- dumping entire responses
- printing giant arrays unchanged
- using JS when a saved file plus one shell grep would be simpler
