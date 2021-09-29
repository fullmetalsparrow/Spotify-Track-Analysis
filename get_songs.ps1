<#
	Utilizes the python spotify_dl library to run CLI in order to retrieve playlist songs for the local machine
#>

$currdir = Split-Path -Path $MyInvocation.MyCommand.Path -Parent <# Get current directory #>

<# Create or retrieve default folder path for playlists #>
$folder = Join-Path -Path $currdir -ChildPath "\playlists"
if (Test-Path -Path $folder) {
    cd $folder
} else {
    New-Item -Path $folder -Name "playlists" -ItemType "directory"
    cd $folder
}

<# Ensure PowerShell scripts are enabled as RemoteSigned in order to use venv #>
& ..\venv\Scripts\Activate.ps1
Invoke-Expression "spotify_dl -l $args[0] -o ."