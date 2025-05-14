function initializeExerciseChart(data, labels) {
    const ctx = document.getElementById('exercise-chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Exercise (mins)',
                data: data,
                backgroundColor: '#4B9CD3'
            }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
              title: {
                  display: true,
                  text: 'Exercise'
              }
          }
      } 
    });
  }

function initializeScreenChart(data, labels) {
    const ctx = document.getElementById('screen-time-chart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Screen Time (hrs)',
                data: data,
                backgroundColor: 'gray'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Screen Time'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}


function initializeSleepChart(data, labels) {
    const ctx = document.getElementById('sleep-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Sleep Hours',
                data: data,
                borderColor: '#6F42C1',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Sleep Hours Over Time'
                }
            }
        }
    });
  }
  
function initializeWaterChart(data, labels) {
    const ctx = document.getElementById('water-intake-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Water Intake (L)',
                data: data,
                borderColor: '#4B9CD3',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Water Intake Over Time'
                }
            }
        }
    });
  }
  

document.addEventListener('DOMContentLoaded', function () {
    const chartData = window.chartData;
    const dates = window.dates;  

    initializeExerciseChart(chartData.exercise, dates);
    initializeWaterChart(chartData.water, dates);
    initializeSleepChart(chartData.sleep, dates);
    initializeScreenChart(chartData.screen, dates);
});
