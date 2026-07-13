#Requires -Version 5.1
<#
.SYNOPSIS
  Compatibility wrapper — prefer root eh.cmd / eh.ps1
#>
param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$CliArgs
)
$ErrorActionPreference = "Stop"
& (Join-Path $PSScriptRoot "..\eh.ps1") @CliArgs
exit $LASTEXITCODE
