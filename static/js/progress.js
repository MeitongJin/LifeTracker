document.addEventListener('DOMContentLoaded', function () {
    const exerciseCtx = document.getElementById('exerciseChart').getContext('2d');
    const waterCtx = document.getElementById('waterChart').getContext('2d');
    const sleepCtx = document.getElementById('sleepChart').getContext('2d');
    const screenCtx = document.getElementById('screenChart').getContext('2d');
  
    const exerciseData = {
      labels: exercise_labels,
      datasets: [{
        label: 'Exercise (hours)',
        data: exercise_data,
        backgroundColor: '#4caf50',
      }]
    };
  
    const waterData = {
      labels: water_labels,
      datasets: [{
        label: 'Water (liters)',
        data: water_data,
        borderColor: '#42a5f5',
        backgroundColor: 'rgba(66, 165, 245, 0.2)',
        fill: true,
      }]
    };
  
    const sleepData = {
      labels: sleep_labels,
      datasets: [{
        label: 'Sleep (hours)',
        data: sleep_data,
        borderColor: '#ffeb3b',
        backgroundColor: 'rgba(255, 235, 59, 0.2)',
        fill: true,
      }]
    };
  
    const screenData = {
      labels: screen_labels,
      datasets: [{
        label: 'Screen Time (hours)',
        data: screen_data,
        borderColor: '#e91e63',
        backgroundColor: 'rgba(233, 30, 99, 0.2)',
        fill: true,
      }]
    };
  
    new Chart(exerciseCtx, {
      type: 'bar',
      data: exerciseData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            beginAtZero: true
          }
        }
      }
    });
  
    new Chart(waterCtx, {
      type: 'doughnut',
      data: waterData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    });
  
    new Chart(sleepCtx, {
      type: 'line',
      data: sleepData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    });
  
    new Chart(screenCtx, {
      type: 'pie',
      data: screenData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    });
  });