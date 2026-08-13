param(
  [string]$RunId
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

if (-not $RunId) {
  $latestShortcut = Join-Path $Root "reports\latest-report.html"
  if (Test-Path $latestShortcut) {
    Start-Process $latestShortcut
    exit 0
  }

  $latestFile = Join-Path $Root "reports\latest.txt"
  if (-not (Test-Path $latestFile)) {
    throw "No latest run found."
  }
  $RunId = (Get-Content $latestFile -Raw -Encoding UTF8).Trim()
}

$HtmlReport = Join-Path $Root "reports\runs\$RunId\report.html"
if (-not (Test-Path $HtmlReport)) {
  Write-Host "HTML report not found, generating ..."
  & (Join-Path $PSScriptRoot "generate_report.ps1") -RunId $RunId
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Start-Process $HtmlReport
