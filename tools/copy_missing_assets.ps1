# Finds the images/PDFs the site references but that are missing from the repo,
# searches local folders for them by file name (ignoring spaces, underscores,
# case and, if needed, the extension), and copies matches into place.
# A .doc/.docx/.rtf original is converted to PDF with Microsoft Word.
#
# Usage (from the repo root, in PowerShell):
#   powershell -ExecutionPolicy Bypass -File tools\copy_missing_assets.ps1          # dry run
#   powershell -ExecutionPolicy Bypass -File tools\copy_missing_assets.ps1 -Copy    # copy files
param(
  [switch]$Copy,
  [string[]]$SearchRoots = @(
    "$env:USERPROFILE\tools\kg\KGCodeSamplesWhole",
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
$byName = @{}   # key of full file name (with extension)
$byBase = @{}   # key of name without extension
foreach ($root in $SearchRoots) {
  if (-not (Test-Path $root)) { Write-Host "  (not found: $root)"; continue }
  $n = 0
  Get-ChildItem -Path $root -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
    $n++
    $k = Get-Key $_.Name
    if (-not $byName.ContainsKey($k)) { $byName[$k] = @() }
    $byName[$k] += $_.FullName
    $b = Get-Key $_.BaseName
    if (-not $byBase.ContainsKey($b)) { $byBase[$b] = @() }
    $byBase[$b] += $_.FullName
  }
  Write-Host "  $root : $n files"
}

$word = $null
function Convert-ToPdf([string]$src, [string]$dest) {
  if (-not $script:word) {
    try { $script:word = New-Object -ComObject Word.Application; $script:word.Visible = $false }
    catch { Write-Host "       (Microsoft Word not available; cannot convert)"; return $false }
  }
  try {
    $doc = $script:word.Documents.Open($src, $false, $true)
    $doc.SaveAs([ref]$dest, [ref]17)   # 17 = wdFormatPDF
    $doc.Close($false)
    return $true
  } catch { Write-Host "       (conversion failed: $($_.Exception.Message))"; return $false }
}

$docExt = @('.doc', '.docx', '.rtf', '.odt', '.txt')
$found = 0; $notFound = @()
foreach ($rel in $missing) {
  $dest = Join-Path $repo ($rel -replace '/', '\')
  if (Test-Path $dest) { continue }
  $leaf = Split-Path $rel -Leaf
  $k = Get-Key $leaf
  $b = Get-Key ([IO.Path]::GetFileNameWithoutExtension($leaf))
  $destExt = [IO.Path]::GetExtension($leaf).ToLower()

  $src = $null; $convert = $false
  if ($byName.ContainsKey($k)) {
    $src = $byName[$k][0]
  } elseif ($byBase.ContainsKey($b)) {
    $cands = $byBase[$b]
    $same = $cands | Where-Object { [IO.Path]::GetExtension($_).ToLower() -eq $destExt } | Select-Object -First 1
    $img = $cands | Where-Object { $destExt -ne '.pdf' -and [IO.Path]::GetExtension($_).ToLower() -in @('.png', '.jpg', '.jpeg') } | Select-Object -First 1
    $docSrc = $cands | Where-Object { $destExt -eq '.pdf' -and [IO.Path]::GetExtension($_).ToLower() -in $docExt } | Select-Object -First 1
    if ($same) { $src = $same } elseif ($img) { $src = $img } elseif ($docSrc) { $src = $docSrc; $convert = $true }
  }

  if ($src) {
    $found++
    Write-Host "FOUND  $rel"
    Write-Host "       <- $src$(if ($convert) { '  (will convert to PDF with Word)' })"
    if ($Copy) {
      New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
      if ($convert) { [void](Convert-ToPdf $src $dest) } else { Copy-Item -LiteralPath $src -Destination $dest }
    }
  } else {
    $notFound += $rel
  }
}
if ($word) { $word.Quit() }

Write-Host ""
Write-Host "$found found, $($notFound.Count) not found."
if ($notFound.Count) {
  Write-Host "Not found (copy these by hand, keeping the exact name and folder):"
  $notFound | ForEach-Object { Write-Host "  $_" }
}
if (-not $Copy -and $found) { Write-Host "`nDry run only. Re-run with -Copy to copy the files." }
