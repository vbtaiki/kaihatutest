// ========================================
// バリューブックス 新評価制度
// インタラクション
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // スクロールアニメーション
    initScrollAnimations();
    
    // ヘッダーのスクロール効果
    initHeaderScroll();
    
    // FAQのスムーズな開閉
    initFAQ();
    
    // 給与表示：時給＋月給（目安）を同時表示
    initSalaryMonthlyPreview();
});

function initSalaryMonthlyPreview() {
    const monthlyEls = document.querySelectorAll('[data-hourly][data-hours]');
    if (!monthlyEls.length) return;

    function formatYen(value) {
        const n = Math.round(Number(value));
        return `${n.toLocaleString('ja-JP')}円`;
    }

    monthlyEls.forEach(el => {
        const hourly = Number(el.dataset.hourly);
        const isRangeMin = el.dataset.range === 'min';
        const hours = Number(el.dataset.hours);
        if (!Number.isFinite(hours) || hours <= 0) return;
        const value = hourly * hours;
        el.textContent = `${formatYen(value)}${isRangeMin ? '〜' : ''}`;
    });
}

// スクロールアニメーション
function initScrollAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, observerOptions);

    // アニメーション対象の要素
    const animatedElements = document.querySelectorAll(
        '.change-card, .work-card, .vision-card, .faq-item, .salary-step, .eval-card, .principle-list li'
    );

    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        observer.observe(el);
    });

    // スタイルを追加
    const style = document.createElement('style');
    style.textContent = `
        .is-visible {
            opacity: 1 !important;
            transform: translateY(0) !important;
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
    `;
    document.head.appendChild(style);
}

// ヘッダーのスクロール効果
function initHeaderScroll() {
    const header = document.querySelector('.header');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            header.style.boxShadow = '0 2px 20px rgba(0, 169, 157, 0.1)';
        } else {
            header.style.boxShadow = 'none';
        }

        lastScroll = currentScroll;
    }, { passive: true });
}

// FAQのアクセシビリティ向上
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const summary = item.querySelector('summary');
        
        summary.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                item.open = !item.open;
            }
        });
    });
}

// 給与の階段をクリックで詳細表示（将来の拡張用）
function initSalarySteps() {
    const steps = document.querySelectorAll('.salary-step');
    
    steps.forEach(step => {
        step.addEventListener('click', () => {
            steps.forEach(s => s.classList.remove('is-active'));
            step.classList.add('is-active');
        });
    });
}

// スムーズスクロール（ナビゲーション用）
function smoothScrollTo(targetId) {
    const target = document.getElementById(targetId);
    if (target) {
        const headerHeight = document.querySelector('.header').offsetHeight;
        const targetPosition = target.offsetTop - headerHeight - 20;
        
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }
}

// ページ読み込み完了時のアニメーション
window.addEventListener('load', () => {
    document.body.classList.add('is-loaded');
    
    // ヒーローセクションのアニメーション
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
        heroContent.style.opacity = '0';
        heroContent.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            heroContent.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            heroContent.style.opacity = '1';
            heroContent.style.transform = 'translateY(0)';
        }, 100);
    }
});
