export function initializeWaterChart(data, labels) {
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
