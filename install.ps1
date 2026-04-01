if (($IsMacOS) -or ($IsLinux)) {
    $Script:color = "red"
} else {
    $Script:color = "white"
}

Write-Host @"
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣶⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⣀⡀⣠⣾⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⡇⠀⠀⠀⠀
⠀⣶⣿⣦⣜⣿⣿⣿⡟⠻⣿⣿⣿⣿⣿⣿⣿⡿⢿⡏⣴⣺⣦⣙⣿⣷⣄⠀⠀⠀
⠀⣯⡇⣻⣿⣿⣿⣿⣷⣾⣿⣬⣥⣭⣽⣿⣿⣧⣼⡇⣯⣇⣹⣿⣿⣿⣿⣧⠀⠀
⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣷
"@ -ForegroundColor $Script:color
if ($Script:color -eq "red") {
    Write-Host "Bongo Cat is not supported on your platform!"
    Write-Host "But don't worry, I accept PRs that add support for these platforms!"
    return
}
$release = Invoke-RestMethod https://api.github.com/repos/NSPC911/bongo-cat/releases/latest
Write-Host "Downloading $($release.tag_name)"
$arch = (Get-CimInstance -Class Win32_Processor -Property Architecture).Architecture | Select-Object -First 1
switch ($arch) {
    5 { $arch = "arm" }
    9 {
        if ([Environment]::Is64BitOperatingSystem) {
            $arch = "x64"
        } else {
            Write-Host "Bongo Cat is not supported on 32-bit operating systems!"
            return
        }
    }
}
$release.assets | ForEach-Object {
    if ($_.name -eq "bongo-cat-standalone-windows-$arch.zip") {
        $script:toDownload = $_.url
        $script:hash = $_.digest
    }
}
$Script:downloadPath = New-TemporaryFile
Invoke-RestMethod -Uri $script:toDownload -Headers @{ "Accept" = "application/octet-stream" } -OutFile $Script:downloadPath
Write-Host "Verifying download..."
$Script:filehash = Get-FileHash $Script:downloadPath -Algorithm SHA256
$Script:filehash = "sha256:$($Script:filehash.Hash)"
if ($Script:filehash -ne $script:hash) {
    Write-Host "Hash does not match! Download may be corrupted."
    return
}
Write-Host "Extracting..."
# check path first
$script:dest_path = "$HOME/AppData/Local/bongo-cat/"
if (Test-Path $script:dest_path) {
    Write-Host "Bongo Cat is already installed! Do you want to overwrite it? (y/n)"
    while ($true) {
        if ([System.Console]::ReadKey($true).Key -eq "Y") {
            [Console]::SetCursorPosition(0, [Console]::CursorTop - 1)
            Write-Host "Bongo Cat is already installed! Do you want to overwrite it? (y/n)" -ForegroundColor Green
            break
        } else {
            Write-Host "Aborting installation..."
            return
        }
    }
    Remove-Item $script:dest_path -Recurse -Force
}
Expand-Archive $Script:downloadPath -DestinationPath "$HOME/AppData/Local/bongo-cat/"
# create shortcut
$Script:WScriptShell = New-Object -ComObject WScript.Shell
$Script:Shortcut = $WScriptShell.CreateShortcut("$HOME/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Bongo Cat.lnk")
$Script:Shortcut.TargetPath = "$HOME/AppData/Local/bongo-cat/bongocat.exe"
$Script:Shortcut.Save()
Write-Host "Installation complete! You can find Bongo Cat in your Start Menu."
