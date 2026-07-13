#Requires -Version 5.1
<#
.SYNOPSIS
  Optional editable install: pip install -e .
#>
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
python -m pip install -e .
Write-Host ""
Write-Host "Install OK. Try: eh --version"
Write-Host "Or without install: .\eh.cmd --version"
