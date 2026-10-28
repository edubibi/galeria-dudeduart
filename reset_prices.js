const fs = require('fs');
const path = require('path');

// 1. Update metadata.json and backup
const metaPath = path.join(__dirname, 'metadata.json');
const metaBackupPath = path.join(__dirname, 'metadata.backup.json');

let meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));

for (let key in meta) {
    if (meta[key].price === '19,99') {
        meta[key].price = '';
    }
}

fs.writeFileSync(metaPath, JSON.stringify(meta, null, 4), 'utf8');
fs.writeFileSync(metaBackupPath, JSON.stringify(meta, null, 4), 'utf8');

// 2. Update resumen_precios_excel.html
const excelPath = path.join(__dirname, 'documentacion_y_planificacion', 'resumen_precios_excel.html');
let excelContent = fs.readFileSync(excelPath, 'utf8');

// We need to replace "19,99 €" with "" and "19,99" with ""
// But since the UI might require a valid number string or expect it empty for proposing, we can set them to empty string ""
// Or "0,00" if empty breaks it. Usually empty string is fine for a text input.
excelContent = excelContent.replace(/"current_price":\s*"19,99\s*€"/g, '"current_price": "0,00 €"');
excelContent = excelContent.replace(/"actual_price":\s*"19,99"/g, '"actual_price": ""');
excelContent = excelContent.replace(/"proposed_price":\s*"19,99"/g, '"proposed_price": ""');

fs.writeFileSync(excelPath, excelContent, 'utf8');

console.log("Prices reset.");
