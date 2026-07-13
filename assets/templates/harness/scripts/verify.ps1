#Requires -Version 5.1
<#
.SYNOPSIS
  Thin wrapper around verify.py (prefer Python directly).
#>
param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
)
$ErrorActionPreference = "Stop"
Push-Location $Root
try {
  & python (Join-Path $PSScriptRoot "verify.py")
  exit $LASTEXITCODE
} finally {
  Pop-Location
}
