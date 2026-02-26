# claude-code-pretty

Human-readable output for Claude Code. Stream sessions in real-time or replay saved .jsonl files.

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

## Output

```
[session]
   id:    88d0ecf7-ec66-451a-aa7a-87d24f8c5641
   path:  ~/.claude/projects/.../88d0ecf7.jsonl
   model: sonnet

[Glob] *.py
   → main.py
   → utils.py

[Bash] echo "hello"
   → hello

[Todo]
   [x] completed
   [~] in progress
   [ ] pending

[done] 5.2s, $0.03, 2 turns, 1000 in / 200 out
```

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
