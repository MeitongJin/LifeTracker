export function initializeExerciseChart(data, labels) {
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
      options: { responsive: true }
  });
}