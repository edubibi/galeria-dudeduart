# 📘 GUÍA RÁPIDA: Cómo añadir obras a tu Web (Protocolo Oficial DudeduArt)

Tu página web es dinámica: lee el inventario curatorial de **`js/data.js`** y lo renderiza automáticamente en la Cuadroteca, Salas y Buscador.

---

## PASO 1: La Imagen 📸
Guarda la fotografía o arte digital de tu nueva obra en su carpeta dentro de **`assets/`**.
* Ejemplo: `assets/61RUPESSE/mi_obra_maestra.jpg`

## PASO 2: El Registro con Fecha Obligatoria 📝
Abre el archivo **`js/data.js`**. Cada obra debe contener su ficha completa incluyendo la **fecha de creación en formato `MM/YYYY`**:

```javascript
    {
        "id": "mi_obra_001",
        "title": "Mi Nueva Obra Maestra",
        "category": "61 RUPESSE",
        "src": "assets/61RUPESSE/mi_obra_maestra.jpg",
        "description": "Descripción artística detallada de la obra.",
        "size": "50×70 cm",
        "price": "2.400,00",
        "tech_info": "Técnica, soporte y pigmentos.",
        "sold": false,
        "date": "11/2026"  // <-- OBLIGATORIO: Fecha de creación en formato MM/YYYY
    },
```

La fecha `"date": "MM/YYYY"` se renderiza de forma automática **justo debajo del título** en la tarjeta de la galería y dentro del visor de detalles.

---

## 🎨 CÓMO ASOCIAR LAS OBRAS A UN "ESTILO"
1. En el campo `"category"`, escribe el nombre oficial de la Serie o Estilo (ej: `"61 RUPESSE"`, `"59 ALTA COSTURA & NOIR"`, etc.).
2. El sistema lo agrupa, indexa y lo vincula a los filtros por décadas (`00s`, `10s`, `20s`... `SELLOS`) y a las 5 Grandes Salas Universales sin necesidad de tocar código.
