"""生成历史报告索引页 reports/index.html"""
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.report_paths import get_reports_root, get_runs_root


def _load_meta(run_dir: Path) -> dict | None:
  meta_file = run_dir / "meta.json"
  if not meta_file.exists():
    return None
  return json.loads(meta_file.read_text(encoding="utf-8-sig"))


def build_index() -> Path:
  reports_root = get_reports_root()
  runs_root = get_runs_root()
  reports_root.mkdir(parents=True, exist_ok=True)

  runs = []
  if runs_root.exists():
    for run_dir in sorted(runs_root.iterdir(), reverse=True):
      if not run_dir.is_dir():
        continue
      meta = _load_meta(run_dir)
      if meta:
        runs.append(meta)

  rows = []
  for meta in runs:
    run_id = meta["runId"]
    created = meta.get("createdAt", run_id)
    status = meta.get("status", "unknown")
    passed = meta.get("passed", "-")
    failed = meta.get("failed", "-")
    total = meta.get("total", "-")
    has_report = meta.get("hasReport", False)
    report_link = f'runs/{run_id}/report.html'
    report_cell = (
      f'<a href="{report_link}" target="_blank">双击打开报告</a>'
      if has_report and (runs_root / run_id / "report.html").exists()
      else "未生成"
    )
    status_color = "#52c41a" if status == "passed" else "#faad14" if status == "partial" else "#f5222d"

    rows.append(
      f"""
      <tr>
        <td><code>{run_id}</code></td>
        <td>{created}</td>
        <td>{total}</td>
        <td style="color:#52c41a">{passed}</td>
        <td style="color:#f5222d">{failed}</td>
        <td style="color:{status_color}">{status}</td>
        <td>{report_cell}</td>
      </tr>
      """
    )

  latest_link = ""
  if (reports_root / "latest-report.html").exists():
    latest_link = '<p class="tip"><strong>最新报告：</strong><a href="latest-report.html" target="_blank">reports/latest-report.html</a>（双击即可打开）</p>'

  html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>测试报告历史记录</title>
  <style>
    body {{ font-family: "Microsoft YaHei", sans-serif; margin: 24px; background: #f5f7fa; }}
    h1 {{ color: #1f2d3d; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #e8e8e8; padding: 10px 12px; text-align: left; }}
    th {{ background: #4472C4; color: #fff; }}
    tr:nth-child(even) {{ background: #fafafa; }}
    .tip {{ color: #666; margin: 12px 0 20px; }}
    a {{ color: #1677ff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>熊猫掌柜 UI 自动化 - 历史测试报告</h1>
  {latest_link}
  <p class="tip">每次执行测试后会归档到 <code>reports/runs/运行编号/</code>，可直接双击 HTML 文件查看，无需命令行。</p>
  <table>
    <thead>
      <tr>
        <th>运行编号</th>
        <th>执行时间</th>
        <th>总用例</th>
        <th>通过</th>
        <th>失败</th>
        <th>结果</th>
        <th>报告</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows) if rows else '<tr><td colspan="7">暂无历史记录，请先运行 run_tests_and_report.bat</td></tr>'}
    </tbody>
  </table>
  <p class="tip">生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</body>
</html>
"""

  index_file = reports_root / "index.html"
  index_file.write_text(html, encoding="utf-8")
  return index_file


if __name__ == "__main__":
  path = build_index()
  print(f"已更新历史索引: {path}")
