# claude-pretty

Pretty formatter for Claude Code sessions - works both for real-time streaming and replaying old session files (.jsonl).

## Installation

```bash
pip install claude-pretty
```

## Usage

```bash
# stream mode - run claude with pretty output
claude-pretty -p "explain this code"

# replay mode - replay a saved session
claude-pretty -f ~/.claude/projects/.../session.jsonl
```

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
ln -sf $(pwd)/.venv/bin/claude-pretty ~/.local/bin/claude-pretty-dev
```

## License

MIT
