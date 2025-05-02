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

// The following are new additions. The purpose is to realize the retention of the user's input record when refreshing the page
function saveToLocal() {
  const fields = [
    'exerciseInput',
    'waterInput',
    'sleepInput',
    'readingInput',
    'eatInput',
    'deviceInput',
    'productivityInput',
  ];

  fields.forEach(id => {
    const el = document.getElementById(id);
    if (el) localStorage.setItem(id, el.value);
  });

  // Save radio: exercise
  const exerciseRadios = document.getElementsByName("exercise");
  exerciseRadios.forEach(r => {
    if (r.checked) localStorage.setItem("exerciseRadio", r.value);
  });

  // Save mood radio
  const moodRadios = document.getElementsByName("mood");
  moodRadios.forEach(r => {
    if (r.checked) localStorage.setItem("moodRadio", r.value);
  });
}


function loadFromLocal() {
  const fields = [
    'exerciseInput',
    'waterInput',
    'sleepInput',
    'readingInput',
    'eatInput',
    'deviceInput',
    'productivityInput',
  ];

  fields.forEach(id => {
    const el = document.getElementById(id);
    const val = localStorage.getItem(id);
    if (el && val !== null) el.value = val;
  });

  // // Restore radio: exercise
  const exerciseValue = localStorage.getItem("exerciseRadio");
  if (exerciseValue) {
    const ex = document.querySelector(`input[name="exercise"][value="${exerciseValue}"]`);
    if (ex) {
      ex.checked = true;
      toggleExerciseInput(exerciseValue === "yes"); // show/hide exercise time input
    }
  }

  // // Restore mood radio
  const moodValue = localStorage.getItem("moodRadio");
  if (moodValue) {
    const m = document.querySelector(`input[name="mood"][value="${moodValue}"]`);
    if (m) m.checked = true;
  }
}


// New function. Clear page after submitting data
function clearForm() {
  const fields = [
    "exerciseInput",
    "waterInput",
    "sleepInput",
    "readingInput",
    "eatInput",
    "deviceInput",
    "productivityInput"
  ];

  fields.forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.value = "";
    localStorage.removeItem(id);
  });

  document.querySelectorAll("input[type=radio]").forEach((r) => (r.checked = false));
  localStorage.removeItem("exerciseRadio");
  localStorage.removeItem("moodRadio");

  toggleExerciseInput(false);
}

// Restore filled data when the page loads
window.addEventListener("load", loadFromLocal);

// Saves the current data each time it is entered
document.querySelectorAll("input, select").forEach(el => {
  el.addEventListener("input", saveToLocal);
});


// submitBtn.addEventListener('click', () => {
  // if (!validateInputs()) {
    // return;
  // }
  // For example, saving to localStorage or jumping to
  // alert("Congratulations! The data has been submitted!");
  // Clear form after user submits data
  // clearForm();
// });

submitBtn.addEventListener('click', () => {
  if (!validateInputs()) {
    return;
  }

  // Collect data from the form
  const data = {
    exercise: document.querySelector('input[name="exercise"]:checked')?.value || "no",
    exercise_hours: document.getElementById('exerciseInput')?.value || "0",
    water_intake: document.getElementById('waterInput')?.value,
    sleep_hours: document.getElementById('sleepInput')?.value,
    reading_hours: document.getElementById('readingInput')?.value,
    meals: document.getElementById('eatInput')?.value,
    screen_hours: document.getElementById('deviceInput')?.value,
    productivity: document.getElementById('productivityInput')?.value,
    mood: document.querySelector('input[name="mood"]:checked')?.value || ""
  };

  // Send dara to server
  fetch('/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  }).then(response => response.json())
    .then(result => {
      if (result.status === 'success') {
        alert("Congratulations! The data has been submitted!");
        clearForm(); 
        window.location.href = "/dashboard";  // Jump to Dashboard after successful submission
      } else {
        alert("Submission failed: " + result.message);
      }
    }).catch(error => {
      console.error('Error:', error);
      alert("Submission error.");
    });
});
