/**
 * DUDEDUART: LAS 5 GRANDES SALAS DE LA HISTORIA DEL ARTE
 * Curaduría y Taxonomía Universal de Eduardo Ramírez de Cartagena
 */

const SALAS_CONFIG = {
    "todas": {
        id: "todas",
        numeral: "GLOBAL",
        title: "Muestrario Vivo: Colección Completa",
        shortTitle: "🏛️ Todas las Salas",
        icon: "🏛️",
        period: "Paleolítico al Arte Contemporáneo",
        badge: "CATÁLOGO GLOBAL",
        desc: "601 obras maestras y 61 series temáticas que componen el Muestrario Vivo de la Historia de la Pintura. Un recorrido cronológico, técnico y pedagógico guiado por una sola visión creadora.",
        categories: []
    },
    "sala_1": {
        id: "sala_1",
        numeral: "SALA I",
        title: "Sala I: El Origen Rupestre y el Oficio Clásico",
        shortTitle: "🏛️ I. Clásico & Rupestre",
        icon: "🏛️",
        period: "Paleolítico Superior – Siglo XVIII",
        badge: "ORIGEN & CANON CLÁSICO",
        desc: "Desde el despertar del arte parietal con pigmentos de óxido, carbón y arpillera rústica (Serie RUPESSE) hasta la precisión matemática del canon renacentista, el dibujo anatómico, el carbón monumental sobre piedra y la tinta milenaria sobre papel oriental.",
        categories: [
            "61 RUPESSE",
            "00 EDUSSE",
            "06 IDE CLASSIC",
            "51 NEO-CLASICC",
            "52 EDUSSE CLASSIC",
            "24BORACARBON MONUMENTOS",
            "35PAPERCHIN"
        ]
    },
    "sala_2": {
        id: "sala_2",
        numeral: "SALA II",
        title: "Sala II: Romanticismo y Paisaje Sublime",
        shortTitle: "🌿 II. Romanticismo & Paisaje",
        icon: "🌿",
        period: "Siglo XIX",
        badge: "LUZ, VIENTO Y EMOCIÓN",
        desc: "La naturaleza indómita convertida en reflejo del alma humana. Óleos cargados de luz atmosférica, horizontes crepusculares, marinas vivas y poesía visual que capturan la comunión espiritual del creador con el entorno salvaje.",
        categories: [
            "31OLENATUR",
            "30OLONATUR-COLOR",
            "56 NATURALEXSSE",
            "33MINIGESTPOETIC",
            "49 ARTE CIBERNETICO NATURE",
            "26CARL_LINE"
        ]
    },
    "sala_3": {
        id: "sala_3",
        numeral: "SALA III",
        title: "Sala III: El Laboratorio de las Vanguardias Modernas",
        shortTitle: "🎨 III. Vanguardias Modernas",
        icon: "🎨",
        period: "Finales Siglo XIX – Mediados Siglo XX",
        badge: "RUPTURA & LIBERACIÓN FORMAL",
        desc: "La gran revolución del lenguaje pictórico. La captura de la luz fugaz en el agua (Monetesse), el trazo enérgico y febril (VG Stilo), la fragmentación geométrica del espacio (Cubesse), la espátula matérica esculpiendo óleo y la abstracción lírica pura.",
        categories: [
            "53 MONETESSE",
            "58 VG STILO",
            "03 EXPNEOPLUS",
            "50 NEO FAUVE",
            "02 CUBESSE STILO",
            "10OLEOCUBBO",
            "15CUBESSEPLUS",
            "12 CRISTAL CÚBICO",
            "13RECTESSE",
            "28ESPATAC",
            "01 EXP NEOCIRC",
            "37 IMPASTUS PAINT",
            "46ESPATAC-EXTREME",
            "29ESPATAC-MAT",
            "34EXPTERICO",
            "16EXPNEO",
            "14TEREXSE",
            "17FUZZTESS",
            "21OCE-BURST",
            "19 FUZZLINE ABS",
            "20BORASSIE",
            "23TRIDIM-BURST",
            "18 ABSTRACTO CONFLUENCIA",
            "27LINEVORT"
        ]
    },
    "sala_4": {
        id: "sala_4",
        numeral: "SALA IV",
        title: "Sala IV: Escultura sobre Lienzo y Relieve 3D (Alta Gama B2B)",
        shortTitle: "✨ IV. Relieve 3D / B2B",
        icon: "✨",
        period: "Arte Matérico & Alta Gama Arquitectónica",
        badge: "ESCULTURA ARQUITECTÓNICA",
        desc: "La pintura que se hace relieve y dialoga con la arquitectura de lujo. Piezas monumentales modeladas con morteros de gesso noble, texturas minerales, pan de oro y las cicatrices doradas del Kintsugi japonés, pensadas para espacios corporativos y hotelería de 5 estrellas.",
        categories: [
            "B2B MAGNA (ACCESO EXCLUSIVO)",
            "39 MATERDIGISSE",
            "57 STUCKEDU",
            "41 GESSOLUX",
            "42 GESSOLUX EXTREMUM",
            "44 GESSOLUX AZURITE",
            "45 GESSOLUX IRIS",
            "40 MECHPASTOSSE",
            "48BESSELUXY_L"
        ]
    },
    "sala_5": {
        id: "sala_5",
        numeral: "SALA V",
        title: "Sala V: Alta Costura, Estética Noir y Vanguardia Digital",
        shortTitle: "🖤 V. Alta Costura & Noir",
        icon: "🖤",
        period: "Siglo XXI – Contemporáneo",
        badge: "SOFISTICACIÓN & MODERNIDAD",
        desc: "El encuentro entre la alta costura (Haute Couture), la penumbra cinematográfica del Film Noir, la gráfica teatral a tinta y el diálogo interdisciplinar con la música. Coronada por la obra monumental «Baila en el puente» (Tríptico de 260 × 120 cm).",
        categories: [
            "59 ALTA COSTURA & NOIR",
            "32SINNOIR",
            "07 NEOINK",
            "54 LUNIORNAT portadas de discos",
            "04 APLICC",
            "08BORACARBON",
            "36 LINEART",
            "05 PLUMINK",
            "09FRACNEO",
            "47 NEBULÍNICO",
            "11URBANSPHERIC",
            "55 VORGGIPAH",
            "22NEO-LUMINA",
            "25CAPLIVE"
        ]
    },
    "gabinete_postal": {
        id: "gabinete_postal",
        numeral: "GABINETE",
        title: "Gabinete Filatélico: Historia Cincelada",
        shortTitle: "📮 Arte Postal & Filatelia",
        icon: "📮",
        period: "Grabado y Patrimonio Histórico Postal",
        badge: "PATRIMONIO HISTÓRICO",
        desc: "Colección conmemorativa dedicada al arte postal. Cuarenta piezas de micro-grabado e iconografía filatélica que recorren la memoria gráfica, monumental y documental de España tratada como una disciplina artística en sí misma.",
        categories: [
            "HISTORIA CINCELADA"
        ]
    }
};

if (typeof window !== 'undefined') {
    window.SALAS_CONFIG = SALAS_CONFIG;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SALAS_CONFIG;
}

