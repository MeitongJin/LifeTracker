fetch('../../../data/user-data.json')
  .then(res => res.json())
  .then(data => {
    new Chart(document.getElementById('sleep-chart'), {
      type: 'line',
      data: {
        labels: data.sleep_data.map(d => d.date),
        datasets: [{
          label: 'Sleep Duration (hrs)',
          data: data.sleep_data.map(d => d.hours),
          backgroundColor: 'gray',
          borderColor: 'grey',
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Sleep Hours'
          }
        }
      }
    });
  });
