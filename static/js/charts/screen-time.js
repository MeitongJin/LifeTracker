export function initializeScreenChart(data, labels) {
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


console.log(window.chartData.screen);

