// スムーズスクロール
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            window.scrollTo({
                top: target.offsetTop - 60, // ナビゲーションバーの高さを考慮
                behavior: 'smooth'
            });
        }
    });
});

// スクロールアニメーション
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// アニメーション要素の監視を開始
document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.add('fade-in');
        observer.observe(section);
    });

    const cards = document.querySelectorAll('.skill-card, .project-card');
    cards.forEach(card => {
        card.classList.add('fade-in');
        observer.observe(card);
    });

    // プロジェクトページのナビゲーション
    const container = document.querySelector('.projects-container');
    const pages = document.querySelectorAll('.projects-page');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    let currentPage = 0;

    // ページ移動関数
    const goToPage = (pageIndex) => {
        currentPage = pageIndex;
        container.scrollTo({
            left: pages[pageIndex].offsetLeft,
            behavior: 'smooth'
        });

        // ドットの状態更新
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === pageIndex);
        });

        // ボタンの状態更新
        prevBtn.disabled = pageIndex === 0;
        nextBtn.disabled = pageIndex === pages.length - 1;
    };

    // イベントリスナーの設定
    prevBtn.addEventListener('click', () => {
        if (currentPage > 0) {
            goToPage(currentPage - 1);
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentPage < pages.length - 1) {
            goToPage(currentPage + 1);
        }
    });

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            goToPage(index);
        });
    });

    // 初期状態の設定
    prevBtn.disabled = true;
});

// Menu Toggle
const menuToggle = document.querySelector('.menu-toggle');
const navContent = document.querySelector('.nav-content');
const navLinks = document.querySelectorAll('.nav-link');

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('active');
    navContent.classList.toggle('active');
    document.body.classList.toggle('menu-open');
});

// Close menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        menuToggle.classList.remove('active');
        navContent.classList.remove('active');
        document.body.classList.remove('menu-open');
    });
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
    if (!navContent.contains(e.target) && !menuToggle.contains(e.target) && navContent.classList.contains('active')) {
        menuToggle.classList.remove('active');
        navContent.classList.remove('active');
        document.body.classList.remove('menu-open');
    }
});

// スムーズスクロール制御
let isScrolling = false;
let lastScrollTime = 0;
const scrollCooldown = 1000; // スクロールのクールダウン時間（ミリ秒）

window.addEventListener('wheel', (e) => {
    // モバイルデバイスではスクロール制御を行わない
    if (window.innerWidth < 768) return;

    const currentTime = Date.now();
    if (isScrolling || currentTime - lastScrollTime < scrollCooldown) {
        e.preventDefault();
        return;
    }

    const sections = document.querySelectorAll('section');
    const currentSection = Array.from(sections).find(section => {
        const rect = section.getBoundingClientRect();
        return rect.top <= 50 && rect.bottom > 50;
    });

    if (!currentSection) return;

    isScrolling = true;
    lastScrollTime = currentTime;

    const nextSection = e.deltaY > 0
        ? currentSection.nextElementSibling
        : currentSection.previousElementSibling;

    if (nextSection && nextSection.tagName === 'SECTION') {
        nextSection.scrollIntoView({ behavior: 'smooth' });
        setTimeout(() => {
            isScrolling = false;
        }, scrollCooldown);
    } else {
        isScrolling = false;
    }
}, { passive: false });
