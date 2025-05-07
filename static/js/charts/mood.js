// fetch('../../../data/user-data.json')
//   .then(res => res.json())
//   .then(data => {
//     const moodCounts = data.mood_productivity_data.reduce((acc, curr) => {
//       acc[curr.mood] = (acc[curr.mood] || 0) + 1;
//       return acc;
//     }, {});

//     new Chart(document.getElementById('mood-chart'), {
//       type: 'pie',
//       data: {
//         labels: Object.keys(moodCounts),
//         datasets: [{
//           label: 'Mood Distribution',
//           data: Object.values(moodCounts),
//           backgroundColor: ['red', 'yellow', 'green', 'blue', 'purple']
//         }]
//       }
//     });
//   });
