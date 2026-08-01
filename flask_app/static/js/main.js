//  THEME 
const body = document.body;
const themeBtn = document.getElementById('theme-toggle');

// Load saved theme
if (localStorage.getItem('theme') === 'light') {
  body.classList.add('light');
  if (themeBtn) themeBtn.textContent = '☀️';
}

if (themeBtn) {
  themeBtn.addEventListener('click', () => {
    body.classList.toggle('light');
    const isLight = body.classList.contains('light');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    themeBtn.textContent = isLight ? '☀️' : '🌙';
  });
}

//  FONT 
const fontSelect = document.getElementById('font-select');

// Load saved font
const savedFont = localStorage.getItem('font') || 'font-inter';
body.classList.add(savedFont);
if (fontSelect) fontSelect.value = savedFont;

if (fontSelect) {
  fontSelect.addEventListener('change', () => {
    body.classList.remove('font-inter', 'font-mono', 'font-serif');
    body.classList.add(fontSelect.value);
    localStorage.setItem('font', fontSelect.value);
  });
}

//  FORM LOADER 
const form = document.querySelector('form');
const loader = document.querySelector('.loader');
const submitBtn = document.querySelector('.btn[type="submit"]');

if (form && loader) {
  form.addEventListener('submit', () => {
    loader.classList.add('active');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Analyzing...';
    }
  });
}

//  SCROLL ANIMATION 
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.feature-card, .history-card').forEach(card => {
  card.style.opacity = '0';
  card.style.transform = 'translateY(16px)';
  card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
  observer.observe(card);
});

//  ACTIVE NAV 
document.querySelectorAll('.nav-links a').forEach(link => {
  if (link.href === window.location.href) {
    link.style.color = 'var(--text)';
  }
});

//  AUTO HIDE FLASH
const flash = document.querySelector('.flash');
if (flash) {
  setTimeout(() => {
    flash.style.transition = 'opacity 0.5s';
    flash.style.opacity = '0';
    setTimeout(() => flash.remove(), 500);
  }, 3000);
}