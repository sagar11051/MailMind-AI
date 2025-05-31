// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!mobileMenuButton.contains(event.target) && !mobileMenu.contains(event.target)) {
            mobileMenu.classList.add('hidden');
        }
    });
});

// Show loading overlay
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('hidden');
    }
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('hidden');
    }
}

// Handle form submissions with loading state
document.addEventListener('submit', function(event) {
    const form = event.target;
    if (form.matches('form')) {
        showLoading();
    }
});

// Handle AJAX form submissions
document.addEventListener('submit', async function(event) {
    const form = event.target;
    
    // Only handle forms with data-ajax="true"
    if (!form.matches('form[data-ajax="true"]')) {
        return;
    }
    
    event.preventDefault();
    showLoading();
    
    const formData = new FormData(form);
    const url = form.getAttribute('action') || window.location.href;
    const method = form.getAttribute('method') || 'POST';
    
    try {
        const response = await fetch(url, {
            method: method,
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Handle success
            if (form.dataset.success) {
                const successElement = document.querySelector(form.dataset.success);
                if (successElement) {
                    successElement.innerHTML = 'Success!';
                    successElement.classList.remove('hidden');
                    setTimeout(() => successElement.classList.add('hidden'), 3000);
                }
            }
            
            // Reset form if needed
            if (form.dataset.resetOnSuccess === 'true') {
                form.reset();
            }
            
            // Reload page or update UI as needed
            if (form.dataset.reloadOnSuccess === 'true') {
                window.location.reload();
            }
        } else {
            // Handle error
            console.error('Form submission error:', data);
            alert(data.message || 'An error occurred. Please try again.');
        }
    } catch (error) {
        console.error('Form submission error:', error);
        alert('An error occurred. Please check your connection and try again.');
    } finally {
        hideLoading();
    }
});

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    
    tooltipTriggers.forEach(trigger => {
        const tooltip = document.createElement('div');
        tooltip.className = 'hidden bg-gray-900 text-white text-xs rounded py-1 px-2 absolute z-50 whitespace-nowrap';
        tooltip.textContent = trigger.getAttribute('data-tooltip');
        document.body.appendChild(tooltip);
        
        const updateTooltipPosition = (event) => {
            const rect = trigger.getBoundingClientRect();
            tooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
            tooltip.style.left = `${rect.left + window.scrollX}px`;
        };
        
        trigger.addEventListener('mouseenter', () => {
            tooltip.classList.remove('hidden');
            updateTooltipPosition();
        });
        
        trigger.addEventListener('mouseleave', () => {
            tooltip.classList.add('hidden');
        });
        
        trigger.addEventListener('mousemove', updateTooltipPosition);
    });
});
