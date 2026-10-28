document.addEventListener('DOMContentLoaded', init);

// Global Navigation State
let currentRoom = 1;
let currentZ = 0;      // Camera depth position
let targetZ = 0;       // Target camera depth for smooth interpolation
let currentYaw = 0;    // Horizontal camera rotation (looking around)
let targetYaw = 0;     // Target horizontal rotation
let currentPitch = 0;  // Vertical camera rotation
let targetPitch = 0;   // Target vertical rotation
const stepSize = 120;  // How fast scroll moves the camera
let maxDepth = 4000;   // Calculated based on number of paintings in room
const wallZGap = 800;  // Distance between paintings on the same wall
let isWelcomeActive = true;

// Room Database Configuration
const roomConfigs = {
    1: {
        name: "Recibidor Brutalista (Carboneras 1996)",
        categories: ["00 EDUSSE"],
        limit: 8,
        label: "Sala 1: Recibidor"
    },
    2: {
        name: "La Gran Rotonda (Galería Semicircular)",
        categories: ["01 EXP NEOCIRC"],
        limit: 8,
        label: "Sala 2: Rotonda"
    },
    3: {
        name: "Gran Galería de Columnas (Sala Cubista)",
        categories: ["02 CUBESSE STILO"],
        limit: 8,
        label: "Sala 3: Columnas"
    },
    4: {
        name: "Ala Monumentos (Muro Amarillo Mostaza)",
        categories: ["03 EXPNEOPLUS"],
        limit: 8,
        label: "Sala 4: Monumentos"
    },
    5: {
        name: "Ala Extrema Izquierda (Colección Externa)",
        categories: ["48 BESSELUXY L"],
        limit: 6,
        label: "Sala 5: Col. Externa"
    },
    6: {
        name: "Ala Rústica (Gabinete de Dibujo)",
        categories: ["05 PLUMINK", "36 LINEART"],
        limit: 8,
        label: "Sala 6: Ala Rústica"
    },
    7: {
        name: "Gran Hall de Lujo (Obras de Autor Premium)",
        categories: ["EXCLUSIVO"], // Special filter for luxury works
        limit: 6,
        label: "Sala 7: Atrio de Lujo"
    },
    8: {
        name: "Ala Extrema Derecha (Sala VIP / Esculturas)",
        categories: ["22 NEO-LUMINA"],
        limit: 6,
        label: "Sala 8: Sala VIP"
    }
};

// Custom Exclusive/Luxury Artworks for Room 7
const exclusiveArtworks = [
    {
        id: "lux_001",
        title: "La Botella De Los Astros (Oro Premium)",
        category: "00 EDUSSE",
        src: "assets/00EDUSSE/La Botella de los Astros.png",
        description: "Una de las obras más exclusivas y personales del autor. Edición especial de colección que representa el cosmos interior embotellado sobre lienzo.",
        price: "950",
        size: "100x100 cm"
    },
    {
        id: "lux_002",
        title: "Cadillac 1982 (Edición de Honor)",
        category: "Colección Privada",
        src: "edu_CADILLAC_1982.png", // High-res master asset in directory
        description: "Pieza magistral que plasma la nostalgia retro-futurista de 1982 en un Cadillac de ensueño. Detalle y textura inigualables.",
        price: "1850",
        size: "150x100 cm"
    },
    {
        id: "lux_003",
        title: "Deidad Cuántica En Oro",
        category: "Quantum Deities",
        src: "assets/00EDUSSE/00edusse_003.png",
        description: "Pieza de coleccionista. Representación abstracta cuántica del guardián eterno bajo una iluminación mística.",
        price: "1200",
        size: "120x80 cm"
    }
];

function init() {
    console.log("Iniciando Sala Virtual 3D Multi-Sala...");
    
    // 1. Visitor Counter
    incrementVisitorCounter();

    // 2. Setup Welcome Screen
    setupWelcomeScreen();
    
    // 3. Setup Navigation & Room transitions
    setupNavigation();
    setupMinimap();
    setupDetailPanel();
    
    // 4. Load initial room (Room 1)
    loadRoom(1);
    
    // 5. Start smooth animation loop
    animateCamera();
}

function setupWelcomeScreen() {
    const welcome = document.getElementById('welcome-screen');
    const startBtn = document.getElementById('btn-start-visit');
    
    if (startBtn && welcome) {
        startBtn.addEventListener('click', () => {
            welcome.classList.add('hidden');
            isWelcomeActive = false;
            // Unmute/play background sounds here if desired in the future
        });
    }
}

function loadRoom(roomId) {
    if (!roomConfigs[roomId]) return;
    
    const fadeOverlay = document.getElementById('room-fade-overlay');
    if (fadeOverlay) {
        fadeOverlay.classList.add('fading');
    }
    
    setTimeout(() => {
        currentRoom = roomId;
        currentZ = 0;
        targetZ = 0;
        currentYaw = 0;
        targetYaw = 0;
        currentPitch = 0;
        targetPitch = 0;
        
        // Update room name in header
        const roomNameEl = document.getElementById('current-room-name');
        if (roomNameEl) {
            roomNameEl.innerText = roomConfigs[roomId].name;
        }
        
        // Update viewport class to morph styling (walls, ceiling, floor)
        const viewport = document.getElementById('viewport');
        if (viewport) {
            viewport.className = `viewport-3d room-style-${roomId}`;
        }
        
        // Render room paintings
        renderRoomArtworks(roomId);
        
        // Highlight room on minimap SVG
        updateMinimapSelection(roomId);
        
        // Fade in
        if (fadeOverlay) {
            fadeOverlay.classList.remove('fading');
        }
    }, 450);
}

function renderRoomArtworks(roomId) {
    const config = roomConfigs[roomId];
    let artworks = [];
    
    // Filter logic
    if (config.categories.includes("EXCLUSIVO")) {
        artworks = [...exclusiveArtworks];
    } else {
        if (typeof artworkData !== 'undefined') {
            artworks = artworkData.filter(art => {
                if (!art || !art.category) return false;
                // Skip NFT stamps
                if (art.category.includes("SELLOS") || art.category.includes("CINCELADA")) return false;
                return config.categories.includes(art.category);
            });
        }
    }
    
    // Fallback if no artworks found
    if (artworks.length === 0 && typeof artworkData !== 'undefined') {
        artworks = artworkData.slice(0, 6);
    }
    
    // Limit paintings count for room size
    artworks = artworks.slice(0, config.limit);
    
    const hallway = document.getElementById('hallway');
    if (!hallway) return;
    
    // Clean up dynamic objects in the hallway
    const dynamicElements = hallway.querySelectorAll('.exhibit-frame, .wall-spotlight-glow, .dynamic-wall');
    dynamicElements.forEach(el => el.remove());
    
    let leftCount = 0;
    let rightCount = 0;
    
    // Custom geometries based on Room ID
    if (false) {
        // --- 1. CIRCULAR ROOM GEOMETRY (DEACTIVATED FOR SINGLE ROOM VOLUME TEST) ---
        const totalArtworks = artworks.length;
        const roomCenterZ = -1200;
        const radius = 950;
        
        // Create 12 dynamic wall panels to form the cylinder
        const wallPanelsCount = 12;
        for (let i = 0; i < wallPanelsCount; i++) {
            const wallPanel = document.createElement('div');
            wallPanel.className = 'wall-panel-3d dynamic-wall';
            
            const angleDegrees = i * (360 / wallPanelsCount);
            const angleRad = (angleDegrees * Math.PI) / 180;
            
            const xPos = radius * Math.sin(angleRad);
            const zPos = roomCenterZ + (radius * Math.cos(angleRad));
            const rotateYVal = -angleDegrees;
            
            wallPanel.style.transform = `translate3d(${xPos}px, 0px, ${zPos}px) rotateY(${rotateYVal}deg)`;
            hallway.appendChild(wallPanel);
        }
        
        // Position artworks in a circle slightly inside the walls (radius 910)
        artworks.forEach((art, index) => {
            const frame = document.createElement('div');
            frame.className = 'exhibit-frame';
            frame.dataset.id = art.id;
            
            frame.innerHTML = `
                <div class="painting-mount">
                    <img src="${art.src}" alt="${art.title}">
                    <div class="painting-floor-reflection">
                        <img src="${art.src}" style="border:none; outline:none; box-shadow:none;">
                    </div>
                </div>
                <div class="exhibit-title">${art.title}</div>
                <div class="exhibit-price">${art.price ? (art.price.toString().includes('€') || art.price.toString().includes('$') ? art.price : art.price + '€') : 'Consultar'}</div>
            `;
            
            // Distribute evenly in a circle around Z = -1200px
            const angleDegrees = (index * (360 / totalArtworks)) + (roomId === 7 ? 60 : 22.5); // Offset slightly
            const angleRad = (angleDegrees * Math.PI) / 180;
            const artworkRadius = 910;
            
            const xPos = artworkRadius * Math.sin(angleRad);
            const zPos = roomCenterZ + (artworkRadius * Math.cos(angleRad));
            const rotateYVal = -angleDegrees; // Face the center of the circle
            
            frame.dataset.z = zPos;
            frame.style.transform = `translate3d(${xPos}px, 0px, ${zPos}px) rotateY(${rotateYVal}deg)`;
            
            // Hover effect (pop inward to the center)
            frame.addEventListener('mouseenter', () => {
                const popRadius = artworkRadius - 40;
                const popX = popRadius * Math.sin(angleRad);
                const popZ = roomCenterZ + (popRadius * Math.cos(angleRad));
                frame.style.transform = `translate3d(${popX}px, 0px, ${popZ}px) rotateY(${rotateYVal}deg) scale(1.03)`;
            });
            
            frame.addEventListener('mouseleave', () => {
                frame.style.transform = `translate3d(${xPos}px, 0px, ${zPos}px) rotateY(${rotateYVal}deg)`;
            });
            
            frame.addEventListener('click', () => {
                zoomToExhibit(art, zPos);
            });
            
            hallway.appendChild(frame);
        });
        
        maxDepth = 2400;
        
        // Hide the flat back wall in the circular room to maintain open feel
        const backWall = document.getElementById('back-wall');
        if (backWall) {
            backWall.style.transform = `translate3d(0, 0, -3500px) scale(0)`;
        }
        
    } else {
        // --- 2. RECTANGULAR/WIDE HALLWAY GEOMETRY (ALL OTHER ROOMS) ---
        // S7 (Atrio de Lujo) is extremely wide (2400px wide)
        // S3 and S4 are moderately wide (1500px)
        let wallWidth = 485;
        if (roomId === 7) wallWidth = 1100;
        else if (roomId === 3 || roomId === 4 || roomId === 8) wallWidth = 700;
        
        // Generate dynamic concrete pilasters for Room 1 to add real 3D volume
        if (roomId === 1) {
            const zPositions = [-100, -900, -1700, -2500, -3300];
            zPositions.forEach(zVal => {
                // Left concrete pilaster
                const pLeft = document.createElement('div');
                pLeft.className = 'pilaster-3d dynamic-wall';
                pLeft.style.transform = `translate3d(-468px, 0px, ${zVal}px) rotateY(90deg)`;
                hallway.appendChild(pLeft);
                
                // Right concrete pilaster
                const pRight = document.createElement('div');
                pRight.className = 'pilaster-3d dynamic-wall';
                pRight.style.transform = `translate3d(468px, 0px, ${zVal}px) rotateY(-90deg)`;
                hallway.appendChild(pRight);
            });
        }
        
        artworks.forEach((art, index) => {
            const isLeft = index % 2 === 0;
            
            const frame = document.createElement('div');
            frame.className = 'exhibit-frame';
            frame.dataset.id = art.id;
            
            const isFloorEasel = (roomId === 5 && index >= 3);
            
            frame.innerHTML = `
                <div class="painting-mount" style="${isFloorEasel ? 'border-width: 4px; padding: 10px; background: #fafafa;' : ''}">
                    <img src="${art.src}" alt="${art.title}">
                    <div class="painting-floor-reflection">
                        <img src="${art.src}" style="border:none; outline:none; box-shadow:none;">
                    </div>
                </div>
                <div class="exhibit-title">${art.title}</div>
                <div class="exhibit-price">${art.price ? (art.price.toString().includes('€') || art.price.toString().includes('$') ? art.price : art.price + '€') : 'Consultar'}</div>
            `;
            
            const zPos = isLeft ? (-300 - (leftCount * wallZGap)) : (-700 - (rightCount * wallZGap));
            frame.dataset.z = zPos;
            
            const spotlight = document.createElement('div');
            spotlight.className = 'wall-spotlight-glow';
            
            const xOffset = isLeft ? -wallWidth : wallWidth;
            const rotateYVal = isLeft ? 90 : -90;
            const yOffset = isFloorEasel ? 120 : 0;
            
            frame.style.transform = `translate3d(${xOffset}px, ${yOffset}px, ${zPos}px) rotateY(${rotateYVal}deg)`;
            spotlight.style.transform = `translate3d(${xOffset}px, -400px, ${zPos}px) rotateY(${rotateYVal}deg)`; // Aligned at top of wall
            
            if (isLeft) {
                leftCount++;
            } else {
                rightCount++;
            }
            
            frame.addEventListener('mouseenter', () => {
                const popX = isLeft ? -(wallWidth - 25) : (wallWidth - 25);
                frame.style.transform = `translate3d(${popX}px, ${yOffset}px, ${zPos}px) rotateY(${rotateYVal}deg) scale(1.03)`;
            });
            frame.addEventListener('mouseleave', () => {
                frame.style.transform = `translate3d(${xOffset}px, ${yOffset}px, ${zPos}px) rotateY(${rotateYVal}deg)`;
            });
            
            frame.addEventListener('click', () => {
                zoomToExhibit(art, zPos);
            });
            
            if (roomId !== 2) {
                hallway.appendChild(spotlight);
            }
            hallway.appendChild(frame);
        });
        
        const totalCount = Math.max(leftCount, rightCount);
        maxDepth = (totalCount * wallZGap) + 1200;
        
        const backWall = document.getElementById('back-wall');
        if (backWall) {
            backWall.style.transform = `translate3d(0, 0, -${maxDepth}px) scale(1)`;
            const label = document.getElementById('back-wall-label');
            if (label) {
                label.innerText = `Acceso a otras salas mediante el plano`;
            }
        }
    }
}

function zoomToExhibit(art, zPos) {
    // Scroll camera directly in front of the painting
    targetZ = -zPos - 180;
    
    setTimeout(() => {
        openDetailModal(art);
    }, 600);
}

// --- SMOOTH CAMERA LOOP ---
function animateCamera() {
    if (!isWelcomeActive) {
        currentZ += (targetZ - currentZ) * 0.15;
        currentYaw += (targetYaw - currentYaw) * 0.15;
        currentPitch += (targetPitch - currentPitch) * 0.15;
        
        const hallway = document.getElementById('hallway');
        if (hallway) {
            // Apply camera rotations (pitch/yaw) and translation Z
            hallway.style.transform = `rotateX(${-currentPitch}deg) rotateY(${-currentYaw}deg) translate3d(0, 0, ${currentZ}px)`;
        }
    }
    requestAnimationFrame(animateCamera);
}

// --- NAV & CONTROL LISTENERS ---
function setupNavigation() {
    // 1. Wheel Scroll (Forward/Backward movement)
    window.addEventListener('wheel', (e) => {
        if (isWelcomeActive) return;
        e.preventDefault();
        targetZ += e.deltaY * (stepSize / 100);
        clampTargetZ();
    }, { passive: false });
    
    // 2. Keyboard Arrows (Forward/Backward movement)
    window.addEventListener('keydown', (e) => {
        if (isWelcomeActive) return;
        if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") {
            targetZ += stepSize;
        } else if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") {
            targetZ -= stepSize;
        }
        clampTargetZ();
    });
    
    // 3. Mouse Drag (Look Around / 360 degree rotation)
    let isDragging = false;
    let startX = 0;
    let startY = 0;
    let baseYaw = 0;
    let basePitch = 0;
    
    window.addEventListener('mousedown', (e) => {
        if (isWelcomeActive) return;
        // Ignore if clicking UI overlays
        if (e.target.closest('#floor-controls, #minimap-container, .gallery-header, #exhibit-detail-panel, .exhibit-frame')) return;
        
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        baseYaw = targetYaw;
        basePitch = targetPitch;
    });
    
    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        // Turn speed sensitivity
        targetYaw = baseYaw - (deltaX * 0.15); // Rotate left/right
        targetPitch = basePitch - (deltaY * 0.15); // Look up/down
        
        // Clamp vertical look (pitch) to avoid turning upside down
        if (targetPitch < -35) targetPitch = -35;
        if (targetPitch > 35) targetPitch = 35;
    });
    
    window.addEventListener('mouseup', () => {
        isDragging = false;
    });
    
    // 4. Touch Drag (Look Around for Mobile)
    let touchStartX = 0;
    let touchStartY = 0;
    
    window.addEventListener('touchstart', (e) => {
        if (isWelcomeActive) return;
        if (e.target.closest('#floor-controls, #minimap-container, .gallery-header, #exhibit-detail-panel, .exhibit-frame')) return;
        
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
        baseYaw = targetYaw;
        basePitch = targetPitch;
    });
    
    window.addEventListener('touchmove', (e) => {
        if (isWelcomeActive) return;
        if (e.target.closest('#floor-controls, #minimap-container, .gallery-header, #exhibit-detail-panel, .exhibit-frame')) return;
        e.preventDefault();
        
        const currentX = e.touches[0].clientX;
        const currentY = e.touches[0].clientY;
        
        const deltaX = currentX - touchStartX;
        const deltaY = currentY - touchStartY;
        
        targetYaw = baseYaw - (deltaX * 0.25);
        targetPitch = basePitch - (deltaY * 0.25);
        
        if (targetPitch < -35) targetPitch = -35;
        if (targetPitch > 35) targetPitch = 35;
    }, { passive: false });
    
    // 4. Street View controls
    const btnForward = document.getElementById('ctrl-forward');
    const btnBackward = document.getElementById('ctrl-backward');
    const btnLeft = document.getElementById('ctrl-turn-left');
    const btnRight = document.getElementById('ctrl-turn-right');
    
    if (btnForward) {
        btnForward.addEventListener('click', () => {
            // Walk forward or go to next central room if at end
            if (targetZ >= maxDepth - 600) {
                handleForwardTransition();
            } else {
                targetZ += stepSize * 4;
                clampTargetZ();
            }
        });
    }
    if (btnBackward) {
        btnBackward.addEventListener('click', () => {
            targetZ -= stepSize * 4;
            clampTargetZ();
        });
    }
    
    if (btnLeft) {
        btnLeft.addEventListener('click', () => {
            targetYaw -= 90; // Smoothly rotate view to the left by 90 degrees
        });
    }
    if (btnRight) {
        btnRight.addEventListener('click', () => {
            targetYaw += 90; // Smoothly rotate view to the right by 90 degrees
        });
    }
}

function handleForwardTransition() {
    if (currentRoom === 1) loadRoom(3);
    else if (currentRoom === 3) loadRoom(6);
    else if (currentRoom === 6) loadRoom(7);
}

function clampTargetZ() {
    if (targetZ < 0) targetZ = 0;
    if (targetZ > maxDepth - 450) targetZ = maxDepth - 450;
}

// --- MINIMAP FUNCTIONALITY ---
function setupMinimap() {
    const nodes = document.querySelectorAll('.map-node');
    nodes.forEach(node => {
        node.addEventListener('click', (e) => {
            const roomId = parseInt(node.getAttribute('data-room'), 10);
            if (roomId && roomId !== currentRoom) {
                loadRoom(roomId);
            }
        });
    });
}

function updateMinimapSelection(roomId) {
    const nodes = document.querySelectorAll('.map-node');
    nodes.forEach(node => {
        const id = parseInt(node.getAttribute('data-room'), 10);
        if (id === roomId) {
            node.classList.add('active-room');
        } else {
            node.classList.remove('active-room');
        }
    });
}

// --- DETAIL MODAL PANEL ---
let selectedExhibit = null;
function setupDetailPanel() {
    const modal = document.getElementById('exhibit-detail-panel');
    const closeBtn = document.getElementById('close-detail');
    
    if (closeBtn) {
        closeBtn.addEventListener('click', closeDetailModal);
    }
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeDetailModal();
        });
    }
}

function openDetailModal(item) {
    selectedExhibit = item;
    
    const modal = document.getElementById('exhibit-detail-panel');
    const img = document.getElementById('detail-img');
    const title = document.getElementById('detail-title');
    const cat = document.getElementById('detail-category');
    const price = document.getElementById('detail-price');
    const desc = document.getElementById('detail-desc');
    
    if (img) img.src = item.src;
    if (title) title.innerText = item.title;
    if (cat) cat.innerText = item.category || 'Galería';
    
    if (price) {
        const pVal = item.price ? item.price.toString() : 'Consultar';
        price.innerText = pVal.includes('€') || pVal.includes('$') || pVal.includes('Consultar') ? pVal : pVal + '€';
    }
    if (desc) desc.innerText = item.description || "Sin descripción disponible.";
    
    if (modal) modal.classList.add('active');
}

function closeDetailModal() {
    const modal = document.getElementById('exhibit-detail-panel');
    if (modal) modal.classList.remove('active');
    selectedExhibit = null;
}

window.comprarCuadro = function() {
    if (selectedExhibit) {
        const itemObj = {
            id: selectedExhibit.id,
            title: selectedExhibit.title,
            price: selectedExhibit.price,
            thumb: selectedExhibit.src
        };
        if (typeof addToCart === 'function') {
            const added = addToCart(itemObj);
            if (added) window.location.href = 'carrito.html';
            else alert('Esta obra ya está en tu carrito.');
        } else {
            alert('Error: el sistema de carrito no está disponible.');
        }
    }
};

window.probarCuadro = function() {
    if (selectedExhibit) {
        const viewerLink = `visor/index.html?img=${encodeURIComponent(selectedExhibit.src)}&title=${encodeURIComponent(selectedExhibit.title)}&category=${encodeURIComponent(selectedExhibit.category)}&id=${selectedExhibit.id}`;
        window.location.href = viewerLink;
    }
};

// --- VISITOR LOCAL STATS ---
function incrementVisitorCounter() {
    let visitsCuadroteca = parseInt(localStorage.getItem('visitas_cuadroteca') || '0', 10);
    let visitsVirtual = parseInt(localStorage.getItem('visitas_sala_virtual') || '0', 10);
    
    visitsVirtual += 1;
    localStorage.setItem('visitas_sala_virtual', visitsVirtual.toString());
    
    const footerStats = document.getElementById('footer-visitor-stats');
    if (footerStats) {
        footerStats.innerText = `Estadísticas de navegación local: Visitas a la Cuadroteca: ${visitsCuadroteca} | Visitas a la Sala Virtual: ${visitsVirtual}`;
    }
}
