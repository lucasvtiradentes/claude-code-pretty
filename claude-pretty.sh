#!/usr/bin/env bash
set -euo pipefail

GREEN=$'\033[32m'
ORANGE=$'\033[33m'
PURPLE=$'\033[35m'
CYAN=$'\033[36m'
BLUE=$'\033[34m'
YELLOW=$'\033[93m'
DIM=$'\033[2m'
RED=$'\033[31m'
RESET=$'\033[0m'
MODEL="${CLAUDE_MODEL:-claude-sonnet-4-20250514}"
RESULT_LIMIT="${RESULT_LIMIT:-300}"
FILE_LINES="${FILE_LINES:-5}"
INDENT="   "

HIDE_TOOLS="Write|TodoWrite|Read|Glob|Grep|Bash|Task|Edit|MultiEdit|NotebookEdit"
CURRENT_TOOL=""
SUBAGENT_DEPTH=0
SP=""

update_sp() {
  SP=""
  for ((i=0; i<SUBAGENT_DEPTH; i++)); do
    SP="${SP}${DIM}│${RESET} "
  done
}

process_json() {
  local line="$1"

  local type
  type=$(echo "$line" | jq -r '.type // empty' 2>/dev/null) || return

  case "$type" in
    system)
      local subtype session_id cwd
      subtype=$(echo "$line" | jq -r '.subtype // empty')
      if [[ "$subtype" == "init" ]]; then
        session_id=$(echo "$line" | jq -r '.session_id')
        cwd=$(echo "$line" | jq -r '.cwd | gsub("/"; "-") | gsub("_"; "-")')
        model_name=$(echo "$line" | jq -r '.model | split("-") | .[1] // .model')
        echo -e "${DIM}[session]"
        echo -e "${INDENT}id:    ${session_id}"
        echo -e "${INDENT}path:  ~/.claude/projects/${cwd}/${session_id}.jsonl"
        echo -e "${INDENT}model: ${model_name}${RESET}"
        echo ""
      fi
      ;;

    stream_event)
      local event_type
      event_type=$(echo "$line" | jq -r '.event.type // empty')

      case "$event_type" in
        content_block_start)
          if [[ $SUBAGENT_DEPTH -gt 0 ]]; then
            echo -e "${SP}${DIM}└───────────────────────────────${RESET}"
            ((SUBAGENT_DEPTH--))
            update_sp
          fi
          local block_type name
          block_type=$(echo "$line" | jq -r '.event.content_block.type // empty')
          if [[ "$block_type" == "tool_use" ]]; then
            name=$(echo "$line" | jq -r '.event.content_block.name')
            CURRENT_TOOL="$name"
            case "$name" in
              Write|TodoWrite|Read|Glob|Grep|Bash|Task|Edit|MultiEdit|NotebookEdit) ;;
              *) echo -ne "\n${SP}${PURPLE}[${name}] " ;;
            esac
          fi
          ;;
        content_block_delta)
          local delta_type
          delta_type=$(echo "$line" | jq -r '.event.delta.type // empty')
          case "$delta_type" in
            text_delta)
              echo -n "$(echo "$line" | jq -rj '.event.delta.text // empty')"
              ;;
            input_json_delta)
              if [[ ! "$CURRENT_TOOL" =~ ^($HIDE_TOOLS)$ ]]; then
                echo -n "$(echo "$line" | jq -rj '.event.delta.partial_json // empty')"
              fi
              ;;
          esac
          ;;
        content_block_stop)
          if [[ ! "$CURRENT_TOOL" =~ ^($HIDE_TOOLS)$ ]]; then
            echo -e "${RESET}"
          fi
          CURRENT_TOOL=""
          ;;
        error)
          echo -e "\n${SP}${RED}[error] $(echo "$line" | jq -r '.event.error // .event | tostring')${RESET}"
          ;;
      esac
      ;;

    user)
      local content_type
      content_type=$(echo "$line" | jq -r '.message.content[0].type // empty')
      if [[ "$content_type" == "tool_result" ]]; then
        local has_file content
        has_file=$(echo "$line" | jq -r 'if .tool_use_result | type == "object" then .tool_use_result.file // empty else empty end' 2>/dev/null)
        if [[ -n "$has_file" && "$has_file" != "null" ]]; then
          local preview num_lines
          num_lines=$(echo "$line" | jq -r '.tool_use_result.file.numLines // 0')
          preview=$(echo "$line" | jq -r --argjson n "$FILE_LINES" '.tool_use_result.file.content | if type == "string" then split("\n") | .[0:$n] | map("'"$INDENT"'" + .) | join("\n") else "'"$INDENT"'" + tostring[0:200] end' 2>/dev/null || echo "${INDENT}(binary/structured content)")
          echo -e "${SP}${DIM}${INDENT}(${num_lines} lines)"
          echo -e "${SP}${preview}"
          [[ "$num_lines" =~ ^[0-9]+$ && $num_lines -gt $FILE_LINES ]] && echo -e "${SP}${INDENT}..."
          echo -e "${SP}${RESET}"
        else
          content=$(echo "$line" | jq -r '.message.content[0].content // "no content"')
          if [[ "$content" =~ ^(Todos\ have\ been|The\ file.*has\ been) ]]; then
            : # hide
          elif [[ "$content" =~ \<tool_use_error\> ]]; then
            local error_msg
            error_msg=$(echo "$content" | sed 's/<[^>]*>//g')
            echo -e "${SP}${RED}${INDENT}✗ ${error_msg}${RESET}\n"
          elif echo "$content" | jq -e 'type == "array"' &>/dev/null; then
            local parsed
            parsed=$(echo "$content" | jq -r 'map(select(.type? == "text") | .text) | first // "" | gsub("<usage>[^<]*</usage>"; "") | gsub("\n"; " ")')
            echo -e "${SP}${CYAN}${INDENT}→ ${parsed:0:$RESULT_LIMIT}${RESET}\n"
          elif [[ "$content" == *$'\n'* ]]; then
            echo "$content" | head -10 | while IFS= read -r l; do
              echo -e "${SP}${CYAN}${INDENT}→ ${l}${RESET}"
            done
            [[ $(echo "$content" | wc -l) -gt 10 ]] && echo -e "${SP}${INDENT}..."
            echo ""
          else
            echo -e "${SP}${CYAN}${INDENT}→ ${content:0:$RESULT_LIMIT}${RESET}\n"
          fi
        fi
      fi
      ;;

    assistant)
      # Handle TodoWrite
      if echo "$line" | jq -e '.message.content[]? | select(.type == "tool_use" and .name == "TodoWrite")' &>/dev/null; then
        echo -e "\n${SP}${YELLOW}[Todo]${RESET}"
        echo "$line" | jq -r --arg g "$GREEN" --arg o "$ORANGE" --arg d "$DIM" --arg r "$RESET" --arg i "$INDENT" --arg sp "$SP" '
          .message.content[] | select(.type == "tool_use" and .name == "TodoWrite") | .input.todos[] |
          $sp + $i + (if .status == "completed" then $g + "[x]" elif .status == "in_progress" then $o + "[~]" else $d + "[ ]" end) + $r + " " + .content
        '
        echo ""
      fi
      # Handle Write
      if echo "$line" | jq -e '.message.content[]? | select(.type == "tool_use" and .name == "Write")' &>/dev/null; then
        local file_path
        file_path=$(echo "$line" | jq -r '.message.content[] | select(.type == "tool_use" and .name == "Write") | .input.file_path')
        echo -e "\n${SP}${ORANGE}[Write] ${file_path}${RESET}"
      fi
      # Handle Read
      if echo "$line" | jq -e '.message.content[]? | select(.type == "tool_use" and .name == "Read")' &>/dev/null; then
        local file_path
        file_path=$(echo "$line" | jq -r '.message.content[] | select(.type == "tool_use" and .name == "Read") | .input.file_path')
        echo -e "\n${SP}${GREEN}[Read] ${file_path}${RESET}"
      fi
      # Handle Glob
      if echo "$line" | jq -e '.message.content[]? | select(.type == "tool_use" and .name == "Glob")' &>/dev/null; then
        local pattern
        pattern=$(echo "$line" | jq -r '.message.content[] | select(.type == "tool_use" and .name == "Glob") | .input.pattern')
        echo -e "\n${SP}${PURPLE}[Glob] ${pattern}${RESET}"
      fi
      # Handle Grep
      if echo "$line" | jq -e '.message.content[]? | select(.type == "tool_use" and .name == "Grep")' &>/dev/null; then
        local pattern path
        pattern=$(echo "$line" | jq -r '.message.content[] | select(.type == "tool_use" and .name == "Grep") | .input.pattern')
        path=$(echo "$line" | jq -r '.message.content[] | select(.type == "tool_use" and .name == "Grep") | .input.path // empty')
        if [[ -n "$path" ]]; then
          echo -e "\n${SP}${PURPLE}[Grep] \"${pattern}\" in ${path##*/}${RESET}"
        else
          echo -e "\n${SP}${PURPLE}[Grep] \"${pattern}\"${RESET}"
        fi
      fi
      # Handle Edit
      if echo "$line" | jq -e '.message.content[]? | select(.type == "tool_use" and (.name == "Edit" or .name == "MultiEdit"))' &>/dev/null; then
        local edit_name edit_file
        edit_name=$(echo "$line" | jq -r '[.message.content[] | select(.type == "tool_use" and (.name == "Edit" or .name == "MultiEdit"))][0].name')
        edit_file=$(echo "$line" | jq -r '[.message.content[] | select(.type == "tool_use" and (.name == "Edit" or .name == "MultiEdit"))][0].input.file_path')
        echo -e "\n${SP}${ORANGE}[${edit_name}] ${edit_file}${RESET}"
      fi
      # Handle NotebookEdit
      if echo "$line" | jq -e '.message.content[]? | select(.type == "tool_use" and .name == "NotebookEdit")' &>/dev/null; then
        local nb_path
        nb_path=$(echo "$line" | jq -r '.message.content[] | select(.type == "tool_use" and .name == "NotebookEdit") | .input.notebook_path')
        echo -e "\n${SP}${ORANGE}[NotebookEdit] ${nb_path}${RESET}"
      fi
      # Handle Bash
      if echo "$line" | jq -e '.message.content[]? | select(.type == "tool_use" and .name == "Bash")' &>/dev/null; then
        local command
        command=$(echo "$line" | jq -r '.message.content[] | select(.type == "tool_use" and .name == "Bash") | .input.command')
        echo -e "\n${SP}${PURPLE}[Bash] ${command}${RESET}"
      fi
      # Handle Task
      if echo "$line" | jq -e '.message.content[]? | select(.type == "tool_use" and .name == "Task")' &>/dev/null; then
        local prompt model
        prompt=$(echo "$line" | jq -r '.message.content[] | select(.type == "tool_use" and .name == "Task") | .input.prompt // .input.description')
        model=$(echo "$line" | jq -r '.message.content[] | select(.type == "tool_use" and .name == "Task") | .input.model // "sonnet"')
        echo -e "\n${SP}${BLUE}[Task] \"${prompt:0:50}\" (${model})${RESET}"
        ((SUBAGENT_DEPTH++))
        update_sp
        echo -e "${SP}${DIM}┌───────────────────────────────${RESET}"
      fi
      ;;

    error)
      echo -e "\n${SP}${RED}[error] $(echo "$line" | jq -r '.error // "unknown error"')${RESET}"
      ;;

    result)
      while [[ $SUBAGENT_DEPTH -gt 0 ]]; do
        echo -e "${SP}${DIM}└───────────────────────────────${RESET}"
        ((SUBAGENT_DEPTH--))
        update_sp
      done
      local is_error
      is_error=$(echo "$line" | jq -r '.is_error')
      if [[ "$is_error" == "true" ]]; then
        echo -e "\n${RED}[error] $(echo "$line" | jq -r '.result // "unknown error"')${RESET}"
      else
        local duration cost turns input_tokens output_tokens
        duration=$(echo "$line" | jq -r '(.duration_ms / 1000 | tostring | .[0:5])')
        cost=$(echo "$line" | jq -r '(.total_cost_usd | tostring | .[0:6])')
        turns=$(echo "$line" | jq -r '.num_turns // 0')
        input_tokens=$(echo "$line" | jq -r '[.usage.input_tokens, .usage.cache_read_input_tokens, .usage.cache_creation_input_tokens] | add // 0')
        output_tokens=$(echo "$line" | jq -r '.usage.output_tokens // 0')
        echo -e "\n${DIM}[done] ${duration}s, \$${cost}, ${turns} turns, ${input_tokens} in / ${output_tokens} out${RESET}"
      fi
      ;;
  esac
}

claude --print --verbose --dangerously-skip-permissions --model "$MODEL" \
  --output-format stream-json --include-partial-messages "$@" | \
while IFS= read -r line; do
  [[ -n "$line" ]] && process_json "$line"
done
