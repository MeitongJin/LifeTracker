from flask import Blueprint, render_template, session, redirect, url_for
from models import db, UserInput
from datetime import date, timedelta
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

output_bp = Blueprint('output', __name__)

# Get the user input data of the past week
def get_past_week_inputs(user_id):
    today = date.today()
    one_week_ago = today - timedelta(days=6)
    records = UserInput.query.filter(
        UserInput.user_id == user_id,
        UserInput.date >= one_week_ago
    ).all()
    return records

# Generate a bar chart (Base64 encoded)
def generate_bar_chart(data_dict, title, ylabel):
    fig, ax = plt.subplots()
    ax.bar(data_dict.keys(), data_dict.values(), color='skyblue')
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(data_dict.keys(), rotation=45)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{chart_data}"

# Generate a pie chart (screen time vs activity time)
def generate_pie_chart(screen, active):
    fig, ax = plt.subplots()
    ax.pie([screen, active], labels=['Screen', 'Active'], autopct='%1.1f%%', colors=['#ff9999','#99ff99'])
    ax.set_title("Screen vs Active Time")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{chart_data}"

@output_bp.route('/dashboard')  # Wait for dashboard.html (if not, change to Daily_output.html)
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    records = get_past_week_inputs(user_id)

    if not records:
        return render_template("Daily_output.html", message="No data found.")

    df = pd.DataFrame([{
        "date": r.date.strftime('%Y-%m-%d'),
        "exercise": 1 if r.exercise == "yes" else 0,
        "exercise_hours": r.exercise_hours or 0,
        "water": r.water_intake or 0,
        "sleep": r.sleep_hours or 0,
        "reading": r.reading_hours or 0,
        "screen": r.screen_hours or 0,
        "productivity": r.productivity or 0,
        "mood": r.mood or ""
    } for r in records])

    df.set_index("date", inplace=True)

    # Chart generation
    exercise_chart = generate_bar_chart(df["exercise_hours"].to_dict(), "Exercise Hours", "Hours")
    water_chart = generate_bar_chart(df["water"].to_dict(), "Water Intake", "Litres")
    sleep_chart = generate_bar_chart(df["sleep"].to_dict(), "Sleep Hours", "Hours")
    screen_vs_active = generate_pie_chart(df["screen"].sum(), max(0.1, df["exercise_hours"].sum() + df["reading"].sum()))

    # Summary
    streak = int(df["exercise"].sum())
    water_avg = df["water"].mean()
    sleep_avg = df["sleep"].mean()
    reading_total = int(df["reading"].sum() * 60)  # Hours to minutes
    sleep_warning = sleep_avg < 7
    summary = (
        f"You exercised {df['exercise'].sum()} times, "
        f"slept an average of {sleep_avg:.1f} hrs "
        f"and had a peak mood. Great Job!!!"
    )

    return render_template("Daily_output.html",
                           exercise_chart=exercise_chart,
                           water_chart=water_chart,
                           sleep_chart=sleep_chart,
                           screen_chart=screen_vs_active,
                           streak=streak,
                           water_avg=f"{water_avg:.1f}",
                           sleep_avg=f"{sleep_avg:.1f}",
                           reading_total=reading_total,
                           sleep_warning=sleep_warning,
                           summary=summary)

