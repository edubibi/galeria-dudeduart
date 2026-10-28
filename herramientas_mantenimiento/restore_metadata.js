const fs = require('fs');
const path = require('path');

const metadataPath = path.join(__dirname, 'metadata.json');

console.log("Restaurando tildes correctas en metadata.json...");

let rawMetadata = fs.readFileSync(metadataPath, 'utf8');

// Eliminar rastro de BOM
if (rawMetadata.charCodeAt(0) === 0xFEFF) rawMetadata = rawMetadata.slice(1);

// Reemplazos ultra-específicos para sanar el archivo
const fixes = [
    { from: /ADMIRACIí“N\.png/g, to: 'ADMIRACIÓN.png' },
    { from: /ADMIRACIÓN\.png/g, to: 'ADMIRACIÓN.png' },
    { from: /Admiración/g, to: 'Admiración' },
    { from: /Admiración/g, to: 'Admiración' },
    { from: /ó/g, to: 'ó' },
    { from: /á/g, to: 'á' },
    { from: /í/g, to: 'í' },
    { from: /é/g, to: 'é' },
    { from: /ú/g, to: 'ú' },
    { from: /ñ/g, to: 'ñ' },
    { from: /¿/g, to: '¿' }
];

fixes.forEach(fix => {
    rawMetadata = rawMetadata.replace(fix.from, fix.to);
});

// Guardar
fs.writeFileSync(metadataPath, rawMetadata, 'utf8');
console.log("metadata.json restaurado con éxito.");
