function toggleExerciseInput(show) {
  const ele = document.getElementById('exercise-hours');
  ele.classList.toggle('hidden', !show);
}

const checkbox = document.getElementById('agreeCheck');
const submitBtn = document.getElementById('submitBtn');

checkbox.addEventListener('change', () => {
  submitBtn.disabled = !checkbox.checked;
});

function validateInputs() {
  const sleep = parseFloat(document.getElementById('sleepInput').value);
  const device = parseFloat(document.getElementById('deviceInput').value);
  const water = parseFloat(document.getElementById('waterInput').value);
  const reading = parseFloat(document.getElementById('readingInput').value);
  const eat = parseFloat(document.getElementById('eatInput').value);
  const exerciseRadio = document.querySelector('input[name="exercise"]:checked');
  const exerciseVal = exerciseRadio && exerciseRadio.value === 'yes' ?
    parseFloat(document.getElementById('exerciseInput').value) : null;

  if (sleep > 24 || sleep < 0) {
    alert("Sleep time must be between 0 and 24 hours.");
    return false;
  }
  if (device > 24 || device < 0) {
    alert("Screen time must be between 0 and 24 hours.");
    return false;
  }
  if (reading > 24 || reading < 0) {
    alert("Reading time must be between 0 and 24 hours.");
    return false;
  }
  if (water < 0 || eat < 0) {
    alert("Values cannot be negative.");
    return false;
  }
  if (exerciseVal !== null && (exerciseVal < 0 || exerciseVal > 24)) {
    alert("Exercise time must be between 0 and 24 hours.");
    return false;
  }
  return true;
}

submitBtn.addEventListener('click', () => {
  if (!validateInputs()) {
    return;
  }
  // For example, saving to localStorage or jumping to
  alert("Congratulations! The data has been submitted!");
});