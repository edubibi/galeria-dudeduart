const fs = require('fs');
const path = require('path');

const metadataPath = path.join(__dirname, 'metadata.json');

console.log("Iniciando Escáner de Salud y Reparación de Galería...");

let metadata;
try {
    let raw = fs.readFileSync(metadataPath, 'utf8');
    if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
    metadata = JSON.parse(raw);
} catch (e) {
    console.error("Error cargando metadata:", e);
    process.exit(1);
}

const accentMap = {
    'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
    'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
    'ñ': 'n', 'Ñ': 'N'
};

function normalize(str) {
    return str.split('').map(char => accentMap[char] || char).join('').toLowerCase();
}

let fixedCount = 0;
let missingCount = 0;

Object.keys(metadata).forEach(key => {
    const item = metadata[key];
    if (!item.src) return;

    const fullPath = path.join(__dirname, item.src.replace(/\//g, path.sep));
    
    if (!fs.existsSync(fullPath)) {
        console.log(`Buscando reemplazo para: ${item.src}`);
        
        // Intentar encontrar el archivo real en la misma carpeta
        const dir = path.dirname(fullPath);
        if (fs.existsSync(dir)) {
            const files = fs.readdirSync(dir);
            const targetBase = normalize(path.basename(fullPath));
            
            const match = files.find(f => normalize(f) === targetBase);
            if (match) {
                const newSrc = path.join(path.dirname(item.src), match).replace(/\\/g, '/');
                console.log(`  -> ¡Encontrado! Nuevo src: ${newSrc}`);
                item.src = newSrc;
                fixedCount++;
            } else {
                console.warn(`  !! No se encontró archivo para: ${item.src}`);
                missingCount++;
            }
        } else {
            console.warn(`  !! Directorio no existe: ${path.dirname(item.src)}`);
            missingCount++;
        }
    }
});

fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 4), 'utf8');
console.log(`\nResumen del Escáner:`);
console.log(`- Vínculos reparados: ${fixedCount}`);
console.log(`- Archivos no encontrados: ${missingCount}`);
console.log(`- Total de obras procesadas: ${Object.keys(metadata).length}`);
