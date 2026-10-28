$path = "C:\Users\Usuario\.gemini\antigravity-ide\scratch\01_APLICACIONES_Y_WEB\GALERIA_DUDEDUART\dossier_senart_FINAL.html"

Write-Host "Reading $path"
$content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

$target1 = "¿Cómo sueña la tecnología cuando es guiada por la sensibilidad y el corazón humano?"
$replacement = "La tecnología guiada por la sensibilidad y corazón humano"

if ($content.Contains($target1)) {
    $content = $content.Replace($target1, $replacement)
    [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
    Write-Host "Replacement successful."
} else {
    Write-Host "Target not found. It might be formatted differently or spread across multiple lines."
}
