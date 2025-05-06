document.addEventListener('DOMContentLoaded', function() {
    // Clear session on fresh page load
    if(performance.navigation.type === 1) {  // Type 1 = page reload
        fetch('/clear_reset_session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        }).then(() => {
            // Force page refresh after clearing session
            window.location.href = "{{ url_for('reset_password') }}";
        }).catch(err => console.error('Error clearing session:', err));
    }
    
    // Add click handler for resend code link
    document.querySelector('a[href*="resend"]')?.addEventListener('click', function(e) {
        e.preventDefault();
        const link = this;
        link.textContent = "Sending...";
        fetch(this.href)
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                }
            })
            .catch(err => console.error('Resend error:', err));
    });
});