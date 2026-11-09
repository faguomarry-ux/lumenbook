$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    $files = @(
        'lumenbook.cls', 'lumen-style.sty', 'lumen-margins.sty',
        'lumen-math.sty', 'lumen-code.sty', 'lumen-fonts.sty', 'lumen-mark.sty',
        'lumen-study.sty', 'main.tex',
        'demo-screen.tex', 'demo-print.tex', 'latexmkrc', '.gitignore', '.gitattributes',
        'README.md', 'SOURCES.md', 'VALIDATION.md', 'LICENSE',
        'examples', 'scripts', 'tests', 'output', 'fonts'
    )
    New-Item -ItemType Directory -Force -Path dist | Out-Null
    Compress-Archive -LiteralPath $files -DestinationPath dist/lumenbook-starter.zip -Force
    Write-Host 'Created dist/lumenbook-starter.zip'
} finally {
    Pop-Location
}
