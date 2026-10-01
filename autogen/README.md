# Autogen Studio

Install by `pip install -U autogenstudio`
- bin path
  - linux `$HOME/.local/bin`
  - Windows (powershell) `(Split-Path (Get-Command python).Source) + '\Scripts'`

Run by `autogenstudio ui --host 0.0.0.0`
- `--appdir` defaults to
  - Windows: `$env:USERPROFILE\.autogenstudio`
  - Linux: `$HOME/.autogenstudio`
- global configs (e.g. Gallery:Models) stored in `--appdir`
- `--port` defaults to 8081



Agent
- **Tools**: 每个 Agent 可以绑定一组 Python 函数，称为工具（tools）
  - 工具通常封装一些底层逻辑，例如数据库查询、外部 API 访问、数据处理等
- Options
  - *Reflect on Tool Use*: agent 在执行任务后对*工具使用效果*进行反思
