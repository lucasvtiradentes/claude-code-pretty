# claude-code-pretty

Pretty formatter for Claude Code - stream sessions in real-time or replay saved .jsonl files.

<div align="center">
   <img src=".github/images/demo.png" width="70%">
</div>

## Features

- stream mode    - run claude with pretty output in real-time
- replay mode    - replay saved .jsonl session files
- tool display   - formatted output for Glob, Grep, Bash, Read, Edit, etc.
- markdown       - renders **bold** and `code` with ANSI styles
- subagent depth - visual indentation for nested Task calls
- cost tracking  - shows duration, cost, tokens per session

## Installation

```bash
pip install claude-code-pretty
```

Aliases: `claudep`, `ccp`, `claude-code-pretty`

## Usage

```bash
# stream mode - run claude with pretty output
claudep -p "explain this code"

# replay mode - replay a saved session
claudep -f ~/.claude/projects/.../session.jsonl
```

Stream mode runs claude with these flags automatically:
```
--print --verbose --dangerously-skip-permissions --output-format stream-json --include-partial-messages
```

## Environment

| Variable                 | Default | Description                         |
|--------------------------|---------|-------------------------------------|
| CP_TOOL_RESULT_MAX_CHARS | 300     | Max chars for tool results (0=hide) |
| CP_READ_PREVIEW_LINES    | 5       | Lines to preview from Read (0=hide) |

## Development

```bash
make install      # setup venv + install
make test         # run pytest
make check        # ruff lint

# dev alias
ln -sf $(pwd)/.venv/bin/claudep ~/.local/bin/claudepd
```

## License

MIT
