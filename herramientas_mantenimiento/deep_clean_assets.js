const fs = require('fs');
const path = require('path');

const baseDir = path.join(__dirname, 'assets');
const metadataPath = path.join(__dirname, 'metadata.json');

const accentMap = {
    'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
    'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
    'ñ': 'n', 'Ñ': 'N'
};

function removeAccents(str) {
    return str.split('').map(char => accentMap[char] || char).join('');
}

let renamingLog = [];

function walkDir(dir) {
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        const filePath = path.join(dir, file);
        const stats = fs.statSync(filePath);
        if (stats.isDirectory()) {
            walkDir(filePath);
        } else {
            const cleanName = removeAccents(file);
            if (cleanName !== file) {
                const newFilePath = path.join(dir, cleanName);
                fs.renameSync(filePath, newFilePath);
                
                // Guardar para actualizar metadata (usar rutas relativas a la raíz)
                const relativeOld = path.relative(__dirname, filePath).replace(/\\/g, '/');
                const relativeNew = path.relative(__dirname, newFilePath).replace(/\\/g, '/');
                renamingLog.push({ old: relativeOld, next: relativeNew });
                console.log(`Renombrado: ${file} -> ${cleanName}`);
            }
        }
    });
}

// 1. Renombrar archivos físicos
console.log("Iniciando renombrado de archivos...");
walkDir(baseDir);

// 2. Actualizar metadata.json
console.log("Actualizando metadata.json...");
let rawMetadata = fs.readFileSync(metadataPath, 'utf8');
if (rawMetadata.charCodeAt(0) === 0xFEFF) rawMetadata = rawMetadata.slice(1);

renamingLog.forEach(entry => {
    // Escapar caracteres para regex
    const escapedOld = entry.old.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(escapedOld, 'g');
    rawMetadata = rawMetadata.replace(regex, entry.next);
});

// También limpiar acentos en los campos "src" que no se hayan detectado por el log
// (por si acaso había discrepancias previas)
// Pero con cuidado de no romper los títulos
const metadataObj = JSON.parse(rawMetadata);
Object.keys(metadataObj).forEach(key => {
    if (metadataObj[key].src) {
        metadataObj[key].src = removeAccents(metadataObj[key].src);
    }
});

fs.writeFileSync(metadataPath, JSON.stringify(metadataObj, null, 4), 'utf8');
console.log(`¡Limpieza completada! Se han renombrado ${renamingLog.length} archivos.`);
