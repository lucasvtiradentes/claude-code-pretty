run:
	bash claude-pretty.sh -p "$$(cat test-prompt.md)"

debug:
	claude --print --verbose --dangerously-skip-permissions --model claude-sonnet-4-20250514 \
		--output-format stream-json --include-partial-messages \
		-p "$$(cat test-prompt.md)" 2>&1 | tee debug-output.jsonl | \
		jq -c 'select(.type == "assistant" and (.message.content[]? | select(.type == "tool_use" and .name == "Task"))) | {type, tool_ids: [.message.content[] | select(.type == "tool_use") | {name, id}]}' || true
	@echo ""
	@echo "--- user tool_result messages ---"
	@jq -c 'select(.type == "user" and .message.content[0].type == "tool_result") | {tool_use_id: .message.content[0].tool_use_id, keys: (. | keys)}' debug-output.jsonl || true
