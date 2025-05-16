// This feature is implemented so that only one question appears on the page at a time.
// After answering one question then jump to another.

// Here the currentQuestion index starts at 0, question 1 indexes 0, 
// question 2 indexes 1, and so on.
let currentQuestion = 0;
// Get all question elements
const questions = document.querySelectorAll('.question');

function showQuestion(index) {
  questions.forEach((q, idx) => {
    q.classList.toggle('hidden', idx !== index);
  });
}

showQuestion(currentQuestion);

// Controls the Previous button.
document.querySelectorAll('.prev-btn').forEach((btn, index) => {
  btn.addEventListener('click', () => {
    if (currentQuestion > 0) {
      currentQuestion--;
      showQuestion(currentQuestion);
    }
  });
});

// Controls the Next button.
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

// Handling of special cases
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


// Switch between dark and light mode
document.getElementById('darkModeToggle').addEventListener('click', function () {
  document.body.classList.toggle('dark-mode');
  this.innerHTML = document.body.classList.contains('dark-mode') ? "Light Mode" : "Dark Mode";
});

const checkbox = document.getElementById('agreeCheck');
const submitBtn = document.getElementById('submitBtn');

// Make sure the element exists
if (checkbox && submitBtn) {
  // Initial state set to disabled
  submitBtn.disabled = true;

  checkbox.addEventListener('change', () => {
    submitBtn.disabled = !checkbox.checked;
  });
}

// Form Submission Processing
document.querySelector('form').addEventListener('submit', function (e) {
  e.preventDefault();
  if (!validateInputs()) {
    return;
  }

  // Submit form
  const formData = new FormData(this);
  fetch(this.action, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
    }
  })
    .then(response => {
      if (response.ok) {
        // Empty Local Storage and Forms
        localStorage.clear();
        clearForm();
        // Reset to first question
        currentQuestion = 0;
        showQuestion(currentQuestion);
        // Hide submission area, show form area
        document.querySelector('.submit').classList.add('hidden');
        document.querySelector('.form-section').classList.remove('hidden');
        // Uncheck the consent box and disable the submit button
        document.getElementById('agreeCheck').checked = false;
        document.getElementById('submitBtn').disabled = true;
        // Show success message
        alert('Data submitted successfully！');
      } else {
        alert('Submission failed, please try again.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('There was an error submitting, please try again.');
    });
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


// New feature. Clear page after submitting data
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

  // Clear all text input fields
  fields.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });

  // Clear exercise selection
  const exerciseRadios = document.getElementsByName('exercise');
  exerciseRadios.forEach(radio => {
    radio.checked = false;
  });

  // Clear Mood Selection
  const moodRadios = document.getElementsByName('mood');
  moodRadios.forEach(radio => {
    radio.checked = false;
  });
}

// Restore filled data when the page loads
window.addEventListener("load", loadFromLocal);

// Saves the current data each time it is entered
document.querySelectorAll("input, select").forEach(el => {
  el.addEventListener("input", saveToLocal);
});

// Add event listeners for exercise radio buttons
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('input[name="exercise"]').forEach(radio => {
    radio.addEventListener('change', function () {
      if (this.value === 'yes') {
        toggleExerciseInput(true);
      } else {
        toggleExerciseInput(false);
      }
    });
  });
});