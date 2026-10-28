/**
 * ARTWORK PROTECTION SYSTEM v2
 * High-security layer to prevent image downloads.
 */
(function() {
    function protect() {
        const artworks = document.querySelectorAll('img, .artwork-overlay, .card-image, .art-image-wrapper');
        
        artworks.forEach(el => {
            // Disable right click
            el.oncontextmenu = function(e) {
                e.preventDefault();
                e.stopPropagation();
                alert("© Obra Protegida por EduArt. Para adquirir una licencia o copia limpia, contacta con el artista.");
                return false;
            };
            
            // Disable drag
            el.ondragstart = function() { return false; };
        });
    }

    // Run on load and every second to catch dynamic elements
    document.addEventListener('DOMContentLoaded', protect);
    setInterval(protect, 1000);

    // Global body protection for good measure
    document.body.oncontextmenu = function(e) {
        if (e.target.tagName === 'IMG' || e.target.closest('.art-card') || e.target.closest('.hero-image-container')) {
            e.preventDefault();
            return false;
        }
    };
})();
