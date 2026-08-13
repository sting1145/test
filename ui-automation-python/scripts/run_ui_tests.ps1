param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$PytestArgs
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$RunId = Get-Date -Format "yyyyMMdd_HHmmss"
$CreatedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$RunDir = Join-Path $Root "reports\runs\$RunId"
$ResultsDir = Join-Path $RunDir "allure-results"

New-Item -ItemType Directory -Path $ResultsDir -Force | Out-Null

$env:ALLURE_RESULTS_DIR = $ResultsDir
$env:CURRENT_RUN_ID = $RunId
$env:TEST_SUITE = "ui"

Write-Host "===== UI Tests | Run ID: $RunId ====="
Write-Host "Results dir: $ResultsDir"
Write-Host ""

$pytestArgs = @("-m", "ui and not positive", "--alluredir=$ResultsDir") + $PytestArgs
& .\.venv\Scripts\pytest.exe @pytestArgs
$exitCode = $LASTEXITCODE

$resultFiles = Get-ChildItem $ResultsDir -Filter "*-result.json" -ErrorAction SilentlyContinue
$passed = 0
$failed = 0
$broken = 0
foreach ($file in $resultFiles) {
  $json = Get-Content $file.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
  switch ($json.status) {
    "passed" { $passed++ }
    "failed" { $failed++ }
    "broken" { $broken++ }
  }
}
$total = $resultFiles.Count
$status = if ($failed -eq 0 -and $broken -eq 0) { "passed" } elseif ($passed -gt 0) { "partial" } else { "failed" }

$meta = @{
  runId = $RunId
  createdAt = $CreatedAt
  suite = "ui"
  resultsDir = $ResultsDir
  reportDir = (Join-Path $RunDir "allure-report")
  total = $total
  passed = $passed
  failed = $failed
  broken = $broken
  status = $status
  hasReport = $false
  exitCode = $exitCode
}
$metaJson = $meta | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText((Join-Path $RunDir "meta.json"), $metaJson, [System.Text.UTF8Encoding]::new($false))
Set-Content (Join-Path $Root "reports\latest.txt") $RunId -Encoding ASCII -NoNewline

& .\.venv\Scripts\python.exe scripts\build_report_index.py

Write-Host ""
Write-Host "Run archived: reports\runs\$RunId"
exit $exitCode
