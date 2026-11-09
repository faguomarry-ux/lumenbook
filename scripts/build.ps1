param(
    [ValidateSet('xelatex', 'lualatex')]
    [string]$Engine = 'xelatex',
    [switch]$Check
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    $buildDirectory = if ($Engine -eq 'xelatex') { 'build' } else { 'build/lua' }
    New-Item -ItemType Directory -Force -Path $buildDirectory | Out-Null
    $targets = @('main.tex', 'demo-screen.tex', 'demo-print.tex', 'examples/minimal-chinese.tex',
        'examples/annotations.tex', 'examples/study-tools.tex', 'examples/pde-cover.tex')
    if ($Check) {
        $targets += @('tests/features.tex', 'tests/features-screen.tex', 'tests/long-content.tex',
            'tests/fonts-code.tex', 'tests/portable-fonts.tex',
            'tests/annotations-print.tex', 'tests/annotations-long.tex',
            'tests/study-hidden.tex', 'tests/study-nohints.tex', 'tests/study-refs.tex')
    }
    foreach ($target in $targets) {
        $stem = [System.IO.Path]::GetFileNameWithoutExtension($target)
        $transcript = Join-Path $buildDirectory "$stem-build.txt"
        Write-Host "Building $target with $Engine ..."
        & latexmk "-$Engine" "-outdir=$buildDirectory" $target *> $transcript
        if ($LASTEXITCODE -ne 0) {
            Get-Content -LiteralPath $transcript -Tail 45 | Write-Host
            throw "Compilation failed: $target"
        }
        $log = Join-Path $buildDirectory "$stem.log"
        $issues = Select-String -Path $log -Pattern 'Overfull \\[hv]box|Missing character:|LaTeX Error:|undefined references|Font shape .* undefined|multiply defined|destination with the same identifier'
        if ($issues) {
            $issues | ForEach-Object { Write-Host $_.Line }
            throw "Output requires review: $target"
        }
    }
    # Only the recommended XeLaTeX builds replace the published previews.
    if ($Engine -eq 'xelatex') {
        New-Item -ItemType Directory -Force -Path output/pdf | Out-Null
        Copy-Item -LiteralPath build/demo-screen.pdf -Destination output/pdf/lumenbook-screen.pdf
        Copy-Item -LiteralPath build/demo-print.pdf -Destination output/pdf/lumenbook-print.pdf
        Copy-Item -LiteralPath build/annotations.pdf -Destination output/pdf/lumenbook-annotations.pdf
        Copy-Item -LiteralPath build/study-tools.pdf -Destination output/pdf/lumenbook-study-tools.pdf
        Copy-Item -LiteralPath build/pde-cover.pdf -Destination output/pdf/lumenbook-pde-cover.pdf
        Copy-Item -LiteralPath build/main.pdf -Destination output/pdf/lumenbook-pde-notes.pdf
    }
    Write-Host "Build and log checks passed. PDF files: $buildDirectory"
} finally {
    Pop-Location
}
