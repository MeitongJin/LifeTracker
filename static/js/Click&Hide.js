function toggleExerciseInput(show) {
  const ele = document.getElementById('exercise-hours');
  ele.classList.toggle('hidden', !show);
}

const checkbox = document.getElementById('agreeCheck');
const submitBtn = document.getElementById('submitBtn');

checkbox.addEventListener('change', () => {
  submitBtn.disabled = !checkbox.checked;
});

submitBtn.addEventListener('click', () => {
  // For example, saving to localStorage or jumping to
  alert("Congratulations! The data has been submitted! ");
});