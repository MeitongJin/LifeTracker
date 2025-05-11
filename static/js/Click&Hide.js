// This feature is implemented so that only one question appears on the page at a time.
// After answering one question then jump to another.

// Here the currentQuestion index starts at 0, question 1 indexes 0, 
// question 2 indexes 1, and so on.
let currentQuestion = 0;
const questions = document.querySelectorAll('.question');

function showQuestion(index) {
  questions.forEach((q, idx) => {
    q.classList.toggle('hidden', idx !== index);
  });
}

showQuestion(currentQuestion);

document.querySelectorAll('.next-btn').forEach((btn, index) => {
  btn.addEventListener('click', () => {
    if (currentQuestion < questions.length - 1) {
      currentQuestion++;
      showQuestion(currentQuestion);
    } else {
      document.querySelector('.form-section').classList.add('hidden');
      document.querySelector('.submit').classList.remove('hidden');
    }
  });
});

function toggleExerciseInput(show) {
  const q2 = document.getElementById('q2');
  if (show) {
    currentQuestion = 1;
  } else {
    currentQuestion = 2;
  }
  showQuestion(currentQuestion);
}

document.querySelector('.submit').classList.add('hidden');

document.getElementById('darkModeToggle').addEventListener('click', function () {
  document.body.classList.toggle('dark-mode');
  this.innerHTML = document.body.classList.contains('dark-mode') ? "Light Mode" : "Dark Mode";
});

const checkbox = document.getElementById('agreeCheck');
const submitBtn = document.getElementById('submitBtn');

checkbox.addEventListener('change', () => {
  submitBtn.disabled = !checkbox.checked;
});

function validateInputs() {
  const sleep = parseFloat(document.getElementById('sleep_hours').value);
  const device = parseFloat(document.getElementById('screen_hours').value);
  const water = parseFloat(document.getElementById('water_intake').value);
  const reading = parseFloat(document.getElementById('reading_hours').value);
  const eat = parseFloat(document.getElementById('meals').value);
  const exerciseRadio = document.querySelector('input[name="exercise"]:checked');
  const exerciseVal = exerciseRadio && exerciseRadio.value === 'yes'
    ? parseFloat(document.getElementById('exercise_hours').value)
    : null;

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
    'exercise_hours',
    'water_intake',
    'sleep_hours',
    'reading_hours',
    'meals',
    'screen_hours',
    'productivity',
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
    'exercise_hours',
    'water_intake',
    'sleep_hours',
    'reading_hours',
    'meals',
    'screen_hours',
    'productivity',
  ];

  fields.forEach(id => {
    const el = document.getElementById(id);
    const val = localStorage.getItem(id);
    if (el && val !== null) el.value = val;
  });

  // Restore radio: exercise
  const exerciseValue = localStorage.getItem("exerciseRadio");
  if (exerciseValue) {
    const ex = document.querySelector(`input[name="exercise"][value="${exerciseValue}"]`);
    if (ex) {
      ex.checked = true;
      // Don't call toggleExerciseInput here to avoid jumping to q2 or q3
    }
  }

  // // Restore mood radio
  const moodValue = localStorage.getItem("moodRadio");
  if (moodValue) {
    const m = document.querySelector(`input[name="mood"][value="${moodValue}"]`);
    if (m) m.checked = true;
  }

  // Always start from q1 regardless of saved inputs
  showQuestion(currentQuestion);
}


// New function. Clear page after submitting data
function clearForm() {
  const fields = [
    'exercise_hours',
    'water_intake',
    'sleep_hours',
    'reading_hours',
    'meals',
    'screen_hours',
    'productivity'
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

submitBtn.addEventListener('click', () => {
  if (!validateInputs()) {
    return;
  }

  // Collect data from the form
  const data = {
    exercise: document.querySelector('input[name="exercise"]:checked')?.value || "no",
    exercise_hours: document.getElementById('exercise_hours')?.value || "0",
    water_intake: document.getElementById('water_intake')?.value,
    sleep_hours: document.getElementById('sleep_hours')?.value,
    reading_hours: document.getElementById('reading_hours')?.value,
    meals: document.getElementById('meals')?.value,
    screen_hours: document.getElementById('screen_hours')?.value,
    productivity: document.getElementById('productivity')?.value,
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
        window.location.href = "/daily_output";  // Jump to daily_output after successful submission
      } else {
        alert("Submission failed: " + result.message);
      }
    }).catch(error => {
      console.error('Error:', error);
      alert("Submission error.");
    });
});