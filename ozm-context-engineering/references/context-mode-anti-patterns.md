# Anti-Patterns

Avoid these when using context-mode:

- dumping raw large outputs instead of printing findings
- calling browser tools without `filename`
- re-indexing content that already entered context
- piping giant shell output through `head` and losing the rest
- analyzing data in Bash when structured parsing is needed
- using inline `content` parameters for large payloads when `path` works
- forgetting that stdout is the only thing that enters context from analysis code
