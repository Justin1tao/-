$ErrorActionPreference = 'Stop'

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$targetRoot = Join-Path $codexHome 'skills'
$targetDir = Join-Path $targetRoot 'distilled-cn-life-skill'

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null
if (Test-Path $targetDir) {
  Remove-Item -Recurse -Force $targetDir
}
Copy-Item -Recurse -Force $projectRoot $targetDir

$python = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
  $python = 'python'
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
  $python = 'py'
} else {
  Write-Error '[ERROR] 未找到 Python，请先安装 Python 3.10+。'
  exit 2
}

$verifyOut = Join-Path $env:TEMP 'life_skill_verify.json'
$verifyErr = Join-Path $env:TEMP 'life_skill_verify.err'

& $python -m engine verify 1> $verifyOut 2> $verifyErr
if ($LASTEXITCODE -ne 0) {
  Write-Host '[ERROR] 自检失败，详情：'
  Get-Content $verifyErr
  exit $LASTEXITCODE
}

Write-Host "[OK] 安装完成: $targetDir"
Write-Host "[OK] 版本信息: $(& $python --version)"
Write-Host '[OK] 自检结果:'
Get-Content $verifyOut

Write-Host ''
Write-Host '启动命令（可复制）：'
Write-Host "cd '$targetDir'; $python -m engine verify"
Write-Host '排查文档: https://github.com/Justin1tao/被蒸馏的中国人的一生#troubleshooting'
