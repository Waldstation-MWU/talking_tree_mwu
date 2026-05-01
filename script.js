/**
 * Talking Tree – MWU Ebersberg
 * Haupt-Logikdatei für Navigation und Interaktion
 */

/**
 * Zeigt eine bestimmte Sektion an und blendet alle anderen aus.
 * @param {string} id - Die ID der anzuzeigenden Section
 * @param {HTMLElement} element - Das angeklickte Menü-Element (optional)
 */
function show(id, element) {
    // 1. Alle Sektionen im Hauptbereich finden und verstecken
    const sections = document.querySelectorAll('.main-content > section');
    sections.forEach(section => {
        section.classList.add('hidden');
    });

    // 2. Die gewünschte Sektion anzeigen
    const targetSection = document.getElementById(id);
    if (targetSection) {
        targetSection.classList.remove('hidden');
    }

    // 3. Sidebar-Menü Status aktualisieren (active-Klasse)
    if (element) {
        document.querySelectorAll('.menu-item').forEach(item => {
            item.classList.remove('active');
        });
        element.classList.add('active');
    }

    // 4. Seite sanft nach oben scrollen
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Spezielle Navigation für Buttons innerhalb des Contents (z.B. Hero-Button)
 */
function goToLive() {
    // Sucht den Live-Daten Button im Menü und simuliert den Klick
    const liveMenuItem = document.querySelector('[onclick*="live"]');
    if (liveMenuItem) {
        show('live', liveMenuItem);
    } else {
        show('live');
    }
}

/**
 * Login-Logik für das Datenarchiv
 */
function login() {
    const pwField = document.getElementById("pw");
    const loginBox = document.getElementById("loginBox");
    const dataContent = document.getElementById("dataContent");
    const errorMsg = document.getElementById("loginError");

    // Das Passwort (wie in der ursprünglichen Datei)
    if (pwField.value === "MWU_Talking!Tree1") {
        loginBox.classList.add("hidden");
        dataContent.classList.remove("hidden");
        if (errorMsg) errorMsg.style.display = "none";
    } else {
        if (errorMsg) {
            errorMsg.style.display = "block";
        } else {
            alert("Falsches Passwort!");
        }
    }
}

/**
 * Bild-Modal / Dialog Steuerung
 * Öffnet ein Bild in Großansicht
 */
function openImg(src) {
    const dialog = document.getElementById("imgDialog");
    const bigImg = document.getElementById("bigImg");
    
    if (dialog && bigImg) {
        bigImg.src = src;
        dialog.showModal();
    }
}

/**
 * Tab-Steuerung für die Messreihen
 */
function showTab(tabId, btn) {
    // Alle Tab-Inhalte verstecken
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.add('hidden');
    });
    
    // Gewünschten Tab anzeigen
    const target = document.getElementById(tabId);
    if (target) target.classList.remove('hidden');

    // Button-Styling anpassen
    if (btn) {
        const parent = btn.parentElement;
        parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    }
}

// Initialisierung beim Laden der Seite
document.addEventListener('DOMContentLoaded', () => {
    console.log("Talking Tree Dashboard bereit.");
});

// Funktion zum Öffnen der Lightbox
function openLightbox(event) {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    
    // Setzt die Bildquelle des Overlays auf die Quelle des geklickten Bildes
    lightboxImg.src = event.target.src;
    lightbox.style.display = 'flex';
}

// Funktion zum Schließen
function closeLightbox() {
    document.getElementById('lightbox').style.display = 'none';
}

// Automatische Zuweisung an alle Bilder mit der Klasse .responsive-img oder .responsive-img-styled
document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll('.responsive-img, .responsive-img-styled');
    images.forEach(img => {
        img.addEventListener('click', openLightbox);
    });
});