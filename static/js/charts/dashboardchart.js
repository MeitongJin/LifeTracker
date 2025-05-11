import { initializeExerciseChart } from './exercise.js';
import { initializeWaterChart } from './water-intake.js';
import { initializeSleepChart } from './sleep.js';
import { initializeScreenChart } from './screen-time.js';

document.addEventListener('DOMContentLoaded', function () {
    const data = window.chartData;
    const dates = data.dates;

    initializeExerciseChart(data.exercise, dates);
    initializeWaterChart(data.water, dates);
    initializeSleepChart(data.sleep, dates);
    initializeScreenChart(data.screen, dates);
});