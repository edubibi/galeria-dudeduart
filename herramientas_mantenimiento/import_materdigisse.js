const fs = require('fs');
const path = require('path');

const ASSETS_DIR = 'assets/39MATERDIGISSE';
const DATA_JS_PATH = 'js/data.js';
const METADATA_PATH = 'metadata.json';

function registerMaterdigisse() {
    let metadata = {};
    if (fs.existsSync(METADATA_PATH)) {
        metadata = JSON.parse(fs.readFileSync(METADATA_PATH, 'utf-8'));
    }

    const files = fs.readdirSync(ASSETS_DIR).filter(f => f.match(/\.(png|jpe?g)$/i)).sort();

    const existingSrcs = new Set();
    let maxId = 0;

    for (const [id, item] of Object.entries(metadata)) {
        if (item && typeof item === 'object' && item.category === "39 MATERDIGISSE") {
            existingSrcs.add(item.src);
        }
        if (id.startsWith("39materdigisse_")) {
            const num = parseInt(id.split('_')[1], 10);
            if (num > maxId) maxId = num;
        }
    }

    const newEntries = [];
    const category = "39 MATERDIGISSE";

    for (const filename of files) {
        const srcPath = `assets/39MATERDIGISSE/${filename}`;
        if (existingSrcs.has(srcPath)) continue;

        maxId++;
        let cleanName = filename.replace(/\.[^/.]+$/, "");
        // "Husky_with_glass_impasto plus" -> "Husky With Glass Impasto"
        let title = cleanName.replace(/_/g, ' ').replace(/-/g, ' ').replace(/ plus/gi, '');
        title = title.replace(/\b\w/g, l => l.toUpperCase());

        const itemId = `39materdigisse_${String(maxId).padStart(3, '0')}`;

        const entry = {
            id: itemId,
            title: title,
            category: category,
            src: srcPath,
            description: "Exploración de la materia digital y energía vortical. Sinergia entre figura y trazo rítmico.",
            size: "Consultar",
            price: "19,99 €",
            tech_info: "Técnica MATERDIGISSE (Digital Impasto)",
            sold: false
        };
        newEntries.append ? newEntries.push(entry) : newEntries.push(entry);
    }

    if (newEntries.length === 0) {
        console.log("No new artworks found to register.");
        return;
    }

    // Update metadata.json
    for (const entry of newEntries) {
        metadata[entry.id] = entry;
    }
    fs.writeFileSync(METADATA_PATH, JSON.stringify(metadata, null, 4), 'utf-8');

    // Update data.js
    let jsContent = fs.readFileSync(DATA_JS_PATH, 'utf-8');
    
    // We need to inject the new objects into the artworkData array in data.js
    // Look for the last ]; in the file
    const jsEntriesStr = newEntries.map(e => `    ${JSON.stringify(e)}`).join(',\n');
    
    // Find the last occurrence of ];
    const lastIndex = jsContent.lastIndexOf('];');
    if (lastIndex !== -1) {
        const before = jsContent.substring(0, lastIndex).trimEnd();
        const comma = before.endsWith(',') ? '' : ',';
        const after = jsContent.substring(lastIndex);
        
        jsContent = before + comma + '\n' + jsEntriesStr + '\n' + after;
        fs.writeFileSync(DATA_JS_PATH, jsContent, 'utf-8');
        console.log(`Registered ${newEntries.length} NEW artworks in ${category}`);
    } else {
        console.log("Could not find ]; in data.js");
    }
}

registerMaterdigisse();
