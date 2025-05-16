# CITS5505_Group_Project
Agile Web Developement Group 17 Project - LifeTracker

## Project Overview
LifeTracker is a lightweight web application that supports users to record their daily habits and is designed for personal habit formation, aiming to help users to establish and maintain an active and healthy lifestyle through daily data recording and intelligent analysis. Users can easily record their daily activities (e.g., exercise, water intake, hours of sleep, reading time, etc.) and understand their behavioral patterns and trends through automatically generated statistical charts.

The application is user-centered and dedicated to providing an intuitive, fun, and motivating tracking experience. Through visual feedback and selective data sharing, LifeTracker encourages self-reflection, self-discipline, and social interaction for support and motivation.

## Design Intent：
- Lower the threshold of habit formation and foster self-awareness among users.
- Utilize data-driven charts and insights to help users discover patterns and blind spots in their lives.
- Provide social sharing options to inspire positive influence and encouragement among users.

## Group Members

| UWA ID   | Name           | Github user name     |
|:-------  |:---------------|----------------------|
| 23463837 | Junxu Liu      | peanut4556           |
| 24505099 | Aksa Benny     | Aksa-23              |
| 23986599 | Meitong Jin    | MeitongJin           |
| 24570882 | Prapti Koirala | praptikoirala        |

## Features

- Daily activity tracking
- Physical health metrics monitoring
- Growth and habits tracking
- Mood and productivity tracking
- Dark mode support
- Interactive dashboard for data visualization

## Prerequisites

Before running the application, make sure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Git
- Node

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/Aksa-23/CITS5505_Group_Project.git
cd CITS5505_Group_Project
```

2. Create a virtual environment (recommended):
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

5. Install client-side dependencies from the package.json file:
```bash
npm install
```

## Database Setup

1. Initialize the database (if running for the first time):
```bash
flask db init
flask db migrate
flask db upgrade
```

## Running the Application

1. Make sure your virtual environment is activated (you should see `(venv)` in your terminal)

2. Start the Flask application:
```bash
# Windows
python app.py

# macOS/Linux
python3 app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
CITS5505_Group_Project/
├── static/
│   ├── js/
│   │   ├── charts/
│   │   │   ├── dashboardchart.js
│   │   │   ├── exercise.js
│   │   │   ├── screen-time.js
│   │   │   ├── share-view.js
│   │   │   ├── sleep.js
│   │   │   └── water-intake.js
│   │   ├── auth.js
│   │   ├── Click&Hide.js
│   │   ├── home.js
│   │   ├── load-users.js
│   │   ├── modal.js
│   │   ├── progress.js
│   │   └── resetPassword.js
│   └── css/
│       ├── input.css
│       ├── output.css
│       └── progress.css
├── templates/
│   ├── base.html
│   ├── Daily_input.html
│   ├── Daily_output.html
│   ├── dashboard.html
│   ├── homepage.html
│   ├── login.html
│   ├── Pre-registration.html
│   ├── register.html
│   ├── resetPassword.html
│   └── share-view.html
├── app.py
├── extensions.py
├── input.py
├── models.py
├── output.py
├── test_app_selenium.py
├── test_app_unit.py
├── package.json
├── package-lock.json
├── requirements.txt
└── README.md
```

## Using the Application

1. Register a new account or login with existing credentials
2. Navigate to the Daily Input page from the navigation menu
3. Fill in your daily metrics:
   - Exercise information (Yes/No and duration)
   - Water intake (in liters)
   - Sleep hours
   - Reading time
   - Meal count
   - Screen time
   - Productivity level (1-10)
   - Mood (Happy/Neutral/Sad/Angry)
4. Submit your daily entry
5. View your progress in the Dashboard

## Troubleshooting

If you encounter any issues:

1. Make sure all dependencies are installed correctly:
```bash
pip install -r requirements.txt --upgrade
```

2. Check if the virtual environment is activated (you should see `(venv)` in your terminal)

3. Ensure the database is properly initialized

4. Clear your browser cache if you're experiencing frontend issues

## Browser Compatibility

The application has been tested and works well with:
- Google Chrome (Recommended, version 90+)
- Mozilla Firefox (version 88+)
- Microsoft Edge (version 90+)
- Safari (version 14+)

## Test

This project includes both unit tests (logic-level validation) and end-to-end Selenium tests (browser-level automation).

### Unit Testing: `test_app_unit.py`
These tests validate core application logic, including:
- User registration and login behavior
- Password reset workflows
- Protected route access
- Form submission handling
#### ▶️ To run unit tests:
```bash
python test_app_unit.py
```
These tests use an **in-memory SQLite database** and do not affect production data.

### Selenium Testing: `test_app_selenium.py`
These tests simulate real user actions in a headless browser, including:
- Registering a new account
- Logging in and logging out
- Verifying page contents after login (e.g., dashboard/home)
- Filling out forms (select cases)
#### ▶️ To run Selenium test (Headless):
The test script automatically starts the Flask app in a background thread.
Just run:
```bash
python test_app_selenium.py
```
All tests will execute in sequence using an **in-memory database**, and the browser will run in headless mode.

**NOTE**: Chrome and Chromedriver must be installed and available in your system PATH. See "Running Selenium" section below if needed.

#### ▶️ Running Selenium (Headless)
To run Selenium tests without opening a browser window, tests use Chrome in headless mode.
If you encounter issues like `NoSuchDriverException` or `chromedriver not found`, ensure you have:
- Installed Google Chrome
- Installed the correct version of [Chromedriver](https://sites.google.com/chromium.org/driver/)
- Placed chromedriver in your system path

**NOTE**: If you can't find your Chrome version in the official Chromedriver list, it likely means you're using a pre-release or testing version of Chrome. For testing versions of Chrome, you can find the matching Chromedriver in the [Chrome for Testing section](https://googlechromelabs.github.io/chrome-for-testing/).



## Support

For any issues or questions:
1. Open an issue in the [GitHub repository](https://github.com/Aksa-23/CITS5505_Group_Project.git)
2. Contact any team member listed above
3. Email the development team at [liuj7533@gmail.com]

## License

Copyright © 2025 CITS5505 Group 17. All rights reserved.
