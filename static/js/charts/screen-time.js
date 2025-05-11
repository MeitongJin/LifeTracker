export function initializeScreenChart(data, labels) {
  const ctx = document.getElementById('screen-time-chart').getContext('2d');
  new Chart(ctx, {
      type: 'bar',
      data: {
          labels: labels,
          datasets: [
              {
                  label: 'Screen Time',
                  data: data.screen_time,
                  backgroundColor: 'gray'
              },
              {
                  label: 'Active Hours',
                  data: data.active_hours,
                  backgroundColor: 'black'
              }
          ]
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
              title: {
                  display: true,
                  text: 'Screen Time vs Active Hours'
              }
          }
      }
  });
}
