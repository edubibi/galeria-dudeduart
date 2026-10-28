const fs = require('fs');
const path = require('path');

const metadataPath = path.join(__dirname, 'metadata.json');
const stampsSnippetPath = path.join(__dirname, 'stamps_metadata_snippet.json');
const dataPath = path.join(__dirname, 'js', 'data.js');

console.log("Iniciando reconstrucción final: 40 SELLOS MÁGICOS al final...");

// 1. Leer metadata.json
let metadata;
try {
    let rawMetadata = fs.readFileSync(metadataPath, 'utf8');
    if (rawMetadata.charCodeAt(0) === 0xFEFF) rawMetadata = rawMetadata.slice(1);
    metadata = JSON.parse(rawMetadata);
} catch (e) {
    console.error("Error leyendo metadata.json:", e);
    process.exit(1);
}

// 2. Leer stamps_metadata_snippet.json
let stampsMeta;
try {
    stampsMeta = JSON.parse(fs.readFileSync(stampsSnippetPath, 'utf8'));
} catch (e) {
    console.error("Error leyendo stamps metadata:", e);
    process.exit(1);
}

// 3. Convertir obras normales a array
const regularArtworks = Object.values(metadata).filter(art => {
    const cat = art.category || "";
    return cat !== 'SELLOS_MAGICOS' && !cat.includes('SELLOS');
});

// 4. Crear array de Sellos Mágicos con categoría numerada para forzar el orden
const newStamps = Object.entries(stampsMeta).map(([id, info]) => ({
    id: id,
    title: info.title,
    category: "1000 SELLOS MAGICOS",
    src: `assets/SELLOS_MAGICOS/${id}.png`,
    description: "Obra de la colección de Sellos Mágicos. Historia y arte postal.",
    size: "Consultar",
    price: "19,99",
    tech_info: "",
    sold: false
}));

// 5. COMBINAR
const finalData = [...regularArtworks, ...newStamps];

// 6. Mapa de Portadas (Actualizado)
const categoryCovers = {
    "photo_3_2025-12-15_18-32-25": "assets/PORTADILLAS_ESTILOS/photo_3_2025-12-15_18-32-25.jpg",
    "20BORASSIE": "assets/PORTADILLAS_ESTILOS/20BORASSIE.jpg",
    "04 APLICC": "assets/PORTADILLAS_ESTILOS/04APLICC.jpg",
    "photo_7_2025-12-15_18-32-25": "assets/PORTADILLAS_ESTILOS/photo_7_2025-12-15_18-32-25.jpg",
    "07 NEOINK": "assets/PORTADILLAS_ESTILOS/07NEOINK_stilo.jpg",
    "02 CUBESSE STILO": "assets/PORTADILLAS_ESTILOS/02CUBESSE_stilo.jpg",
    "10OLEOCUBBO": "assets/PORTADILLAS_ESTILOS/10OLEOCUBBO.jpg",
    "00 EDUSSE": "assets/PORTADILLAS_ESTILOS/00EDUSSE.jpg",
    "photo_11_2025-12-15_18-32-25": "assets/PORTADILLAS_ESTILOS/photo_11_2025-12-15_18-32-25.jpg",
    "photo_4_2025-12-15_18-32-25": "assets/PORTADILLAS_ESTILOS/photo_4_2025-12-15_18-32-25.jpg",
    "09FRACNEO": "assets/PORTADILLAS_ESTILOS/09FRACNEO.jpg",
    "06 IDE CLASSIC": "assets/PORTADILLAS_ESTILOS/06IDE_CLASSIC.jpg",
    "05 PLUMINK": "assets/PORTADILLAS_ESTILOS/05PLUMINK.jpg",
    "photo_8_2025-12-15_18-32-25": "assets/PORTADILLAS_ESTILOS/photo_8_2025-12-15_18-32-25.jpg",
    "11URBANSPHERIC": "assets/PORTADILLAS_ESTILOS/11URBANSPHERIC.png",
    "photo_10_2025-12-15_18-32-25": "assets/PORTADILLAS_ESTILOS/photo_10_2025-12-15_18-32-25.jpg",
    "12 CRISTAL CÚBICO": "assets/PORTADILLAS_ESTILOS/CRISTAL_CUBICO.jpg",
    "03 EXPNEOPLUS": "assets/PORTADILLAS_ESTILOS/03EXPNEOPLUS.jpg",
    "photo_12_2025-12-15_18-32-25": "assets/PORTADILLAS_ESTILOS/photo_12_2025-12-15_18-32-25.jpg",
    "08BORACARBON": "assets/PORTADILLAS_ESTILOS/08BORACARBON.jpg",
    "01 EXP NEOCIRC": "assets/PORTADILLAS_ESTILOS/01EXP_NEOCIRC.jpg",
    "photo_2_2025-12-15_18-32-25": "assets/PORTADILLAS_ESTILOS/photo_2_2025-12-15_18-32-25.jpg",
    "30OLONATUR-COLOR": "assets/30OLONATUR-COLOR/Cote de Granit Rose de Francia.png",
    "31OLENATUR": "assets/31OLENATUR/ARC DU TRIUMPH.png",
    "32SINNOIR": "assets/32SINNOIR/banco de piedra.png",
    "33MINIGESTPOETIC": "assets/33MINIGESTPOETIC/el_ojo_del_cazador.png",
    "00FURSONA GENESIS": "assets/00FURSONA GENESIS/fursona-genesis-portada.png",
    "36 LINEART": "assets/36LINEART/chica joven posando.png",
    "37 IMPASTUS PAINT": "assets/37IMPASTUS PAINT/MANHATTAN.png",
    "1000 SELLOS MAGICOS": "assets/SELLOS_MAGICOS/sello_magico_001.png"
};

const header = `/**
 * BASE DE DATOS DE OBRAS
 * Sincronizada: ${new Date().toLocaleString()}
 */

const categoryCovers = ${JSON.stringify(categoryCovers, null, 4)};

const artworkData = `;

const finalContent = header + JSON.stringify(finalData, null, 4) + ";";

try {
    fs.writeFileSync(dataPath, finalContent, 'utf8');
    console.log(`¡Éxito! 40 SELLOS MÁGICOS integrados.`);
} catch (e) {
    console.error("Error escribiendo data.js:", e);
    process.exit(1);
}
