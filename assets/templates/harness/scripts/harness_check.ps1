#Requires -Version 5.1
<#
.SYNOPSIS
  Thin wrapper around harness_check.py (prefer Python directly).
#>
param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
)
$ErrorActionPreference = "Stop"
& python (Join-Path $PSScriptRoot "harness_check.py") --root $Root
exit $LASTEXITCODE
