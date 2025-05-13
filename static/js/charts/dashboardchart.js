import { initializeExerciseChart } from './exercise.js';
import { initializeWaterChart } from './water-intake.js';
import { initializeSleepChart } from './sleep.js';
import { initializeScreenChart } from './screen-time.js';

document.addEventListener('DOMContentLoaded', function () {
    const chartData = window.chartData;
    const dates = window.dates;  

    initializeExerciseChart(chartData.exercise, dates);
    initializeWaterChart(chartData.water, dates);
    initializeSleepChart(chartData.sleep, dates);
    initializeScreenChart(chartData.screen, dates);
});