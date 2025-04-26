import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="Mental Health Dashboard",
    page_icon="🧠",
    layout="wide"
)

# --- Sidebar (Login/Auth) ---
st.sidebar.title("User Authentication")
auth_option = st.sidebar.radio("Choose Mode:", ["Login", "Signup", "Guest Mode"])

if auth_option == "Login":
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        # Firebase/MongoDB Auth Logic Here
        st.sidebar.success("Logged In!")
elif auth_option == "Signup":
    new_email = st.sidebar.text_input("New Email")
    new_password = st.sidebar.text_input("New Password", type="password")
    if st.sidebar.button("Create Account"):
        # Firebase/MongoDB Signup Logic Here
        st.sidebar.success("Account Created!")
else:
    st.sidebar.warning("Guest Mode: Limited Access")

# --- Main Dashboard ---
st.title("Mental Health Dashboard 🧠")
tab1, tab2, tab3, tab4 = st.tabs(["Mood Tracking", "AI Chat Support", "Symptom Analysis", "Progress Reports"])

# --- Tab 1: Mood Tracking ---
with tab1:
    st.header("Log Your Daily Mood")
    mood = st.slider("How are you feeling today? (1=Low, 10=High)", 1, 10)
    notes = st.text_area("Additional Notes")
    if st.button("Save Mood Entry"):
        # Save to Excel/DB (Mock Example)
        new_entry = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Mood": mood,
            "Notes": notes
        }
        st.success("Mood logged successfully!")
        
    # Display Mood History (Mock Data)
    st.subheader("Mood History")
    mood_data = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=30),
        "Mood": np.random.randint(1, 11, 30)
    })
    st.line_chart(mood_data.set_index("Date"))

# --- Tab 2: AI Chat Support ---
with tab2:
    st.header("AI Chat Support 🤖")
    user_input = st.text_input("How are you feeling today?")
    if st.button("Get Support"):
        # GPT/BERT Integration Mock
        bot_response = "I hear you're feeling this way. Try practicing deep breathing for 5 minutes."
        st.text_area("AI Response:", value=bot_response, height=100)
    
    # Crisis Alert
    if st.button("🚨 Emergency Help"):
        st.error("Connecting you to a therapist...")
        st.info("National Suicide Prevention Lifeline: 1-800-273-8255")

# --- Tab 3: Symptom Analysis ---
with tab3:
    st.header("Self-Report Symptoms")
    symptoms = st.multiselect(
        "Select symptoms you're experiencing:",
        ["Anxiety", "Insomnia", "Fatigue", "Loss of Appetite", "Headaches"]
    )
    severity = st.slider("Symptom Severity (1-10)", 1, 10)
    if st.button("Analyze Symptoms"):
        # TensorFlow/BERT Risk Assessment Mock
        risk = "High Risk" if severity >= 8 else "Moderate/Low Risk"
        st.warning(f"Assessment: {risk}")
        st.write("Suggested Coping Strategies: Mindfulness, Journaling, Professional Help")

# --- Tab 4: Progress Reports ---
with tab4:
    st.header("Your Progress Over Time")
    # Mock Visualization (Matplotlib/Plotly)
    fig, ax = plt.subplots()
    ax.plot(mood_data["Date"], mood_data["Mood"], marker="o")
    ax.set_title("Mood Trend (Last 30 Days)")
    st.pyplot(fig)
    
    # Export Data
    if st.button("Download Progress Report"):
        # Generate Excel/PDF (Mock)
        st.write("Preparing report...")
        st.download_button(
            label="Download",
            data=mood_data.to_csv(),
            file_name="progress_report.csv"
        )

# --- Footer ---
st.markdown("---")
st.markdown("ℹ For emergencies, contact a mental health professional immediately.")