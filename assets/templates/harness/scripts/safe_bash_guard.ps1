#Requires -Version 5.1
<#
.SYNOPSIS
  Thin wrapper around safe_bash_guard.py (prefer Python directly).
#>
param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$CommandParts
)
$ErrorActionPreference = "Stop"
$parts = @($CommandParts)
if ($parts.Count -gt 0 -and $parts[0] -eq "--") {
  $parts = $parts[1..($parts.Count - 1)]
}
& python (Join-Path $PSScriptRoot "safe_bash_guard.py") -- @parts
exit $LASTEXITCODE
