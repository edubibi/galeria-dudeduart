document.addEventListener('DOMContentLoaded', init);

function init() {
    console.log("Iniciando Galería Digital Neon Edition...");

    if (typeof artworkData === 'undefined') {
        console.error("No se han cargado los datos de las obras.");
        document.getElementById('gallery-container').innerHTML = "<p style='color:white; text-align:center; padding:2rem;'>Error: No se encontraron obras.</p>";
        return;
    }

    let dataToLoad = artworkData;

    // Check if there is a category filter in the URL
    const params = new URLSearchParams(window.location.search);
    const catFilter = params.get('category');

    if (catFilter && catFilter !== 'null' && catFilter !== '') {
        console.log("Filtrando galería digital por categoría:", catFilter);

        // Let's decode more safely just in case
        let targetCat = decodeURIComponent(catFilter);
        console.log("Categoría decodificada:", targetCat);

        // Exact match filter (with trim just in case)
        dataToLoad = artworkData.filter(art => (art.category || "").trim() === targetCat.trim());

        console.log("Obras encontradas para esta categoría:", dataToLoad.length);

        if (dataToLoad.length === 0) {
            alert(`No se encontraron obras para la categoría: "${targetCat}". Mostrando todas.`);
            dataToLoad = artworkData; // Fallback to all if category mismatch
        } else {
            // Update title to show collection name only if we found items
            const titleEl = document.querySelector('.neon-title');
            if (titleEl) {
                const cleanTitle = targetCat.replace(/^\d+/, '').replace(/_/g, ' ').trim();
                titleEl.innerHTML = `COLECCIÓN <span class="highlight">${cleanTitle.toUpperCase()}</span>`;
            }
        }
    }

    renderGrid(dataToLoad);
    setupSearch();
    setupMusic();
    setupHero();
    incrementVisitorCounter();

    if (params.has('auto_open')) {
        setTimeout(() => {
            if (dataToLoad && dataToLoad.length > 0) openHero(dataToLoad[0]);
        }, 300);
    }
}

function renderGrid(data) {
    const container = document.getElementById('gallery-container');
    container.innerHTML = '';

    // Group by Category
    const grouped = {};
    data.forEach(item => {
        if (typeof item !== "object" || item === null) return;
        let cat = item.category || 'Otros';
        if (!grouped[cat]) grouped[cat] = [];
        grouped[cat].push(item);
    });

    // Sort categories, but ensure SELLOS is ALWAYS at the end
    const sortedCategories = Object.keys(grouped).sort((a, b) => {
        if (a && a.toUpperCase().includes('SELLOS')) return 1;
        if (b && b.toUpperCase().includes('SELLOS')) return -1;
        return a.localeCompare(b);
    });

    sortedCategories.forEach(category => {
        const items = grouped[category];

        // Section
        const section = document.createElement('section');
        section.className = 'category-section';

        // Unique slug and data attributes for fast scrolling
        const catSlug = 'cat-' + category.toLowerCase().replace(/[^a-z0-9]/g, '-');
        section.id = catSlug;
        section.dataset.category = category;

        const numMatch = category.match(/^(\d+)/);
        if (numMatch) {
            section.dataset.decade = numMatch[1].charAt(0);
            section.dataset.number = numMatch[1];
        }

        // Check if B2B category is locked
        const isB2B = category.toUpperCase().includes('B2B MAGNA');
        if (isB2B) section.dataset.isB2b = "true";
        if (category.toUpperCase().includes('SELLOS')) section.dataset.isSellos = "true";
        const isUnlocked = localStorage.getItem('b2b_unlocked') === 'true';

        // Title
        const title = document.createElement('h2');
        title.className = 'category-title';
        
        if (isB2B) {
            if (isUnlocked) {
                title.innerHTML = `${category} <span style="font-size: 0.75rem; font-weight: normal; margin-left: 15px; cursor: pointer; color: #ef4444; border: 1px solid #ef4444; padding: 3px 8px; border-radius: 4px; transition: all 0.2s;" onclick="lockB2B()" onmouseover="this.style.background='#ef4444'; this.style.color='#fff';" onmouseout="this.style.background='transparent'; this.style.color='#ef4444';">🔒 Cerrar Acceso B2B</span>`;
            } else {
                title.innerText = category;
            }
        } else {
            title.innerText = category;
        }
        section.appendChild(title);

        if (isB2B && !isUnlocked) {
            // Render luxury black & gold locked access panel
            const lockBox = document.createElement('div');
            lockBox.className = 'b2b-lock-panel';
            lockBox.style.cssText = "background: #0d0d10; border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 8px; padding: 3rem 2.5rem; text-align: center; max-width: 560px; margin: 3rem auto; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8);";
            lockBox.innerHTML = `
                <div style="font-size: 2.8rem; margin-bottom: 1.2rem; color: #D4AF37; filter: drop-shadow(0 0 12px rgba(212, 175, 55, 0.3));">🔒</div>
                <h3 style="color: #D4AF37; margin-bottom: 1rem; font-size: 1.35rem; font-family: 'Playfair Display', serif; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;">Colección de Super Lujo B2B</h3>
                <p style="color: rgba(255, 255, 255, 0.8); font-family: 'Lato', sans-serif; font-size: 0.95rem; margin-bottom: 2rem; line-height: 1.6; max-width: 480px; margin-left: auto; margin-right: auto;">
                    Esta sección contiene obras exclusivas de gran formato para proyectos de interiorismo de alto nivel y cadenas hoteleras. Introduzca la clave de acceso autorizada.
                </p>
                <div style="display: flex; gap: 12px; justify-content: center; align-items: center; flex-wrap: wrap;">
                    <input type="password" id="b2b-password-input" placeholder="Clave de acceso..." style="background: #141418; border: 1px solid rgba(212, 175, 55, 0.35); color: #ffffff; padding: 12px 18px; border-radius: 6px; font-family: 'Lato', sans-serif; font-size: 0.95rem; outline: none; width: 230px; transition: all 0.3s; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);" onfocus="this.style.borderColor='#D4AF37'; this.style.boxShadow='0 0 8px rgba(212, 175, 55, 0.3)';" onblur="this.style.borderColor='rgba(212, 175, 55, 0.35)'; this.style.boxShadow='none';">
                    <button onclick="checkB2BPassword()" style="background: #D4AF37; color: #000000; font-weight: 700; font-family: 'Lato', sans-serif; border: none; padding: 12px 28px; border-radius: 6px; font-size: 0.95rem; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.25);" onmouseover="this.style.background='#f59e0b'; this.style.boxShadow='0 0 20px rgba(212, 175, 55, 0.5)';" onmouseout="this.style.background='#D4AF37'; this.style.boxShadow='0 4px 15px rgba(212, 175, 55, 0.25)';">Entrar</button>
                </div>
                <div id="b2b-password-error" style="color: #f87171; font-size: 0.88rem; margin-top: 14px; display: none; font-weight: 600;">⚠️ Clave incorrecta. Por favor, verifíquela y vuelva a intentar.</div>
            `;
            
            // Listen for Enter key
            setTimeout(() => {
                const input = document.getElementById('b2b-password-input');
                if (input) {
                    input.addEventListener('keydown', (e) => {
                        if (e.key === 'Enter') window.checkB2BPassword();
                    });
                }
            }, 100);

            section.appendChild(lockBox);
        } else {
            // Render normal artwork cards grid
            const grid = document.createElement('div');
            grid.className = 'art-grid';

            items.forEach(item => {
                const card = createCard(item);
                grid.appendChild(card);
            });

            section.appendChild(grid);
        }

        container.appendChild(section);
    });

    // Iniciar Navegación Rápida e Índice Memorándum SIEMPRE con el catálogo completo
    const allGrouped = {};
    artworkData.forEach(item => {
        if (typeof item !== "object" || item === null) return;
        let cat = item.category || 'Otros';
        if (!allGrouped[cat]) allGrouped[cat] = [];
        allGrouped[cat].push(item);
    });

    const allCategories = Object.keys(allGrouped).sort((a, b) => {
        if (a && a.toUpperCase().includes('SELLOS')) return 1;
        if (b && b.toUpperCase().includes('SELLOS')) return -1;
        return a.localeCompare(b);
    });

    setupQuickNav(allCategories, allGrouped);
}

function createCard(item) {
    const card = document.createElement('div');
    card.className = 'art-card';
    card.dataset.title = item.title.toLowerCase();

    // Image container
    const imgWrapper = document.createElement('div');
    imgWrapper.className = 'art-image-wrapper watermarked';
    const overlay = document.createElement('div');
    overlay.className = 'artwork-overlay';
    imgWrapper.appendChild(overlay);

    // Lazy load image
    const img = document.createElement('img');
    img.src = `../${item.src}`;
    img.loading = "lazy";
    img.alt = item.title;

    imgWrapper.appendChild(img);

    // Info container
    const info = document.createElement('div');
    info.className = 'art-info';

    const title = document.createElement('div');
    title.className = 'art-title';
    title.innerText = item.title;

    info.appendChild(title);
    // El precio se muestra únicamente dentro del modal de la obra según preferencia del usuario

    card.appendChild(imgWrapper);
    card.appendChild(info);

    // Event Click -> Hero
    card.addEventListener('click', () => openHero(item));

    return card;
}

// --- SEARCH ---
function setupSearch() {
    const input = document.getElementById('search-input');
    input.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const cards = document.querySelectorAll('.art-card');

        cards.forEach(card => {
            if (card.dataset.title.includes(term)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}


// --- HERO MODAL ---
function setupHero() {
    const overlay = document.getElementById('hero-overlay');

    // Also allow closing by clicking the overlay background
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) window.closeHero();
    });
}

window.comprarCuadro = function() {
    const itemData = window.currentHeroItem;
    console.log("Comprar pulsado. Item:", itemData);
    if (itemData) {
        const itemObj = {
            id: itemData.id,
            title: itemData.title,
            price: itemData.price,
            thumb: itemData.src
        };
        if (typeof addToCart === 'function') {
            const added = addToCart(itemObj);
            if (added) window.location.href = '../carrito.html';
            else alert('Esta obra ya está en tu carrito.');
        } else {
            alert('Error: el sistema de carrito no está disponible.');
        }
    }
};

window.probarCuadro = function() {
    const itemData = window.currentHeroItem;
    console.log("Probador pulsado. Item:", itemData);
    if (itemData) {
        const viewerLink = `../visor/index.html?img=${encodeURIComponent(itemData.src)}&title=${encodeURIComponent(itemData.title)}&category=${encodeURIComponent(itemData.category)}&id=${itemData.id}`;
        window.location.href = viewerLink;
    } else {
        alert("Ocurrió un error al intentar abrir esta obra en el probador.");
    }
};

function openHero(item) {
    window.currentHeroItem = item; // Store the item globally for the buttons
    const overlay = document.getElementById('hero-overlay');
    const heroImg = document.getElementById('hero-img');
    const heroTitle = document.getElementById('hero-title');
    const heroCat = document.getElementById('hero-category');
    const heroSize = document.getElementById('hero-size');
    const heroPrice = document.getElementById('hero-price');
    const heroDesc = document.getElementById('hero-desc');
    const probadorBtn = document.getElementById('btn-probador-cuadroteca');
    const comprarBtn = document.getElementById('btn-comprar-cuadroteca');
    const mockupContainer = document.getElementById('mockup-container');
    const mockupArtImg = document.getElementById('mockup-art-img');

    // Populate standard fields
    heroTitle.innerText = item.title;
    heroCat.innerText = item.category || 'Galería';
    heroPrice.innerText = (item.price && !item.price.toString().includes('€') && !item.price.toString().includes('EUR') && item.price.toLowerCase() !== 'consultar') ? `${item.price} €` : (item.price || 'Consultar');
    heroDesc.innerText = item.description || "Sin descripción disponible.";
    
    if (heroSize) {
        if (item.size && item.size.toLowerCase() !== 'consultar' && !item.size.toLowerCase().includes('consultar')) {
            heroSize.innerHTML = `📐 <strong>Formatos:</strong> ${item.size} <span style="display:block; font-size:0.8rem; color:#94a3b8; margin-top:2px;">(Medidas personalizadas bajo petición)</span>`;
        } else {
            heroSize.innerHTML = `📐 <strong>Formatos estándar:</strong> 50×70 cm · 70×100 cm · 100×140 cm <span style="display:block; font-size:0.8rem; color:#94a3b8; margin-top:2px;">(Medidas personalizadas bajo petición)</span>`;
        }
    }

    // Toggle mockup view for B2B Magna works
    const isB2B = item.category && (item.category === 'B2B Magna (Fuera de Web)' || item.b2b_only);
    if (isB2B) {
        if (heroImg) heroImg.style.display = 'none';
        if (mockupContainer) mockupContainer.style.display = 'block';
        if (mockupArtImg) mockupArtImg.src = `../${item.src}`;
    } else {
        if (heroImg) {
            heroImg.style.display = 'block';
            heroImg.src = `../${item.src}`;
        }
        if (mockupContainer) mockupContainer.style.display = 'none';
    }

    // Hide virtual tester for stamps and B2B Magna works
    const isSello = item.category && (item.category === 'HISTORIA CINCELADA' || item.category.includes('CINCELADA') || item.category.includes('SELLOS'));
    if (isSello || isB2B) {
        if (probadorBtn) probadorBtn.style.display = 'none';
        if (isSello) {
            if (comprarBtn) comprarBtn.innerText = '🛒 Comprar Sello';
        } else {
            if (comprarBtn) comprarBtn.innerText = '🛒 Adquirir Obra';
        }
    } else {
        if (probadorBtn) probadorBtn.style.display = 'block';
        if (comprarBtn) comprarBtn.innerText = '🛒 Comprar el Cuadro';
    }

    overlay.classList.add('active');
    const heroContent = overlay.querySelector('.hero-content');
    if (heroContent) heroContent.scrollTop = 0; // Reiniciar siempre arriba para que nunca aparezca cortado
    document.body.style.overflow = 'hidden'; // Lock scroll
}

window.closeHero = function () {
    const overlay = document.getElementById('hero-overlay');
    if (overlay) {
        overlay.classList.remove('active');
        const heroContent = overlay.querySelector('.hero-content');
        if (heroContent) heroContent.scrollTop = 0;
    }
    document.body.style.overflow = ''; // Unlock scroll
    document.body.style.overflowY = 'auto'; // Ensure it can scroll again if needed
};



// --- MUSIC ---
function setupMusic() {
    const audio = document.getElementById('bgMusic');
    const musicBtn = document.getElementById('musicBtn');

    if (!audio || !musicBtn) return;

    // Same logic as before roughly
    musicBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play().catch(e => console.error(e));
            musicBtn.innerText = "⏸ PAUSE";
            musicBtn.classList.add('playing');
        } else {
            audio.pause();
            musicBtn.innerText = "🎵 MÚSICA";
            musicBtn.classList.remove('playing');
        }
    });

    // Optional: Keep playlist logic if needed, but simplicity first.
    // If playlist is key, we can re-add the array logic.
    // Re-adding simple playlist logic for continuity
    const playlist = [
        "01Medianoche-en-la-Terraza.mp3",
        "All_around_if_you_want.mp3",
        "Black_and_grey_.mp3",
        "Close_Your_Feelings_Extended.mp3",
        "Groove_or_not.mp3",
        "Heaven_s_Glow.mp3",
        "Man_island_beach.mp3",
        "Meanwhile_I_Love_You.mp3",
        "Saxo_by_the_clouds.mp3",
        "Saxophone_Serenade.mp3",
        "Secret-of-Velvet.mp3",
        "Sharp-echoes.mp3",
        "Soft-corners.mp3",
        "Voices_for_dreams.mp3",
        "Woman_on_the_island_beach.mp3"
    ];
    let trackIdx = 0;
    const basePath = "../assets/music/";
    audio.src = basePath + playlist[0];

    audio.addEventListener('ended', () => {
        trackIdx = (trackIdx + 1) % playlist.length;
        audio.src = basePath + playlist[trackIdx];
        audio.play().catch(e => console.log(e));
    });
}

// --- VISITOR LOCAL STATS ---
function incrementVisitorCounter() {
    let visitsCuadroteca = parseInt(localStorage.getItem('visitas_cuadroteca') || '0', 10);
    let visitsVirtual = parseInt(localStorage.getItem('visitas_sala_virtual') || '0', 10);
    
    visitsCuadroteca += 1;
    localStorage.setItem('visitas_cuadroteca', visitsCuadroteca.toString());
    
    const footerStats = document.getElementById('footer-visitor-stats');
    if (footerStats) {
        footerStats.innerText = `Estadísticas de navegación local: Visitas a la Cuadroteca: ${visitsCuadroteca} | Visitas a la Sala Virtual: ${visitsVirtual}`;
    }
}

// --- B2B EXCLUSIVE PASSWORD GATE ---
window.checkB2BPassword = function() {
    const pwdInput = document.getElementById('b2b-password-input');
    const errorMsg = document.getElementById('b2b-password-error');
    if (!pwdInput) return;
    
    const val = pwdInput.value.trim().toUpperCase();
    if (val === 'DUDEMAGNA' || val === 'MAGNA2026') {
        localStorage.setItem('b2b_unlocked', 'true');
        location.reload(); // Re-render page to show unlocked items!
    } else {
        if (errorMsg) {
            errorMsg.style.display = 'block';
            pwdInput.value = '';
            pwdInput.focus();
        }
    }
};

window.lockB2B = function() {
    localStorage.removeItem('b2b_unlocked');
    location.reload();
};

// --- SISTEMA DE NAVEGACIÓN RÁPIDA E ÍNDICE MEMORÁNDUM ---
function setupQuickNav(categories, grouped) {
    const select = document.getElementById('quick-style-select');
    const memoGrid = document.getElementById('memo-index-grid');
    if (!select || !memoGrid) return;

    // Reset
    select.innerHTML = '<option value="">-- Elige Colección (00 al 56) --</option>';
    select.innerHTML += '<option value="ALL">🏛️ VER TODA LA GALERÍA (Todas las Obras)</option>';
    memoGrid.innerHTML = '';

    window.allCategoriesBySlug = {};
    window.decadeFirstCategory = {};
    window.b2bCategoryName = null;
    window.sellosCategoryName = null;

    categories.forEach(cat => {
        const count = (grouped[cat] || []).length;
        const catSlug = 'cat-' + cat.toLowerCase().replace(/[^a-z0-9]/g, '-');
        const cleanName = cat.replace(/^\d+/, '').replace(/_/g, ' ').trim();
        const numMatch = cat.match(/^(\d+)/);
        const prefix = numMatch ? `[${numMatch[1]}] ` : '';

        // Guardar mapeos globales para salto garantizado
        window.allCategoriesBySlug[catSlug] = cat;
        if (numMatch) {
            const dec = numMatch[1].charAt(0);
            if (!window.decadeFirstCategory[dec]) {
                window.decadeFirstCategory[dec] = cat;
            }
        }
        if (cat.toUpperCase().includes('B2B MAGNA') && !window.b2bCategoryName) {
            window.b2bCategoryName = cat;
        }
        if ((cat.toUpperCase().includes('SELLOS') || cat.toUpperCase().includes('CINCELADA')) && !window.sellosCategoryName) {
            window.sellosCategoryName = cat;
        }

        // 1. Añadir al selector desplegable
        const opt = document.createElement('option');
        opt.value = catSlug;
        opt.textContent = `${prefix}${cleanName || cat} (${count} obras)`;
        select.appendChild(opt);

        // 2. Añadir ficha al panel estilo Memorándum
        const chip = document.createElement('div');
        chip.className = 'memo-style-chip';
        chip.onclick = () => {
            window.jumpToSelectedStyle(catSlug);
            window.toggleMemoIndex(false);
        };

        chip.innerHTML = `
            <span class="memo-chip-title">${prefix}<strong>${cleanName || cat}</strong></span>
            <span class="memo-chip-count">${count}</span>
        `;
        memoGrid.appendChild(chip);
    });

    // 3. Listener para botón flotante "Volver Arriba"
    const backBtn = document.getElementById('btn-back-to-top');
    if (backBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 350) {
                backBtn.style.display = 'flex';
            } else {
                backBtn.style.display = 'none';
            }
        });
    }
}

window.jumpToSelectedStyle = function(catSlug) {
    if (!catSlug) return;
    if (catSlug === 'ALL') {
        window.location.href = 'index.html';
        return;
    }
    const target = document.getElementById(catSlug);
    if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(() => {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
    } else {
        // Si no existe en el DOM actual (vista filtrada), navegar a esa categoría
        const targetCat = window.allCategoriesBySlug ? window.allCategoriesBySlug[catSlug] : null;
        if (targetCat) {
            window.location.href = `index.html?category=${encodeURIComponent(targetCat)}`;
        }
    }
    const select = document.getElementById('quick-style-select');
    if (select) {
        setTimeout(() => { select.value = catSlug; }, 500);
    }
};

window.jumpToDecade = function(decadeDigit) {
    const sections = document.querySelectorAll('.category-section');
    for (const sec of sections) {
        if (sec.dataset.decade === String(decadeDigit)) {
            sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
            setTimeout(() => {
                sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 300);
            return;
        }
    }
    // Si no está en el DOM actual (porque la página está filtrada a una categoría)
    const targetCat = window.decadeFirstCategory ? window.decadeFirstCategory[String(decadeDigit)] : null;
    if (targetCat) {
        window.location.href = `index.html?category=${encodeURIComponent(targetCat)}`;
    }
};

window.jumpToB2B = function() {
    const b2bSec = document.querySelector('.category-section[data-is-b2b="true"]');
    if (b2bSec) {
        b2bSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(() => {
            b2bSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
    } else {
        const b2bCat = window.b2bCategoryName || 'B2B Magna (Fuera de Web)';
        window.location.href = `index.html?category=${encodeURIComponent(b2bCat)}`;
    }
};

window.jumpToSellos = function() {
    const sellosSec = document.querySelector('.category-section[data-is-sellos="true"]');
    if (sellosSec) {
        sellosSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(() => {
            sellosSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
    } else {
        const sellosCat = window.sellosCategoryName || '1000 SELLOS MAGICOS';
        window.location.href = `index.html?category=${encodeURIComponent(sellosCat)}`;
    }
};

window.toggleMemoIndex = function(forceState) {
    const panel = document.getElementById('memo-index-panel');
    if (!panel) return;
    if (typeof forceState === 'boolean') {
        panel.style.display = forceState ? 'block' : 'none';
    } else {
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    }
    if (panel.style.display === 'block') {
        panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
};
