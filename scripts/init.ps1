#Requires -Version 5.1
<#
.SYNOPSIS
  Thin wrapper: prefer `python -m engineering_harness init` or `scripts\eh.cmd init`.
#>
param(
  [Parameter(Mandatory = $true)]
  [string]$TargetPath,

  [ValidateSet("Light", "Standard", "Full")]
  [string]$Level = "Standard",

  [string]$ProjectName = "",

  [switch]$Force
)

$FrameworkRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$launcher = Join-Path $FrameworkRoot "eh.cmd"
if (Test-Path $launcher) {
  $pyArgs = @("init", $TargetPath, "--level", $Level)
  if (-not [string]::IsNullOrWhiteSpace($ProjectName)) {
    $pyArgs += @("--name", $ProjectName)
  }
  if ($Force) {
    $pyArgs += "--force"
  }
  & $launcher @pyArgs
  exit $LASTEXITCODE
}

$env:PYTHONPATH = "$(Join-Path $FrameworkRoot 'src');$env:PYTHONPATH"
$pyArgs = @("init", $TargetPath, "--level", $Level)
if (-not [string]::IsNullOrWhiteSpace($ProjectName)) {
  $pyArgs += @("--name", $ProjectName)
}
if ($Force) {
  $pyArgs += "--force"
}
& python -m engineering_harness @pyArgs
exit $LASTEXITCODE
