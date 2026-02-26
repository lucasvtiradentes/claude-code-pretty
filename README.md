# claude-pretty

Pretty formatter for Claude Code's `--output-format stream-json` output.

Transforms raw JSON stream into readable, colorized terminal output with structured tool calls and session info.

## Installation

```bash
pip install claude-pretty
```

Or install from source:

```bash
git clone https://github.com/lucasvtiradentes/cc-utils
cd cc-utils
pip install -e .
```

## Usage

```bash
# Stream mode - run claude with pretty output
claude-pretty -p "explain this code"

# Replay mode - replay a saved session
claude-pretty -f ~/.claude/projects/.../session.jsonl

# Pipe from stdin
cat session.jsonl | claude-pretty -f -

# Show help
claude-pretty --help
```

## Features

- Session info (id, path, model)
- Colorized tool calls by category
- File content preview with line count
- Todo list formatting with checkboxes
- Subagent nesting visualization
- Error highlighting
- Usage stats (duration, cost, tokens, turns)

## Tool Colors

| Color  | Tools                        |
|--------|------------------------------|
| Green  | Read, user prompt            |
| Orange | Write, Edit                  |
| Blue   | Task (subagents)             |
| Yellow | Todo                         |
| Purple | Glob, Grep, Bash, default    |
| Cyan   | Results (→)                  |
| Red    | Errors (✗)                   |

## Environment Variables

| Variable       | Default                      | Description                    |
|----------------|------------------------------|--------------------------------|
| CLAUDE_MODEL   | claude-sonnet-4-20250514     | Model to use                   |

## Output Examples

### Session Header
```
[session]
   id:    88d0ecf7-ec66-451a-aa7a-87d24f8c5641
   path:  ~/.claude/projects/-home-user-project/88d0ecf7.jsonl
   model: sonnet
```

### Tool Calls
```
[Read] /home/user/project/README.md
   (277 lines)
   # Project Title
   ...

[Glob] src/**/*.ts
   → /home/user/project/src/index.ts
   → /home/user/project/src/utils.ts

[Bash] echo "hello"
   → hello

[Task] "analyze the code" (sonnet)
│ ┌───────────────────────────────
│ [Read] /path/to/file.py
│    → file contents...
│ └───────────────────────────────
```

### Todo List
```
[Todo]
   [x] Completed task
   [~] In progress task
   [ ] Pending task
```

### Summary
```
[done] 32.0s, $0.0935, 2 turns, 45903 in / 136 out
```

## Requirements

- Python 3.9+
- claude CLI (Claude Code)

## License

MIT

## Development

```bash
make install      # setup venv + install deps
make test         # run pytest
make check        # ruff lint
make format       # ruff format
make build        # build wheel
```

```bash
# dev alias
ln -sf $(pwd)/.venv/bin/claude-pretty ~/.local/bin/claude-pretty-dev
```