const hour = new Date().getHours();
  document.getElementById('time-greeting').textContent = 
    hour < 12 ? 'Morning' : hour < 18 ? 'Afternoon' : 'Evening';