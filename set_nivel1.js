const fs = require('fs');
const path = require('path');

const catName = "54 LUNIORNAT portadas de discos";

// 1. Update metadata.json
const metaPath = path.join(__dirname, 'metadata.json');
const metaBackupPath = path.join(__dirname, 'metadata.backup.json');

let meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));

for (let key in meta) {
    if (meta[key].category === catName) {
        meta[key].price = "250,00";
    }
}

fs.writeFileSync(metaPath, JSON.stringify(meta, null, 4), 'utf8');
fs.writeFileSync(metaBackupPath, JSON.stringify(meta, null, 4), 'utf8');

// 2. Update resumen_precios_excel.html
const excelPath = path.join(__dirname, 'documentacion_y_planificacion', 'resumen_precios_excel.html');
let excelContent = fs.readFileSync(excelPath, 'utf8');

let arrayMatch = excelContent.match(/const artworks = (\[[\s\S]*?\]);/);
if (arrayMatch) {
    let artworks = JSON.parse(arrayMatch[1]);
    for (let art of artworks) {
        if (art.category === catName) {
            art.current_price = "250,00 €";
            art.tier = "Nivel 1: Acceso";
            art.proposed_price = "";
            art.actual_price = "250,00";
            art.badge_class = "badge-n4";
            art.edition = "Ed. Limitada (30 copias)";
            art.serial_format = `EA-ACC-${art.title.toUpperCase().replace(/\s+/g, '')}-01/30`;
        }
    }
    
    // We stringify the array, indent properly, and replace the old block
    let replacement = "const artworks = " + JSON.stringify(artworks, null, 4) + ";";
    excelContent = excelContent.replace(/const artworks = \[[\s\S]*?\];/, replacement);
    fs.writeFileSync(excelPath, excelContent, 'utf8');
    console.log("Updated 54 LUNIORNAT to Nivel 1.");
} else {
    console.error("Could not find artworks array in HTML.");
}
