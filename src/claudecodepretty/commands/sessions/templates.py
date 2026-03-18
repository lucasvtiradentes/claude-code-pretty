SESSIONS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>claude-code-pretty sessions</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #1a1b26;
    color: #a9b1d6;
    font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', 'Consolas', monospace;
    font-size: 13px;
    line-height: 1.6;
    display: flex;
    height: 100vh;
  }
  .sidebar {
    width: 280px;
    min-width: 280px;
    background: #16161e;
    border-right: 1px solid #24283b;
    overflow-y: auto;
    padding: 16px 0;
  }
  .sidebar h2 {
    color: #7aa2f7;
    font-size: 14px;
    font-weight: 600;
    padding: 0 16px 12px;
    border-bottom: 1px solid #24283b;
    margin-bottom: 8px;
  }
  .project-item {
    padding: 8px 16px;
    cursor: pointer;
    border-left: 3px solid transparent;
    transition: background 0.15s;
  }
  .project-item:hover { background: #1a1b26; }
  .project-item.active {
    background: #1a1b26;
    border-left-color: #7aa2f7;
  }
  .project-item.current .project-name::after {
    content: ' (current)';
    color: #9ece6a;
    font-size: 11px;
  }
  .project-name {
    color: #c0caf5;
    font-size: 13px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .project-count {
    color: #565f89;
    font-size: 11px;
  }
  .main {
    flex: 1;
    overflow-y: auto;
    padding: 24px 32px;
  }
  .main h1 {
    color: #7aa2f7;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 4px;
  }
  .main .path {
    color: #565f89;
    font-size: 12px;
    margin-bottom: 20px;
  }
  .session-list { list-style: none; }
  .session-item {
    padding: 12px 16px;
    border: 1px solid #24283b;
    border-radius: 6px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
  }
  .session-item:hover {
    border-color: #7aa2f7;
    background: #1e2030;
  }
  .session-meta {
    display: flex;
    gap: 16px;
    margin-bottom: 4px;
    font-size: 12px;
  }
  .session-date { color: #7aa2f7; }
  .session-size { color: #565f89; }
  .session-id { color: #565f89; font-size: 11px; }
  .session-preview {
    color: #a9b1d6;
    font-size: 13px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 600px;
  }
  .session-preview.loading { color: #565f89; font-style: italic; }
  .empty {
    color: #565f89;
    padding: 40px 0;
    text-align: center;
  }
</style>
</head>
<body>
<div class="sidebar">
  <h2>Projects</h2>
  <div id="project-list"></div>
</div>
<div class="main">
  <div id="content">
    <div class="empty">Select a project</div>
  </div>
</div>
<script>
let projects = [];
let activeProject = null;

async function init() {
  const resp = await fetch('/api/projects');
  projects = await resp.json();
  renderProjects();
  const current = projects.find(p => p.is_current);
  if (current) selectProject(current.folder);
  else if (projects.length > 0) selectProject(projects[0].folder);
}

function renderProjects() {
  const el = document.getElementById('project-list');
  el.innerHTML = projects.map((p, i) => `
    <div class="project-item ${p.is_current ? 'current' : ''} ${p.folder === activeProject ? 'active' : ''}"
         data-folder="${attr(p.folder)}">
      <div class="project-name">${esc(p.name)}</div>
      <div class="project-count">${p.sessions.length} session${p.sessions.length !== 1 ? 's' : ''}</div>
    </div>
  `).join('');
  el.querySelectorAll('.project-item').forEach(item => {
    item.addEventListener('click', () => selectProject(item.dataset.folder));
  });
}

function selectProject(folder) {
  activeProject = folder;
  renderProjects();
  const project = projects.find(p => p.folder === folder);
  if (!project) return;
  const el = document.getElementById('content');
  if (project.sessions.length === 0) {
    el.innerHTML = '<div class="empty">No sessions</div>';
    return;
  }
  el.innerHTML = `
    <h1>${esc(project.name)}</h1>
    <div class="path">${esc(project.path)}</div>
    <ul class="session-list">
      ${project.sessions.map(s => `
        <li class="session-item" data-file="${attr(s.file)}">
          <div class="session-meta">
            <span class="session-date">${esc(s.date)}</span>
            <span class="session-size">${esc(s.size)}</span>
            <span class="session-id">${esc(s.id.substring(0, 8))}</span>
          </div>
          <div class="session-preview loading" data-file="${attr(s.file)}">loading...</div>
        </li>
      `).join('')}
    </ul>
  `;
  el.querySelectorAll('.session-item').forEach(item => {
    item.addEventListener('click', () => {
      window.open('/session?file=' + encodeURIComponent(item.dataset.file), '_blank');
    });
  });
  el.querySelectorAll('.session-preview[data-file]').forEach(loadPreview);
}

async function loadPreview(el) {
  const file = el.dataset.file;
  try {
    const resp = await fetch('/api/preview?file=' + encodeURIComponent(file));
    const data = await resp.json();
    el.textContent = data.preview || '(no preview)';
    el.classList.remove('loading');
  } catch {
    el.textContent = '(no preview)';
    el.classList.remove('loading');
  }
}

function esc(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

function attr(s) {
  return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

init();
</script>
</body>
</html>"""
