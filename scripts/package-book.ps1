$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$templateRoot = Join-Path $projectRoot 'templates/book'
$stagingRoot = Join-Path $projectRoot ('tmp/book-package/' + [guid]::NewGuid().ToString('N') + '/lumenbook-book')
$archivePath = Join-Path $projectRoot 'dist/lumenbook-book-clean.zip'

# Explicit file lists keep previews, tests, fonts and intermediate output out.
$runtimeFiles = @(
    'lumenbook.cls', 'lumen-style.sty', 'lumen-cover.sty',
    'lumen-fonts.sty', 'lumen-margins.sty', 'lumen-math.sty',
    'lumen-code.sty', 'lumen-mark.sty', 'lumen-study.sty',
    'latexmkrc', 'LICENSE'
)
$writingFiles = @(
    'main.tex', 'book-info.tex', 'chapters/01-introduction.tex',
    'README.md', 'SOURCES.md', '.gitignore'
)
New-Item -ItemType Directory -Force -Path $stagingRoot | Out-Null
foreach ($relativePath in $runtimeFiles) {
    Copy-Item -LiteralPath (Join-Path $projectRoot $relativePath) -Destination $stagingRoot
}
foreach ($relativePath in $writingFiles) {
    $destination = Join-Path $stagingRoot $relativePath
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destination) | Out-Null
    Copy-Item -LiteralPath (Join-Path $templateRoot $relativePath) -Destination $destination
}
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $archivePath) | Out-Null
Add-Type -AssemblyName System.IO.Compression.FileSystem
if (Test-Path -LiteralPath $archivePath) {
    Remove-Item -LiteralPath $archivePath
}
[System.IO.Compression.ZipFile]::CreateFromDirectory(
    $stagingRoot, $archivePath, [System.IO.Compression.CompressionLevel]::Optimal, $true
)
Write-Host "Created $archivePath"
Write-Host ('Source files: ' + ($runtimeFiles.Count + $writingFiles.Count))
