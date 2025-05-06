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
        fetch('/clear_reset_session', {
            method: 'POST',
            credentials: 'same-origin'
        }).then(() => {
            window.location.href = "{{ url_for('reset_password') }}";
        });
    });
});