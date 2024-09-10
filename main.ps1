[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Set path variables
$pythonExe = "C:\your\python\path\python.exe"
$scriptPath = "C:\your\spider\path\utils"

trap {
    Write-Host "warning: $_"
    exit
}
$choice1 = Read-Host "Enter '1' to start from getting ID or enter '2' to continue from the last download progress`n"
Set-Location $scriptPath
function Validate-Url {
    param (
        [string]$url
    )
    if ($url -match '^(https?|ftp)://[^\s/$.?#].[^\s]*$') {
        return $true
    }
    else {
        return $false
    }
}
if ($choice1 -eq '1') {
    $choice2 = Read-Host "Enter '1' to download using default category`nEnter '2' to download Chinese category`nEnter '3' to download uncensored Chinese category`nEnter '4' to download by using a url`n"
    if ($choice2 -eq '1') {
        & $pythonExe "$scriptPath\get_id.py"
        Start-Sleep -Seconds 3
        & $pythonExe "$scriptPath\handing.py"
        Start-Sleep -Seconds 3
        & $pythonExe "$scriptPath\download.py"
        Start-Sleep -Seconds 3
        & $pythonExe "$scriptPath\fix.py"
        Pause
    }
    elseif ($choice2 -eq '2') {
        & $pythonExe "$scriptPath\get_id.py" 'https://nhentai.net/search/?q=pages%3A%3E100+%5Bchinese%5D&page='
        Start-Sleep -Seconds 3
        & $pythonExe "$scriptPath\handing.py"
        Start-Sleep -Seconds 3
        & $pythonExe "$scriptPath\download.py"
        Start-Sleep -Seconds 3
        & $pythonExe "$scriptPath\fix.py"
        Pause
    }
    elseif ($choice2 -eq '3') {
        & $pythonExe "$scriptPath\get_id.py" 'https://nhentai.net/search/?q=pages%3A%3E60+uncensored+%5Bchinese%5D&page='
        Start-Sleep -Seconds 3
        & $pythonExe "$scriptPath\handing.py"
        Start-Sleep -Seconds 3
        & $pythonExe "$scriptPath\download.py"
        Start-Sleep -Seconds 3
        & $pythonExe "$scriptPath\fix.py"
        Pause
    }
    elseif ($choice2 -eq '4') {
        do {
            $url = Read-Host "Enter URL"
            if (Validate-Url $url) {
                & $pythonExe "$scriptPath\get_id.py" $url
                Start-Sleep -Seconds 3
                & $pythonExe "$scriptPath\handing.py"
                Start-Sleep -Seconds 3
                & $pythonExe "$scriptPath\download.py"
                Start-Sleep -Seconds 3
                & $pythonExe "$scriptPath\fix.py"
                Pause
                break # Exit loop
            }
            else {
                Write-Host "The entered URL is invalid, please enter a valid URL.`n"
            }
        } while ($true) # Continue looping until a valid URL is entered
    }
    else {
        Write-Host "Invalid input."
    }
}
elseif ($choice1 -eq '2') {
    & $pythonExe "$scriptPath\download.py"
    Start-Sleep -Seconds 3
    & $pythonExe "$scriptPath\fix.py"
    Pause
}
else {
    Write-Host "Invalid input."
}
