from models import db, UserInput
from datetime import date, timedelta
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd


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
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(data_dict.keys(), data_dict.values(), color='skyblue')
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks(range(len(data_dict)))
    ax.set_xticklabels(list(data_dict.keys()), rotation=45)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{chart_data}"

# Generate a pie chart (screen time vs activity time)
def generate_pie_chart(screen, active):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie([screen, active], labels=['Screen', 'Active'], autopct='%1.1f%%', colors=['#ff9999','#99ff99'])
    ax.set_title("Screen vs Active Time")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{chart_data}"



