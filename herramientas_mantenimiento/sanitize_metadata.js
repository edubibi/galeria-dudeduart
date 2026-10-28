const fs = require('fs');
const path = require('path');

const metadataPath = path.join(__dirname, 'metadata.json');

console.log("Limpiando metadata.json y arreglando rutas...");

let rawMetadata = fs.readFileSync(metadataPath, 'utf8');

// Eliminar el BOM si existe
if (rawMetadata.charCodeAt(0) === 0xFEFF) {
    rawMetadata = rawMetadata.slice(1);
}

// 1. Corregir caracteres rotos masivamente
const replacements = {
    'á': 'á', 'é': 'é', 'í': 'í', 'ó': 'ó', 'ú': 'ú',
    'ñ': 'ñ', '¿': '¿', 'Á': 'à', 'Ã¨': 'è', 'Ã¬': 'ì',
    'Ã²': 'ò', 'Ã¹': 'ù', 'Ã': 'í', '¡': '¡', 'Ñ': 'Ñ'
};

Object.keys(replacements).forEach(key => {
    const regex = new RegExp(key, 'g');
    rawMetadata = rawMetadata.replace(regex, replacements[key]);
});

// 2. Corregir específicamente la ruta de ADMIRACION (ahora sin tilde)
rawMetadata = rawMetadata.replace(/ADMIRACIÓ N.png/g, 'ADMIRACION.png');
rawMetadata = rawMetadata.replace(/ADMIRACIÓN.png/g, 'ADMIRACION.png');
rawMetadata = rawMetadata.replace(/Admiración/g, 'Admiracion');

// Guardar metadata limpia
fs.writeFileSync(metadataPath, rawMetadata, 'utf8');
console.log("metadata.json limpio y actualizado.");
