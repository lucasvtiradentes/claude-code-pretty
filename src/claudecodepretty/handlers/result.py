from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_result(data: dict, state: ParserState, result: ParseResult):
    r = state.renderer

    while state.subagent_depth > 0:
        result.add(f"{state.sp}{r.section_close()}\n")
        state.decrement_depth()

    if data.get("is_error"):
        error_msg = data.get("result", "unknown error")
        result.add(f"\n{r.red(f'[error] {error_msg}')}\n")
    else:
        duration_ms = data.get("duration_ms", 0)
        duration = f"{duration_ms / 1000:.1f}"
        cost = f"{data.get('total_cost_usd', 0):.4f}"
        turns = data.get("num_turns", 0)
        usage = data.get("usage", {})
        input_tokens = sum(
            [
                usage.get("input_tokens", 0),
                usage.get("cache_read_input_tokens", 0),
                usage.get("cache_creation_input_tokens", 0),
            ]
        )
        output_tokens = usage.get("output_tokens", 0)
        stats = f"{duration}s, ${cost}, {turns} turns, {input_tokens} in / {output_tokens} out"
        result.add(f"\n{r.dim(f'[done] {stats}')}\n")
