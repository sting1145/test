param(
  [string]$RunId
)

$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

if (-not $RunId) {
  $latestFile = Join-Path $Root "reports\latest.txt"
  if (-not (Test-Path $latestFile)) {
    throw "未找到最近运行记录，请先执行 run_tests_and_report.bat"
  }
  $RunId = (Get-Content $latestFile -Raw -Encoding UTF8).Trim()
}

$RunDir = Join-Path $Root "reports\runs\$RunId"
$ResultsDir = Join-Path $RunDir "allure-results"
$HtmlReport = Join-Path $RunDir "report.html"
$BuildDir = Join-Path $RunDir "_report_build"
$MetaFile = Join-Path $RunDir "meta.json"

if (-not (Test-Path $ResultsDir)) {
  throw "未找到 Allure 结果目录: $ResultsDir"
}

$ConfigPath = Join-Path $Root "config\allure.json"
$Config = Get-Content $ConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
$AllureBat = Join-Path $Root "tools\allure\allure-2.35.1\bin\allure.bat"

if (-not (Test-Path $AllureBat)) {
  throw "未找到 Allure CLI，请先运行 scripts\install_allure.bat"
}

$java = Get-Command java -ErrorAction SilentlyContinue
if (-not $java) {
  throw "未找到 Java，请安装: winget install Microsoft.OpenJDK.17"
}

Write-Host "Generating single-file HTML report for run: $RunId"
& $AllureBat generate $ResultsDir -o $BuildDir --clean --lang $Config.lang --name $Config.reportName --single-file
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$builtHtml = Join-Path $BuildDir "index.html"
if (-not (Test-Path $builtHtml)) {
  throw "Report file not generated: $builtHtml"
}

[System.IO.File]::Copy($builtHtml, $HtmlReport, $true)
Remove-Item $BuildDir -Recurse -Force -ErrorAction SilentlyContinue

$LatestReport = Join-Path $Root "reports\latest-report.html"
[System.IO.File]::Copy($HtmlReport, $LatestReport, $true)

if (Test-Path $MetaFile) {
  & .\.venv\Scripts\python.exe -c @"
import json
from pathlib import Path
p = Path(r'$MetaFile')
meta = json.loads(p.read_text(encoding='utf-8-sig'))
meta['hasReport'] = True
meta['htmlReport'] = r'$HtmlReport'
p.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
"@
}

& .\.venv\Scripts\python.exe scripts\build_report_index.py

Write-Host ""
Write-Host "HTML report: $HtmlReport"
Write-Host "Latest shortcut: reports\latest-report.html"
Write-Host "History index: reports\index.html"
