export function initializeSleepChart(data, labels) {
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
