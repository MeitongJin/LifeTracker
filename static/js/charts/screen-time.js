fetch('../../../data/user-data.json')
  .then(res => res.json())
  .then(data => {
    const sorted = data.screen_time_data.sort((a, b) => new Date(a.date) - new Date(b.date));
    new Chart(document.getElementById('screen-time-chart'), {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.date),
        datasets: [
          {
            label: 'Screen Time',
            data: sorted.map(d => d.screen_time),
            backgroundColor: 'gray'
          },
          {
            label: 'Active Hours',
            data: sorted.map(d => d.active_hours),
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
  });
