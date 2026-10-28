/**
 * SHOPPING CART LOGIC
 * Uses LocalStorage to persist items.
 */

const CART_KEY = 'tu_arte_cart';

// --- Core Functions ---

function getCart() {
    const json = localStorage.getItem(CART_KEY);
    return json ? JSON.parse(json) : [];
}

/**
 * Calculates discounts and promotions.
 * Promo: Buy 3, get 1 free (cheapest one is free).
 */
function calculateTotals() {
    const cart = getCart();
    let subtotal = 0;
    let discount = 0;

    // Parse prices
    const itemsWithPrice = cart.map(item => {
        let priceStr = item.price || '0';
        let clean = priceStr.replace('€', '').replace('.', '').replace(',', '.');
        let price = parseFloat(clean) || 0;
        return { ...item, numericPrice: price };
    });

    itemsWithPrice.sort((a, b) => b.numericPrice - a.numericPrice);

    // Apply 3+1 Promo
    const freeItemsCount = Math.floor(itemsWithPrice.length / 4);
    for (let i = 0; i < itemsWithPrice.length; i++) {
        subtotal += itemsWithPrice[i].numericPrice;
        // The last N cheapest items are free
        if (i >= itemsWithPrice.length - freeItemsCount) {
            discount += itemsWithPrice[i].numericPrice;
        }
    }

    return {
        subtotal: subtotal,
        discount: discount,
        total: subtotal - discount
    };
}

function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateCartCount();
    window.dispatchEvent(new Event('cartUpdated'));
}

function addToCart(item) {
    const cart = getCart();
    const exists = cart.find(i => i.id === item.id);
    if (!exists) {
        cart.push(item);
        saveCart(cart);
        return true;
    }
    return false;
}

function removeFromCart(id) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== id);
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateCartCount();
    window.dispatchEvent(new Event('cartUpdated'));
}

function clearCart() {
    localStorage.removeItem(CART_KEY);
    updateCartCount();
    window.dispatchEvent(new Event('cartUpdated'));
}

function updateCartCount() {
    const cart = getCart();
    const count = cart.length;
    const badges = document.querySelectorAll('.cart-badge');
    badges.forEach(el => {
        if (count > 0) {
            el.innerText = count;
            el.style.display = 'inline-block';
        } else {
            el.innerText = '';
            el.style.display = 'none';
        }
    });
}

/**
 * Universal Mobile Navigation
 * Garantiza menú hamburguesa y carrito táctil en todas las páginas de la galería.
 */
window.toggleMobileNav = function(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    const navLinks = document.getElementById('main-nav-links') || document.querySelector('.nav-links');
    const toggleBtn = document.getElementById('mobile-menu-toggle');
    if (!navLinks) return;
    const isOpen = navLinks.classList.toggle('open');
    if (toggleBtn) {
        toggleBtn.classList.toggle('open', isOpen);
        toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    }
};

function initUniversalMobileNav() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelector('.nav-links');
    if (!navbar || !navLinks) return;

    let mobileActions = navbar.querySelector('.navbar-mobile-actions');
    let toggleBtn = document.getElementById('mobile-menu-toggle');

    if (!mobileActions) {
        mobileActions = document.createElement('div');
        mobileActions.className = 'navbar-mobile-actions';
        
        const inSubdir = window.location.pathname.includes('/cuadroteca/') || window.location.pathname.includes('/visor/');
        const cartHref = inSubdir ? '../carrito.html' : 'carrito.html';

        mobileActions.innerHTML = `
            <a href="${cartHref}" class="mobile-cart-btn" aria-label="Ver Carrito">
                🛒 <span class="cart-badge"></span>
            </a>
            <button class="nav-toggle-btn" id="mobile-menu-toggle" aria-label="Abrir menú de navegación" aria-expanded="false" onclick="toggleMobileNav(event)">
                <span class="bar bar-1"></span>
                <span class="bar bar-2"></span>
                <span class="bar bar-3"></span>
            </button>
        `;
        navbar.insertBefore(mobileActions, navLinks);
        toggleBtn = mobileActions.querySelector('#mobile-menu-toggle');
    }

    if (toggleBtn && !toggleBtn.getAttribute('onclick')) {
        toggleBtn.setAttribute('onclick', 'toggleMobileNav(event)');
    }

    if (!navLinks.dataset.closeBound) {
        navLinks.dataset.closeBound = 'true';
        // Cerrar al pulsar un enlace
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('open');
                const btn = document.getElementById('mobile-menu-toggle');
                if (btn) {
                    btn.classList.remove('open');
                    btn.setAttribute('aria-expanded', 'false');
                }
            });
        });

        // Cerrar al pulsar fuera del menú
        document.addEventListener('click', (e) => {
            const btn = document.getElementById('mobile-menu-toggle');
            if (navLinks.classList.contains('open')) {
                if (!navLinks.contains(e.target) && (!btn || !btn.contains(e.target))) {
                    navLinks.classList.remove('open');
                    if (btn) {
                        btn.classList.remove('open');
                        btn.setAttribute('aria-expanded', 'false');
                    }
                }
            }
        });
    }
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
    initUniversalMobileNav();
});
