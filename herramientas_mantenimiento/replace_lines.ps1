$path = "C:\Users\Usuario\.gemini\antigravity-ide\scratch\01_APLICACIONES_Y_WEB\GALERIA_DUDEDUART\dossier_senart_FINAL.html"

# Detect file encoding automatically or default to UTF8
$lines = [System.IO.File]::ReadAllLines($path, [System.Text.Encoding]::UTF8)

if ($lines[538] -match "sensibilidad") {
    Write-Host "Found target at line 539: " $lines[538]
    Write-Host "And line 540: " $lines[539]
    
    $lines[538] = "            <p><strong>La tecnología guiada por la sensibilidad y corazón humano</strong></p>"
    $lines[539] = "" # Clear the continuation line
    
    [System.IO.File]::WriteAllLines($path, $lines, [System.Text.Encoding]::UTF8)
    Write-Host "Replaced successfully!"
} else {
    Write-Host "Target not found at line 539. Searching..."
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match "sensibilidad y") {
            Write-Host "Found at line $($i + 1)"
            $lines[$i] = "            <p><strong>La tecnología guiada por la sensibilidad y corazón humano</strong></p>"
            if ($lines[$i+1] -match "corazón humano") {
                $lines[$i+1] = ""
            }
            [System.IO.File]::WriteAllLines($path, $lines, [System.Text.Encoding]::UTF8)
            Write-Host "Replaced successfully after search!"
            break
        }
    }
}
