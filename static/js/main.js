// Python Learning Adventure - Main JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-dismissible')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Progress bar animation
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-in-out';
            bar.style.width = width;
        }, 500);
    });

    // Level item hover effects
    const levelItems = document.querySelectorAll('.level-item');
    levelItems.forEach(item => {
        item.addEventListener('mouseenter', function () {
            if (!this.classList.contains('locked')) {
                this.classList.add('pulse');
            }
        });

        item.addEventListener('mouseleave', function () {
            this.classList.remove('pulse');
        });
    });
});

// Utility Functions
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    `;

    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    // Auto remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            const bsAlert = new bootstrap.Alert(notification);
            bsAlert.close();
        }
    }, duration);
}

function updatePlayerStats(playerData) {
    // Update player stats in the UI
    const levelElement = document.querySelector('.player-level');
    const xpElement = document.querySelector('.player-xp');
    const coinsElement = document.querySelector('.player-coins');
    const streakElement = document.querySelector('.player-streak');

    if (levelElement) levelElement.textContent = playerData.current_level;
    if (xpElement) xpElement.textContent = playerData.total_xp;
    if (coinsElement) coinsElement.textContent = playerData.coins;
    if (streakElement) streakElement.textContent = playerData.streak;

    // Update progress bar
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        const percentage = ((playerData.total_xp % 1000) / 1000) * 100;
        progressBar.style.width = `${percentage}%`;
    }
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function getTimeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
        return 'yesterday';
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else if (diffDays < 30) {
        const weeks = Math.floor(diffDays / 7);
        return `${weeks} week${weeks > 1 ? 's' : ''} ago`;
    } else {
        const months = Math.floor(diffDays / 30);
        return `${months} month${months > 1 ? 's' : ''} ago`;
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function () {
        showNotification('Copied to clipboard!', 'success', 2000);
    }, function (err) {
        console.error('Could not copy text: ', err);
        showNotification('Failed to copy to clipboard', 'danger', 2000);
    });
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/;
    return re.test(password);
}

// API Helper Functions
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const config = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }

        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// Game-specific functions
function unlockAchievement(achievementName) {
    showNotification(`🏆 Achievement Unlocked: ${achievementName}`, 'success', 5000);

    // Add sparkle effect
    const sparkles = document.createElement('div');
    sparkles.className = 'achievement-sparkles';
    sparkles.innerHTML = '✨🎉✨';
    sparkles.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 3rem;
        z-index: 10000;
        pointer-events: none;
        animation: sparkle 2s ease-out forwards;
    `;

    document.body.appendChild(sparkles);

    setTimeout(() => {
        if (sparkles.parentNode) {
            sparkles.remove();
        }
    }, 2000);
}

function levelUp(newLevel) {
    showNotification(`🌟 Level Up! You reached level ${newLevel}!`, 'success', 5000);

    // Add level up effect
    const levelUpEffect = document.createElement('div');
    levelUpEffect.className = 'level-up-effect';
    levelUpEffect.innerHTML = `
        <div class="level-up-text">
            <h2>LEVEL UP!</h2>
            <p>Level ${newLevel}</p>
        </div>
    `;
    levelUpEffect.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10001;
        animation: levelUpAnimation 3s ease-out forwards;
        color: white;
        text-align: center;
    `;

    document.body.appendChild(levelUpEffect);

    setTimeout(() => {
        if (levelUpEffect.parentNode) {
            levelUpEffect.remove();
        }
    }, 3000);
}

function updateStreak(streakCount) {
    if (streakCount > 0) {
        const streakElement = document.querySelector('.player-streak');
        if (streakElement) {
            streakElement.textContent = streakCount;
            streakElement.parentElement.classList.add('pulse');
            setTimeout(() => {
                streakElement.parentElement.classList.remove('pulse');
            }, 2000);
        }
    }
}

// Local Storage helpers
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

function loadFromLocalStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
        console.error('Error loading from localStorage:', error);
        return defaultValue;
    }
}

// Theme management
function setTheme(themeName) {
    document.body.className = `theme-${themeName}`;
    saveToLocalStorage('selectedTheme', themeName);
}

function loadSavedTheme() {
    const savedTheme = loadFromLocalStorage('selectedTheme', 'default');
    setTheme(savedTheme);
}

// Sound effects (optional)
function playSound(soundName) {
    // Only play if user has enabled sounds
    const soundEnabled = loadFromLocalStorage('soundEnabled', true);
    if (!soundEnabled) return;

    try {
        const audio = new Audio(`/static/sounds/${soundName}.mp3`);
        audio.volume = 0.3;
        audio.play().catch(e => {
            // Ignore errors if audio can't play
            console.log('Audio play failed:', e);
        });
    } catch (error) {
        console.log('Sound effect not available:', soundName);
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function (e) {
    // ESC to close modals
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) bsModal.hide();
        });
    }

    // Ctrl/Cmd + Enter to submit forms
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeForm = document.querySelector('form:focus-within');
        if (activeForm) {
            const submitBtn = activeForm.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.click();
            }
        }
    }
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes sparkle {
        0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
        50% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
    }
    
    @keyframes levelUpAnimation {
        0% { transform: scale(0); opacity: 0; }
        20% { transform: scale(1.1); opacity: 1; }
        80% { transform: scale(1); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0; }
    }
    
    .level-up-text h2 {
        font-size: 4rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .level-up-text p {
        font-size: 2rem;
        opacity: 0.8;
    }
`;
document.head.appendChild(style);

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    loadSavedTheme();
});

// Export functions for use in other scripts
window.GameUtils = {
    showNotification,
    updatePlayerStats,
    formatNumber,
    getTimeAgo,
    copyToClipboard,
    apiRequest,
    unlockAchievement,
    levelUp,
    updateStreak,
    playSound,
    saveToLocalStorage,
    loadFromLocalStorage,
    setTheme
};
