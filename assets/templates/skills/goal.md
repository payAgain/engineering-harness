# Goal

`restore → validate one active Goal → resume active Build if present → evaluate gap → replan if needed → containment → issue Build → orchestrator → Accept/commit → evaluate → repeat or stop`

Use Goal G-00x and Build B-00x records. Stop before push, PR, merge, tag, release, protected-branch changes, production, credentials, or any escalation trigger.
