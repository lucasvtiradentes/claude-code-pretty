SESSION_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #1a1b26;
    color: #a9b1d6;
    font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
    font-size: 13px;
    line-height: 1.6;
    padding: 24px 32px;
  }}
  pre {{
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
  }}
  .bold {{ font-weight: 700; color: #c0caf5; }}
  .dim {{ color: #565f89; }}
  .red {{ color: #f7768e; }}
  .green {{ color: #9ece6a; }}
  .orange {{ color: #e0af68; }}
  .purple {{ color: #bb9af7; }}
  .cyan {{ color: #7dcfff; }}
  .blue {{ color: #7aa2f7; }}
  .yellow {{ color: #e0af68; }}
  code {{
    background: #24283b;
    color: #c0caf5;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: inherit;
  }}
  .header {{
    border-bottom: 1px solid #24283b;
    padding-bottom: 16px;
    margin-bottom: 16px;
  }}
  .header h1 {{
    color: #7aa2f7;
    font-size: 16px;
    font-weight: 600;
  }}
  .header .meta {{
    color: #565f89;
    font-size: 12px;
    margin-top: 4px;
  }}
</style>
</head>
<body>
<div class="header">
  <h1>claude-code-pretty</h1>
  <div class="meta">{meta}</div>
</div>
<pre>{content}</pre>
</body>
</html>"""
