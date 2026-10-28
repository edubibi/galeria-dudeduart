const fs = require('fs');
const path = require('path');

const files = [
    "Ball in play.jpeg", "Bass stand yeah.jpeg", "Books forever.jpeg", 
    "Bruma.jpg", "Chrome Rhythms.jpg", "Deprisa, ven despacio.jpg", 
    "Dragon lands.jpg", "Feel your dreams.jpeg", "Lotus play.jpeg", 
    "Macao no es Lao.jpeg", "Much time ago.jpg", "Plastic hard.jpg", 
    "Tatum.png", "Without a trace of barbarism.jpeg", "bloody lukas.jpeg"
];

const cat_name = "54 LUNIORNAT portadas de discos";
const folder = "assets/54 LUNIORNAT/";

function titleCase(str) {
    return str.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ');
}

// 1. Update metadata.json
const meta_path = path.join(__dirname, "metadata.json");
let data = JSON.parse(fs.readFileSync(meta_path, 'utf8'));

for (let file of files) {
    const name_no_ext = path.basename(file, path.extname(file));
    const id_key = name_no_ext.toLowerCase();
    data[id_key] = {
        "id": id_key,
        "title": titleCase(name_no_ext),
        "category": cat_name,
        "src": folder + file,
        "description": "Nueva obra añadida recientemente.",
        "price": "1.500,00",
        "size": "Consultar"
    };
}

fs.writeFileSync(meta_path, JSON.stringify(data, null, 4), 'utf8');

// Update backup
const backup_path = path.join(__dirname, "metadata.backup.json");
fs.writeFileSync(backup_path, JSON.stringify(data, null, 4), 'utf8');

// 2. Update resumen_precios_excel.html
const excel_path = path.join(__dirname, "documentacion_y_planificacion", "resumen_precios_excel.html");
let html_content = fs.readFileSync(excel_path, 'utf8');

let new_elements = [];
for (let file of files) {
    const name_no_ext = path.basename(file, path.extname(file));
    const id_key = name_no_ext.toLowerCase();
    const title = titleCase(name_no_ext);
    new_elements.push(`    {
        "id": "${id_key}",
        "title": "${title}",
        "category": "${cat_name}",
        "src": "${folder}${file}",
        "current_price": "1.500,00 €",
        "tier": "Nivel 3: Premium",
        "proposed_price": "1.500,00",
        "actual_price": "1.500,00",
        "badge_class": "badge-n1",
        "edition": "Ed. Limitada (15 copias)",
        "serial_format": "EA-PREM-${title.toUpperCase()}-01/15"
    }`);
}

const replacement = "    },\n" + new_elements.join(",\n") + "\n];";
html_content = html_content.replace(/    \}\n\];/g, replacement);

fs.writeFileSync(excel_path, html_content, 'utf8');

console.log("Updates complete.");
