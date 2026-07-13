#Requires -Version 5.1
<#
.SYNOPSIS
  Thin wrapper: prefer `python -m engineering_harness audit` or `scripts\eh.cmd audit`.
#>
param(
  [Parameter(Mandatory = $true)]
  [string]$TargetPath
)

$ErrorActionPreference = "Stop"
$FrameworkRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$launcher = Join-Path $FrameworkRoot "eh.cmd"
if (Test-Path $launcher) {
  & $launcher audit $TargetPath
  exit $LASTEXITCODE
}
$env:PYTHONPATH = "$(Join-Path $FrameworkRoot 'src');$env:PYTHONPATH"
& python -m engineering_harness audit $TargetPath
exit $LASTEXITCODE
