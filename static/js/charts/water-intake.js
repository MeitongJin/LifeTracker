fetch('../../../data/user-data.json')
  .then(res => res.json())
  .then(data => {
    new Chart(document.getElementById('water-intake-chart'), {
      type: 'line',
      data: {
        labels: data.water_data.map(d => d.date),
        datasets: [{
          label: 'Water Intake (liters)',
          data: data.water_data.map(d => d.liters),
          backgroundColor: 'gray',
          borderColor: 'gray',
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Water Intake'
          }
        }
      }
    });
  });
