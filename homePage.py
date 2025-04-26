# Calmora: Mental Health Dashboard
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from mongo_auth import MongoAuth
import bcrypt

# Configuration
MONGO_URI = "mongodb+srv://itsbhumika04:itsbhumika04@calmora.clfzr00.mongodb.net/"
DB_NAME = "calmora"

# Custom CSS for styling
def local_css():
    st.markdown(f"""
    <style>
        /* Main content styling */
        .stApp {{
            background-color: #f5f7fa;
        }}
        /* Header styling */
        h1, h2, h3 {{
            color: #4a4a4a;
            font-family: 'Arial', sans-serif;
        }}
        /* Button styling */
        .stButton>button {{
            background-color: #6c63ff;
            color: black;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: #5a52d3;
            transform: translateY(-2px);
        }}
        /* Slider styling */
        .stSlider {{
            color: #6c63ff;
        }}
        /* Radio button styling */
        .stRadio > div {{
            flex-direction: row;
            gap: 1rem;
        }}
        .stRadio label {{
            font-size: 1.1rem;
        }}
        /* Text input styling */
        .stTextInput input, .stTextArea textarea {{
            border-radius: 8px;
            padding: 0.5rem;
        }}
        /* Success message */
        .stAlert {{
            border-radius: 8px;
        }}
        /* Increase base font size */
        html {{
            font-size: 18px;
        }}
        /* Custom card styling */
        .custom-card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }}
    </style>
    """, unsafe_allow_html=True)

# Initialize MongoDB connection
@st.cache_resource
def get_auth():
    auth = MongoAuth(MONGO_URI, DB_NAME)
    # Initialize with admin user if DB is empty
    auth.initialize_db(
        admin_username="admin",
        admin_password="admin123",  # Change this in production!
        admin_email="admin@example.com",
        admin_name="Admin User"
    )
    return auth

auth = get_auth()

# Authentication Functions
# Update the login_form function
def login_form():
    """Render login form and handle authentication"""
    with st.form("Login"):
        st.markdown("""
        <div class="custom-card">
            <h3 style='color: #6c63ff;'>Login to Your Account</h3>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username").lower()
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", type="primary")
        
        if submit:
            user = auth.get_user(username)
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                # Update last login time
                auth.update_user(username, {'last_login': datetime.utcnow()})
                
                # Set session state
                st.session_state['user'] = {
                    'username': username,
                    'name': user['name'],
                    'email': user['email'],
                    'authenticated': True
                }
                st.rerun()
            else:
                st.error("Invalid username or password")

# Update the register_form function
def register_form():
    """Render registration form"""
    with st.form("Register"):
        st.markdown("""
        <div class="custom-card">
            <h3 style='color: #6c63ff;'>Create New Account</h3>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username").lower()
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Register", type="primary")
        
        if submit:
            if password != confirm_password:
                st.error("Passwords don't match!")
            elif auth.get_user(username):
                st.error("Username already exists")
            else:
                try:
                    auth.create_user(username, email, name, password)
                    st.success("Account created successfully! Please login.")
                    st.session_state['show_login'] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error creating account: {str(e)}")

# Update the local_css function to include form text colors
def local_css():
    st.markdown(f"""
    <style>
        /* Form text colors */
        .stTextInput>label, .stTextInput>div>div>input, 
        .stTextArea>label, .stTextArea>div>div>textarea,
        .stRadio>label, .stSelectbox>label, .stMultiselect>label {{
            color: #4a4a4a !important;
            font-size: 1.1rem;
        }}
        /* Form container styling */
        .stForm {{
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 2rem;
            background: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
        /* Make form inputs match our theme */
        .stTextInput input, .stTextInput input:focus, 
        .stTextArea textarea, .stTextArea textarea:focus {{
            border: 1px solid #d1d1d1;
            border-radius: 8px;
            padding: 0.75rem;
        }}
        /* Error message styling */
        .stAlert {{
            border-radius: 8px;
        }}
        .stException {{
            border-left: 4px solid #ff4b4b;
        }}
    </style>
    """, unsafe_allow_html=True)

    
def register_form():
    """Render registration form"""
    with st.form("Register"):
        st.markdown("#### Create New Account")
        username = st.text_input("Username").lower()
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Register")
        
        if submit:
            if password != confirm_password:
                st.error("Passwords don't match!")
            elif auth.get_user(username):
                st.error("Username already exists")
            else:
                try:
                    auth.create_user(username, email, name, password)
                    st.success("Account created successfully! Please login.")
                    st.session_state['show_login'] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error creating account: {str(e)}")

def logout():
    """Clear session state on logout"""
    st.session_state.clear()
    st.rerun()

# Password Reset Functionality
def password_reset_form():
    """Render password reset form"""
    with st.form("Reset Password"):
        st.write("Change your password")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Update Password")
        
        if submit:
            username = st.session_state['user']['username']
            user = auth.get_user(username)
            
            if new_password != confirm_password:
                st.error("New passwords don't match!")
            elif not bcrypt.checkpw(current_password.encode('utf-8'), user['password'].encode('utf-8')):
                st.error("Current password is incorrect")
            else:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                auth.update_user(username, {'password': hashed_password})
                st.success("Password updated successfully!")

# Profile Update Functionality
def profile_update_form():
    """Render profile update form"""
    with st.form("Update Profile"):
        st.write("Update your profile")
        user = auth.get_user(st.session_state['user']['username'])
        new_name = st.text_input("Name", value=user.get('name', ''))
        new_email = st.text_input("Email", value=user.get('email', ''))
        submit = st.form_submit_button("Update Profile")
        
        if submit:
            updates = {}
            if new_name != user.get('name'):
                updates['name'] = new_name
            if new_email != user.get('email'):
                updates['email'] = new_email
            
            if updates:
                auth.update_user(st.session_state['user']['username'], updates)
                st.session_state['user']['name'] = new_name
                st.session_state['user']['email'] = new_email
                st.success("Profile updated successfully!")
                st.rerun()

# Daily Mood Check-In Function
def daily_mood_checkin():
    """Daily mood check-in form"""
    st.markdown("""
    <div class="custom-card">
        <h2 style='color: #6c63ff;'>🧠 Daily Mood Check-In</h2>
        <p style='font-size: 1.1rem;'>Take a minute to reflect on your day. Your answers help us understand how you're feeling.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mood Questions (mix of sliders and yes/no)
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            q1 = st.slider("😴 How well did you sleep last night?", 1, 5, 3, 
                          help="1 = Poor sleep, 5 = Excellent sleep")
            q2 = st.radio("🌤 Are you feeling hopeful today?", ["Yes", "No"], 
                         horizontal=True, index=0)
            q3 = st.radio("🍽 Did you eat properly today?", ["Yes", "No"], 
                         horizontal=True, index=0)
            q4 = st.slider("😟 How anxious are you feeling?", 1, 5, 3, 
                          help="1 = Not anxious, 5 = Extremely anxious")
            q5 = st.radio("😄 Did you enjoy something today?", ["Yes", "No"], 
                         horizontal=True, index=0)
            
        with col2:
            q6 = st.slider("😔 Are you feeling lonely?", 1, 5, 3, 
                          help="1 = Not lonely, 5 = Very lonely")
            q7 = st.radio("🗣 Did you talk to a friend today?", ["Yes", "No"], 
                         horizontal=True, index=0)
            q8 = st.slider("💪 Do you feel motivated right now?", 1, 5, 3, 
                          help="1 = Not motivated, 5 = Very motivated")
            q9 = st.radio("🛡 Do you feel safe and secure?", ["Yes", "No"], 
                         horizontal=True, index=0)
            q10 = st.radio("💬 Do you want to talk to someone?", ["Yes", "No"], 
                          horizontal=True, index=0)

    # Submit Button with animation
    if st.button("Submit Mood Check-In", key="mood_submit"):
        mood_log = {
            "timestamp": datetime.now().isoformat(),
            "username": st.session_state['user']['username'],
            "responses": {
                "sleep_quality": q1,
                "hopeful": q2,
                "ate_properly": q3,
                "anxiety_level": q4,
                "enjoyed_something": q5,
                "loneliness_level": q6,
                "talked_to_friend": q7,
                "motivation_level": q8,
                "feeling_safe": q9,
                "wants_to_talk": q10
            }
        }

        # Here you would save to MongoDB
        # auth.db.mood_logs.insert_one(mood_log)
        
        st.balloons()
        st.success("✅ Your mood has been logged successfully!")
        
        with st.expander("📋 View Today's Check-In Summary"):
            st.json(mood_log)

# --- Mental Health Dashboard Functions ---
def mental_health_dashboard():
    st.title("Mental Health Dashboard 🧠")
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Mood Tracking", "💬 AI Chat Support", "🩺 Symptom Analysis", "📈 Progress Reports"])

    # --- Tab 1: Mood Tracking ---
    with tab1:
        daily_mood_checkin()
        
        st.markdown("---")
        st.header("Your Mood History")
        
        # Display Mood History (Mock Data - replace with actual data from MongoDB)
        mood_data = pd.DataFrame({
            "Date": pd.date_range(start="2024-01-01", periods=30),
            "Mood": np.random.randint(1, 11, 30),
            "Sleep Quality": np.random.randint(1, 6, 30),
            "Anxiety Level": np.random.randint(1, 6, 30)
        })
        
        # Interactive chart
        chart_type = st.radio("Select Chart Type", ["Line Chart", "Bar Chart"], horizontal=True)
        
        if chart_type == "Line Chart":
            st.line_chart(mood_data.set_index("Date"), height=400)
        else:
            st.bar_chart(mood_data.set_index("Date"), height=400)
        
        # Data table
        with st.expander("View Raw Data"):
            st.dataframe(mood_data.style.background_gradient(cmap="Blues"))

    # --- Tab 2: AI Chat Support ---
    with tab2:
        st.header("AI Chat Support 🤖")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Accept user input
        if prompt := st.chat_input("How are you feeling today?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                response = f"I hear you're feeling this way. Remember to practice self-care. Would you like to talk more about it?"
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Crisis Alert
        st.markdown("---")
        if st.button("🚨 Emergency Help", key="emergency"):
            st.error("Connecting you to a therapist...")
            st.info("""
            **Immediate Help Resources:**
            - National Suicide Prevention Lifeline: 1-800-273-8255
            - Crisis Text Line: Text HOME to 741741
            - International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/
            """)

    # --- Tab 3: Symptom Analysis ---
    with tab3:
        st.header("Self-Report Symptom Analysis")
        
        with st.form("symptom_form"):
            symptoms = st.multiselect(
                "Select symptoms you're experiencing:",
                ["Anxiety", "Insomnia", "Fatigue", "Loss of Appetite", 
                 "Headaches", "Irritability", "Difficulty Concentrating"],
                help="Select all that apply"
            )
            
            severity = st.slider("Overall Symptom Severity (1-10)", 1, 10, 5,
                               help="1 = Mild, 10 = Severe")
            
            notes = st.text_area("Additional Notes (Optional)",
                               placeholder="Describe your symptoms in more detail...")
            
            submitted = st.form_submit_button("Analyze Symptoms")
            
            if submitted:
                if not symptoms:
                    st.warning("Please select at least one symptom")
                else:
                    # Simple risk assessment
                    if severity >= 8:
                        risk_level = "High Risk"
                        recommendation = "We recommend speaking with a mental health professional soon."
                    elif severity >= 5:
                        risk_level = "Moderate Risk"
                        recommendation = "Consider self-care strategies and monitor your symptoms."
                    else:
                        risk_level = "Low Risk"
                        recommendation = "Your symptoms appear manageable. Continue self-care practices."
                    
                    st.markdown(f"""
                    <div class="custom-card">
                        <h3>Assessment Results</h3>
                        <p><strong>Risk Level:</strong> <span style='color: {"red" if severity >=8 else "orange" if severity >=5 else "green"}'>{risk_level}</span></p>
                        <p><strong>Recommendation:</strong> {recommendation}</p>
                        <p><strong>Suggested Coping Strategies:</strong> Mindfulness, Journaling, Physical Activity</p>
                    </div>
                    """, unsafe_allow_html=True)

    # --- Tab 4: Progress Reports ---
    with tab4:
        st.header("Your Progress Over Time")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
        with col2:
            end_date = st.date_input("End Date", value=pd.to_datetime("2024-01-31"))
        
        # Filter data
        filtered_data = mood_data[
            (mood_data["Date"] >= pd.to_datetime(start_date)) & 
            (mood_data["Date"] <= pd.to_datetime(end_date))
        ]
        
        # Metrics
        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Mood", f"{filtered_data['Mood'].mean():.1f}/10")
        col2.metric("Average Sleep Quality", f"{filtered_data['Sleep Quality'].mean():.1f}/5")
        col3.metric("Average Anxiety", f"{filtered_data['Anxiety Level'].mean():.1f}/5")
        
        # Progress chart
        st.subheader("Trend Analysis")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(filtered_data["Date"], filtered_data["Mood"], marker="o", label="Mood")
        ax.plot(filtered_data["Date"], filtered_data["Sleep Quality"]*2, marker="s", label="Sleep Quality (scaled)")
        ax.plot(filtered_data["Date"], filtered_data["Anxiety Level"]*2, marker="^", label="Anxiety Level (scaled)")
        ax.set_title("Progress Over Time")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
        
        # Export Data
        st.download_button(
            label="📥 Download Progress Report",
            data=filtered_data.to_csv(index=False),
            file_name="calmora_progress_report.csv",
            mime="text/csv"
        )

# Main App Logic
def main():
    # Apply custom CSS
    local_css()
    
    # Initialize session state variables if they don't exist
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'show_login' not in st.session_state:
        st.session_state['show_login'] = True

    # Check authentication status
    if st.session_state['user'] and st.session_state['user'].get('authenticated'):
        # Authenticated user view
        user = st.session_state['user']
        
        # Sidebar with user info and navigation
        with st.sidebar:
            st.markdown(f"""
            <div style='padding: 1rem; border-radius: 12px; background: #f0f2f6; margin-bottom: 2rem;'>
                <h3 style='color: #6c63ff;'>👋 Welcome, {user['name']}!</h3>
                <p>Last login: {datetime.now().strftime('%Y-%m-%d')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.button("Logout", on_click=logout, key="sidebar_logout")
            
            # Navigation
            st.markdown("### Navigation")
            page = st.radio("Go to", ["Dashboard", "Profile Settings"], label_visibility="collapsed")
            
            if page == "Profile Settings":
                with st.expander("Update Profile"):
                    profile_update_form()
                with st.expander("Change Password"):
                    password_reset_form()
        
        # Main content area
        if page == "Dashboard":
            st.title(f'Hello, {user["name"]} 👋')
            st.markdown("""
            <div class="custom-card">
                <p style='font-size: 1.1rem;'>Welcome back to your mental health dashboard. 
                Track your mood, get support, and monitor your progress.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Mental Health Dashboard
            mental_health_dashboard()
        
    else:
        # Unauthenticated user view
        st.title("Welcome to Calmora 🌿")
        st.markdown("""
        <div class="custom-card">
            <p style='font-size: 1.1rem;'>Your personal mental health companion. 
            Track your mood, get support, and improve your wellbeing.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state['show_login']:
            login_form()
            if st.button("Don't have an account? Register", key="to_register"):
                st.session_state['show_login'] = False
                st.rerun()
        else:
            register_form()
            if st.button("Already have an account? Login", key="to_login"):
                st.session_state['show_login'] = True
                st.rerun()

if __name__ == "__main__":
    main()