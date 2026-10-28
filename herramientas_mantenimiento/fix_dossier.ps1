$path = "C:\Users\Usuario\.gemini\antigravity-ide\scratch\01_APLICACIONES_Y_WEB\GALERIA_DUDEDUART\dossier_senart_FINAL.html"

$lines = [System.IO.File]::ReadAllLines($path, [System.Text.Encoding]::UTF8)

if ($lines[539].Trim() -eq "") {
    Write-Host "Line 540 is empty, restoring it."
    $lines[539] = "            <p>Como creador multidisciplinario bajo la filosofía de <strong>SENSORY ARTISTIC (senart)</strong>, entiendo la tecnología no como un fin o un generador automático de algoritmos, sino como una extensión de los sentidos. Cada pieza en el `"Universo EDUSSE`" nace de una visión personal íntima -un recuerdo, un acorde de sonido, una emoción o un imposible arquitectónico- que moldeo y esculpo meticulosamente a través de un diálogo digital honesto.</p>"
    [System.IO.File]::WriteAllLines($path, $lines, [System.Text.Encoding]::UTF8)
    Write-Host "Restored successfully."
} else {
    Write-Host "Line 540 is not empty. It contains: " $lines[539]
}

# Check line 539 to see if encoding is okay
Write-Host "Line 539: " $lines[538]
