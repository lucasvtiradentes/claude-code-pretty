import json

from claudecodepretty.parser import ParserState, parse_json_line


def test_parse_system_init():
    state = ParserState(mode="stream")
    line = json.dumps(
        {
            "type": "system",
            "subtype": "init",
            "session_id": "abc-123",
            "cwd": "/Users/test/project",
            "model": "claude-sonnet-4-20250514",
        }
    )
    result = parse_json_line(line, state)
    output = result.get_output()

    assert "[session]" in output
    assert "abc-123" in output
    assert "sonnet" in output


def test_parse_tool_use_glob():
    state = ParserState(mode="stream")
    line = json.dumps(
        {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Glob",
                        "input": {"pattern": "*.py"},
                    }
                ]
            },
        }
    )
    result = parse_json_line(line, state)
    output = result.get_output()

    assert "[Glob]" in output
    assert "*.py" in output


def test_parse_tool_use_bash():
    state = ParserState(mode="stream")
    line = json.dumps(
        {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Bash",
                        "input": {"command": "echo hello"},
                    }
                ]
            },
        }
    )
    result = parse_json_line(line, state)
    output = result.get_output()

    assert "[Bash]" in output
    assert "echo hello" in output


def test_parse_todo_write():
    state = ParserState(mode="stream")
    line = json.dumps(
        {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "TodoWrite",
                        "input": {
                            "todos": [
                                {"status": "completed", "content": "item one"},
                                {"status": "in_progress", "content": "item two"},
                                {"status": "pending", "content": "item three"},
                            ]
                        },
                    }
                ]
            },
        }
    )
    result = parse_json_line(line, state)
    output = result.get_output()

    assert "[Todo]" in output
    assert "item one" in output
    assert "item two" in output
    assert "item three" in output


def test_parse_result():
    state = ParserState(mode="stream")
    line = json.dumps(
        {
            "type": "result",
            "is_error": False,
            "duration_ms": 5000,
            "total_cost_usd": 0.05,
            "num_turns": 3,
            "usage": {
                "input_tokens": 1000,
                "output_tokens": 500,
            },
        }
    )
    result = parse_json_line(line, state)
    output = result.get_output()

    assert "[done]" in output
    assert "5.0s" in output
    assert "$0.0500" in output
    assert "3 turns" in output


def test_parse_task_increments_depth():
    state = ParserState(mode="stream")
    line = json.dumps(
        {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Task",
                        "input": {"prompt": "do something", "model": "sonnet"},
                    }
                ]
            },
        }
    )
    parse_json_line(line, state)

    assert state.subagent_depth == 1
    assert "│" in state.sp


def test_replay_mode_shows_user_prompt():
    state = ParserState(mode="replay")
    line = json.dumps(
        {
            "type": "user",
            "message": {
                "content": "Hello, can you help me?",
            },
        }
    )
    result = parse_json_line(line, state)
    output = result.get_output()

    assert "[user]" in output
    assert "Hello" in output


def test_replay_mode_shows_assistant_text():
    state = ParserState(mode="replay")
    line = json.dumps(
        {
            "type": "assistant",
            "message": {
                "content": [
                    {"type": "text", "text": "Sure, I can help!"},
                ],
            },
        }
    )
    result = parse_json_line(line, state)
    output = result.get_output()

    assert "Sure, I can help!" in output
