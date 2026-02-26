# cc-utils

Pretty formatter for Claude Code's `--output-format stream-json` output.

Transforms raw JSON stream into readable, colorized terminal output with structured tool calls and session info.

```
                Raw JSON Stream                          Pretty Output
┌─────────────────────────────────────┐     ┌─────────────────────────────────────┐
│ {"type":"system","subtype":"init".. │     │ [session]                           │
│ {"type":"stream_event","event":...  │     │    id:    abc123-def456             │
│ {"type":"stream_event","event":...  │ ──► │    path:  ~/.claude/projects/...    │
│ {"type":"user","message":...        │     │    model: sonnet                    │
│ {"type":"result","duration_ms":...  │     │                                     │
└─────────────────────────────────────┘     │ [Read] /path/to/file.md             │
                                            │    (50 lines)                       │
                                            │    # File content preview...        │
                                            │                                     │
                                            │ [done] 5.2s, $0.03, 2 turns         │
                                            └─────────────────────────────────────┘
```

## Features

- Session info (id, path, model)
- Colorized tool calls by category
- File content preview with line count
- Todo list formatting with checkboxes
- Error highlighting
- Usage stats (duration, cost, tokens, turns)

## Tool Colors

| Color  | Tools                        |
|--------|------------------------------|
| Green  | Read                         |
| Orange | Write, Edit                  |
| Blue   | Task (subagents)             |
| Yellow | Todo                         |
| Purple | Glob, Grep, Bash, default    |
| Cyan   | Results (→)                  |
| Red    | Errors (✗)                   |

## Usage

```bash
# Basic usage
./run-claude.sh "your prompt here"

# With custom model
CLAUDE_MODEL=claude-haiku-4-5-20251001 ./run-claude.sh "prompt"

# More file preview lines
FILE_LINES=10 ./run-claude.sh "read large-file.md"

# Longer result truncation
RESULT_LIMIT=500 ./run-claude.sh "prompt"
```

## Environment Variables

| Variable       | Default                      | Description                    |
|----------------|------------------------------|--------------------------------|
| CLAUDE_MODEL   | claude-sonnet-4-20250514     | Model to use                   |
| FILE_LINES     | 5                            | Lines to preview from files    |
| RESULT_LIMIT   | 300                          | Max chars for tool results     |

## Requirements

- bash
- jq
- claude CLI (Claude Code)

## Output Examples

### Session Header
```
[session]
   id:    88d0ecf7-ec66-451a-aa7a-87d24f8c5641
   path:  ~/.claude/projects/-home-user-project/88d0ecf7.jsonl
   model: sonnet
```

### File Read
```
[Read] /home/user/project/README.md
   (277 lines)
   # Project Title

   Description of the project...
   ...
```

### Todo List
```
[Todo]
   [x] Completed task
   [~] In progress task
   [ ] Pending task
```

### Tool Results
```
[Glob] src/**/*.ts
   → /home/user/project/src/index.ts
   → /home/user/project/src/utils.ts
   ...

[Bash] echo "hello"
   → hello

[Task] "what is 2+2?" (haiku)
   → 2 + 2 = 4
```

### Error
```
[Write] /path/to/file.txt
   ✗ File has not been read yet. Read it first before writing to it.
```

### Summary
```
[done] 32.07s, $0.0935, 2 turns, 45903 in / 136 out
```

## How It Works

1. Runs `claude` with `--output-format stream-json --include-partial-messages`
2. Processes each JSON line through `jq`
3. Routes events to appropriate handlers based on type
4. Maintains state to track current tool (for hiding JSON params)
5. Outputs formatted, colorized text

## License

MIT
