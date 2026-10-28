const fs = require('fs');
const path = require('path');

const files = ['muestrario_estilos.html', 'catalogo_completo.html', 'memorandum.html', 'dossier_portfolio.html'];

const replacements = {
    'á': 'á', 'é': 'é', 'í': 'í', 'ó': 'ó', 'ú': 'ú',
    'ñ': 'ñ', '¿': '¿', 'Á': 'à', 'Ã¨': 'è', 'Ã¬': 'ì',
    'Ã²': 'ò', 'Ã¹': 'ù', 'Ã': 'í', '¡': '¡', 'Ñ': 'Ñ'
};

files.forEach(file => {
    const filePath = path.join(process.cwd(), file);
    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Fix the specific "RamÃrez" case which can be tricky
        content = content.replace(/Ramírez/g, 'Ramírez');
        content = content.replace(/RamÃrez/g, 'Ramírez');

        Object.keys(replacements).forEach(key => {
            const regex = new RegExp(key, 'g');
            content = content.replace(regex, replacements[key]);
        });

        // Also fix some common entities if they got broken
        content = content.replace(/&iacute;/g, 'í');
        content = content.replace(/&oacute;/g, 'ó');
        content = content.replace(/&aacute;/g, 'á');
        content = content.replace(/&eacute;/g, 'é');
        content = content.replace(/&ntilde;/g, 'ñ');

        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`File fixed: ${file}`);
    }
});
