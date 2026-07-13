# Generic agent adapter

Any coding agent that can read repository files can use Engineering Harness.

## Minimal instruction

```text
Read PROTOCOL.md (or harness/PROTOCOL.md). Follow AGENTS.md.
Use agents/*.md as role definitions and skills/*.md as procedures.
Persist all durable state into the repository. Do not rely on chat memory.
```

## Required capabilities

- Read/write project files
- Run shell commands for harness_check / verify when available
- Ability to delegate work to a separate role instance when forced-delegation rules apply
  (exact mechanism is tool-specific and optional adapters may document it)
