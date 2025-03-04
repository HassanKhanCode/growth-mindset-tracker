import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import random

# Function to get a random motivational quote
def get_motivational_quote():
    quotes = [
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston S. Churchill",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "It does not matter how slowly you go as long as you do not stop. - Confucius",
        "You are never too old to set another goal or to dream a new dream. - C.S. Lewis"
    ]
    return random.choice(quotes)

# Function to load data
def load_data():
    try:
        data = pd.read_csv('data.csv')
    except FileNotFoundError:
        data = pd.DataFrame(columns=['Date', 'Reflection', 'Challenges', 'Successes', 'Habits'])
    return data

# Function to save data
def save_data(data):
    data.to_csv('data.csv', index=False)

# Load data
data = load_data()

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0;
    }
    .title {
        font-size: 3em;
        color: #4CAF50;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .header {
        font-size: 2.5em;
        color: #2196F3;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .subheader {
        font-size: 2em;
        color: #FF5722;
        font-weight: bold;
        margin-top: 10px;
    }
    .text {
        font-size: 1.3em;
        color: #333333;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
    }
    .button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 1.2em;
        border: none;
        margin-top: 10px;
    }
    .stTextInput>div>div>input {
        border: 1px solid #4CAF50;
        border-radius: 5px;
        padding: 10px;
    }
    .stTextArea>div>div>textarea {
        border: 1px solid #4CAF50;
        border-radius: 5px;
        padding: 10px;
    }
    .stDateInput>div>div>input {
        border: 1px solid #4CAF50;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to render the Dashboard
def render_dashboard():
    st.markdown('<h2 class="header">Dashboard</h2>', unsafe_allow_html=True)
    
    # Display recent reflections
    st.markdown('<h3 class="subheader">Recent Reflections</h3>', unsafe_allow_html=True)
    recent_reflections = data.tail(3)
    for index, row in recent_reflections.iterrows():
        st.markdown(f'<p class="text"><b>Date:</b> {row["Date"]}<br><b>Reflection:</b> {row["Reflection"]}</p>', unsafe_allow_html=True)
    
    # Display progress chart
    st.markdown('<h3 class="subheader">Progress Chart</h3>', unsafe_allow_html=True)
    if not data.empty:
        data['Date'] = pd.to_datetime(data['Date'])
        plt.figure(figsize=(10, 5))
        plt.plot(data['Date'], data.index + 1, marker='o', color='#4CAF50')
        plt.title('Progress Over Time', fontsize=16, color='#2196F3')
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Entries', fontsize=14)
        plt.grid(True)
        st.pyplot(plt.gcf())
    else:
        st.write("No data available yet. Start adding your reflections and habits to see progress.")

# Set the title of the app with custom CSS
st.markdown('<h1 class="title">Growth Mindset Tracker</h1>', unsafe_allow_html=True)

# Create a sidebar for navigation with custom CSS
st.sidebar.markdown('<h2 class="header">Navigation</h2>', unsafe_allow_html=True)
options = ["Dashboard", "Daily Reflections", "Habit Tracker", "Progress Tracker"]
choice = st.sidebar.selectbox("Select an option", options)

# Home Page with custom CSS
if choice == "Dashboard":
    render_dashboard()

# Daily Reflections Page with custom CSS
elif choice == "Daily Reflections":
    st.markdown('<h2 class="header">Daily Reflections</h2>', unsafe_allow_html=True)
    st.markdown('<p class="text">Reflect on your learning experiences, challenges, and successes.</p>', unsafe_allow_html=True)

    # Input fields for reflection
    date = st.date_input("Date", datetime.date.today())
    reflection = st.text_area("What did you learn today?")
    challenges = st.text_area("What challenges did you face?")
    successes = st.text_area("What were your successes?")

    # Save the reflection
    if st.button("Save Reflection", key="save_reflection"):
        new_entry = pd.DataFrame({
            'Date': [date],
            'Reflection': [reflection],
            'Challenges': [challenges],
            'Successes': [successes],
            'Habits': [""]  # Placeholder for habits
        })
        data = pd.concat([data, new_entry], ignore_index=True)
        save_data(data)
        st.success("Reflection saved!")

# Habit Tracker Page with custom CSS
elif choice == "Habit Tracker":
    st.markdown('<h2 class="header">Habit Tracker</h2>', unsafe_allow_html=True)
    st.markdown('<p class="text">Track your daily habits related to growth mindset.</p>', unsafe_allow_html=True)

    # Define habits
    habits = ["Read a book", "Practice mindfulness", "Exercise", "Learn something new"]
    habit_status = []

    # Input fields for habits
    for habit in habits:
        status = st.checkbox(habit)
        habit_status.append(status)

    # Save habits
    if st.button("Save Habits", key="save_habits"):
        data.loc[data['Date'] == datetime.date.today().strftime('%Y-%m-%d'), 'Habits'] = ', '.join(
            [habit for habit, status in zip(habits, habit_status) if status])
        save_data(data)
        st.success("Habits saved!")

# Progress Tracker Page with custom CSS
elif choice == "Progress Tracker":
    st.markdown('<h2 class="header">Progress Tracker</h2>', unsafe_allow_html=True)
    st.markdown('<p class="text">Track your progress over time.</p>', unsafe_allow_html=True)

    # Visualize progress
    if not data.empty:
        # Convert Date column to datetime
        data['Date'] = pd.to_datetime(data['Date'])
        
        # Plot progress
        plt.figure(figsize=(10, 5))
        plt.plot(data['Date'], data.index + 1, marker='o', color='#4CAF50')
        plt.title('Progress Over Time', fontsize=16, color='#2196F3')
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Entries', fontsize=14)
        plt.grid(True)
        st.pyplot(plt.gcf())
    else:
        st.write("No data available yet. Start adding your reflections and habits to see progress.")

# Save data on exit
save_data(data)
