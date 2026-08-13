param(
  [string]$RunId
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

if (-not $RunId) {
  $latestFile = Join-Path $Root "reports\latest.txt"
  if (-not (Test-Path $latestFile)) {
    throw "No latest run found. Run tests first."
  }
  $RunId = (Get-Content $latestFile -Raw -Encoding UTF8).Trim()
}

$ResultsDir = Join-Path $Root "reports\runs\$RunId\allure-results"
if (-not (Test-Path $ResultsDir)) {
  throw "Results not found for run: $RunId"
}

$ConfigPath = Join-Path $Root "config\allure.json"
$Config = Get-Content $ConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
$AllureBat = Join-Path $Root "tools\allure\allure-2.35.1\bin\allure.bat"

Write-Host "Starting Allure server for run: $RunId (Ctrl+C to stop)"
& $AllureBat serve $ResultsDir --lang $Config.lang --name $Config.reportName
