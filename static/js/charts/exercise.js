fetch('/data/user-data.json')
  .then(res => res.json())
  .then(data => {
    new Chart(document.getElementById('exercise-chart'), {
      type: 'bar',
      data: {
        labels: data.exercise_data.map(d => d.date),
        datasets: [{
          label: 'Exercise Hours',
          data: data.exercise_data.map(d => d.hours),
          backgroundColor: 'grey',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Exercise Duration (hrs)'
          }
        }
      }
    });
  });
