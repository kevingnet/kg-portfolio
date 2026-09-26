# Finds the images/PDFs the site references but that are missing from the repo,
# searches local folders for them by file name, and copies matches into place.
#
# Usage (from the repo root, in PowerShell):
#   powershell -ExecutionPolicy Bypass -File tools\copy_missing_assets.ps1          # dry run
#   powershell -ExecutionPolicy Bypass -File tools\copy_missing_assets.ps1 -Copy    # copy files
param(
  [switch]$Copy,
  [string[]]$SearchRoots = @(
    "$env:USERPROFILE\tools\kg\Jobs",
    "$env:USERPROFILE\Pictures\Screenshots"
  )
)

$repo = Split-Path -Parent $PSScriptRoot

$missing = @(
  'assets/archive/audiotelco/pdf/2-Problem_Evaluation.pdf'
  'assets/archive/audiotelco/pdf/3-Feasibility_Study.pdf'
  'assets/archive/audiotelco/pdf/5-Scope_or_Specifications.pdf'
  'assets/archive/audiotelco/pdf/6-Design.pdf'
  'assets/archive/audiotelco/pdf/Mexicana_-_Appointment_Scheduling_Application.pdf'
  'assets/archive/disney/pdf/Deployer.pdf'
  'assets/archive/electrosonic/pdf/ESCAN.pdf'
  'assets/archive/electrosonic/pdf/ESCAN__copy_.pdf'
  'assets/archive/electrosonic/pdf/Easy_Schedule_User_Guide.pdf'
  'assets/archive/electrosonic/pdf/SiteLinx_User_Guide.pdf'
  'assets/archive/google/pdf/Antaeus_Architecture.pdf'
  'assets/archive/google/pdf/BabelSupportEscalationsCodeRed.pdf'
  'assets/archive/google/pdf/newAViK.pdf'
  'assets/archive/hms/pdf/Input_Validation_Library.pdf'
  'assets/archive/hms/pdf/Input_Validation_Library_1.pdf'
  'assets/archive/hms/pdf/Snort-Zeus_Request_Filtering_Rules.pdf'
  'assets/archive/jakeknows/pdf/Code_Generator_Architecture_and_Features.pdf'
  'assets/archive/jakeknows/pdf/ID_Engine_Mid_Level_Architecture.pdf'
  'assets/archive/jakeknows/pdf/Production_Server_Deployment_Plan.pdf'
  'assets/archive/jakeknows/pdf/Sony_Application_-_Web_Service_Architecture.pdf'
  'assets/archive/jakeknows/pdf/Web_Service_Architecture.pdf'
  'assets/archive/spirent/pdf/Interface_Wrappers.pdf'
  'assets/archive/spirent/pdf/P2-Sal_Interface_Error_Handling.pdf'
  'assets/archive/spirent/pdf/P2-Sal_Interface_Wrappers.pdf'
  'assets/archive/vmware/pdf/GeminiFramework.pdf'
  'assets/archive/voltdelta/pdf/X.25_Module.pdf'
  'assets/images/projects/mafroda/main-display-normal.png'
  'assets/images/projects/mafroda/main-display-status1.png'
  'assets/images/projects/mafroda/maint-outlets-selected.png'
  'assets/images/projects/mafroda/uieditor-color-dialog.png'
  'assets/images/projects/mafroda/uieditor-figma-combination9.png'
  'assets/images/samples/hero.jpeg'
)

# Compare names ignoring case, spaces, underscores, dashes, dots and parentheses,
# so "Antaeus Architecture.pdf" matches "Antaeus_Architecture.pdf".
function Get-Key([string]$name) {
  ($name.ToLower() -replace '[^a-z0-9]', '')
}

Write-Host "Indexing search folders..."
$index = @{}
foreach ($root in $SearchRoots) {
  if (-not (Test-Path $root)) { Write-Host "  (not found: $root)"; continue }
  Get-ChildItem -Path $root -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
    $k = Get-Key $_.Name
    if (-not $index.ContainsKey($k)) { $index[$k] = @() }
    $index[$k] += $_.FullName
  }
}

$found = 0; $notFound = @()
foreach ($rel in $missing) {
  $dest = Join-Path $repo ($rel -replace '/', '\')
  if (Test-Path $dest) { continue }
  $k = Get-Key (Split-Path $rel -Leaf)
  if ($index.ContainsKey($k)) {
    $src = $index[$k][0]
    $found++
    Write-Host "FOUND  $rel"
    Write-Host "       <- $src"
    if ($index[$k].Count -gt 1) { Write-Host "       ($($index[$k].Count) candidates; using the first)" }
    if ($Copy) {
      New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
      Copy-Item -LiteralPath $src -Destination $dest
    }
  } else {
    $notFound += $rel
  }
}

Write-Host ""
Write-Host "$found found, $($notFound.Count) not found."
if ($notFound.Count) {
  Write-Host "Not found (copy these by hand, keeping the exact name and folder):"
  $notFound | ForEach-Object { Write-Host "  $_" }
}
if (-not $Copy -and $found) { Write-Host "`nDry run only. Re-run with -Copy to copy the files." }
