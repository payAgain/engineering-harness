#Requires -Version 5.1
<#
.SYNOPSIS
  Root launcher for Engineering Harness CLI (sets PYTHONPATH).
#>
param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$CliArgs
)
$ErrorActionPreference = "Stop"
$FrameworkRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$(Join-Path $FrameworkRoot 'src');$env:PYTHONPATH"
& python -m engineering_harness @CliArgs
exit $LASTEXITCODE
