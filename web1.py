import os
import random
import streamlit as st
import re
import pickle
import numpy as np
from pathlib import Path
import hashlib
import time
import base64

# Password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load models
try:
    model = pickle.load(open("df1.pkl", 'rb'))
    svc = pickle.load(open("svc.pkl", 'rb'))
    model1 = pickle.load(open("df.pkl", 'rb'))
    svc1 = pickle.load(open("svc1.pkl", 'rb'))
    model2 = pickle.load(open("df2.pkl", 'rb'))
    GB = pickle.load(open("GB.pkl", 'rb'))
except FileNotFoundError as e:
    st.error(f"Model file not found: {e}")
    st.stop()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# User database
USER_DB = Path("user_db.pkl")
if not USER_DB.exists():
    with open(USER_DB, 'wb') as f:
        pickle.dump({}, f)

def load_users():
    with open(USER_DB, 'rb') as f:
        return pickle.load(f)

def save_users(users):
    with open(USER_DB, 'wb') as f:
        pickle.dump(users, f)

def sign_up(username, password, fname, lname, phnno):
    if username == "" or password == "":
        return False
    
    phone_regex = r"^\+?[1-9]\d{1,14}$"

    if phnno:
        if re.match(phone_regex, phnno):
            st.success("Valid phone number!")
        else:
            st.error("Invalid phone number! Please enter in the format: +1234567890.")


    users = load_users()
    if fname in users:
        return True
    if lname in users:
        return True
    if username in users:
        return False
    if phnno in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def authenticate(username, password):
    users = load_users()
    return users.get(username) == hash_password(password)

def preprocess_input(age, academic_pressure, cgpa, study_satisfaction, study_hours, gender, sleep_duration, dietary, suicide, family_illness):
    gender_encoded = 0 if gender == 'Male' else 1

    dietary_encoded = {
        'Healthy': 1,
        'Moderate': 2,
        'Unhealthy': 3,
        'Others': 4
    }.get(dietary, 4)

    suicide_encoded = 1 if suicide == 'Yes' else 0
    family_illness_encoded = 1 if family_illness == 'Yes' else 0

    return np.array([age, academic_pressure, cgpa, study_satisfaction,
                     study_hours, gender_encoded, sleep_duration,
                     dietary_encoded, suicide_encoded, family_illness_encoded]).reshape(1, -1)

def preprocess_input1(Gender,Country,Ocupation,self_employed,family_history,Days_Indoors,Growing_Stress,Changes_Habits,Mental_Health_History,Mood_Swings,Coping_Struggles,Work_Interest,Social_Weakness,mental_health_interview,care_options):
    """
    Function to preprocess the input into the format expected by the model.
    """
    gender = 0 if Gender == 'Male' else 1
    
    country = {
        "United States": 1,
        "Poland": 2,
        "Australia": 3,
        "Canada": 4,
        "United": 5,
        "Kingdom": 6,
        "South Africa": 7,
        "New Zealand": 8,
        "Netherlands": 9,
        "India": 10,
        "Belgium": 11,
        "Ireland": 12,
        "France": 13,
        "Portugal": 14, 
        "Brazil": 15,
        "Costa Rica": 16,
        "Russia": 17, 
        "Germany": 18,
        "Switzerland": 19,
        "Finland": 20,
        "Israel": 21,
        "Italy": 22,
        "Bosnia and Herzegovina": 23,
        "Singapore": 24,
        "Nigeria": 25,
        "Croatia": 26, 
        "Thailand": 27,
        "Denmark": 28,
        "Mexico": 29,
        "Greece": 30,
        "Moldova": 31, 
        "Colombia": 32,
        "Georgia": 33,
        "Czech Republic": 34,
        "Philippines": 35
    }.get(Country, 35)

    ocupation = {
        'Corporate': 1,
        'Student': 2,
        'Business': 3,
        'Housewife': 4,
        'Others': 5
    }.get(Ocupation, 5)

    Self_employed = {
        'No' : 0,
        'Yes': 1,
        'Nan': 2,
    }.get(self_employed, 2)

    Family_history = 0 if family_history == 'NO' else 1

    # gender = 0 if Gender == 'Male' else 1
    
    days_Indoors = {
        '1-14 days': 0,
        'Go out Every day': 1,
        'More than 2 months':2,
        '15-30 days':3,
        '31-60 days': 4
    }.get(Days_Indoors, 4)

    growing_Stress = {
        'No' : 0,
        'Yes': 1,
        'Maybe': 2,
    }.get(Growing_Stress, 2)

    changes_Habits = {
        'No' : 0,
        'Yes': 1,
        'Maybe': 2,
    }.get(Changes_Habits, 2)

    mental_Health_History = {
        'No' : 0,
        'Yes': 1,
        'Maybe': 2,
    }.get(Mental_Health_History, 2)

    mood_Swings = {
        'Medium' : 0,
        'Low': 1,
        'High': 2,
    }.get(Mood_Swings, 2)

    coping_Struggles = 0 if Coping_Struggles == 'NO' else 1

    mental_Health_History = {
        'No' : 0,
        'Yes': 1,
        'Maybe': 2,
    }.get(Mental_Health_History, 2)

    work_Interest = {
        'No' : 0,
        'Yes': 1,
        'Maybe': 2,
    }.get(Work_Interest, 2)

    social_Weakness = {
        'No' : 0,
        'Yes': 1,
        'Maybe': 2,
    }.get(Social_Weakness, 2)
    
    Mental_health_interview = {
        'No' : 0,
        'Yes': 1,
        'Maybe': 2,
    }.get(mental_health_interview, 2)
    
    Care_options = {
        'No' : 0,
        'Yes': 1,
        'Not sure': 2,
    }.get(care_options, 2)
    

    return np.array([gender, country, ocupation, Self_employed,
                     Family_history, days_Indoors, growing_Stress,
                     changes_Habits, mental_Health_History, mood_Swings,coping_Struggles,
                     work_Interest,social_Weakness,Mental_health_interview,Care_options,
                    ]).reshape(1, -1)


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "Landing"

# Toggle test visibility state
if "show_student_test" not in st.session_state:
    st.session_state.show_student_test = False
if "show_working_test" not in st.session_state:
    st.session_state.show_working_test = False
if "show_common_for_all_test" not in st.session_state:
    st.session_state.show_common_for_all_test = False


def main():
    if st.session_state.page == "Landing":
        landing_page()
    elif st.session_state.page == "Signup":
        sign_up_page()
    elif st.session_state.page == "Login":
        login_page()
    elif st.session_state.page == "Home":
        app_pages()
st.set_page_config(
        page_title="Mental Health Support",  # Title of the page
        page_icon="🧠",  # Icon for the page
        layout="centered",  # Center the content on the page
        initial_sidebar_state="collapsed"
    )
def landing_page():
   
    st.markdown("""
        <style>
        .title {
            font-size: 3em;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-top: 50px;
        }
        .subheader {
            font-size: 1.5em;
            font-weight: normal;
            text-align: center;
            color: #eee;
        }
        .section {
            margin-top: 30px;
        }
        
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<h1 class="title">Mental Health Matters</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Taking care of your mental health is just as important as physical health.</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="section">
        <p style="font-size: 1.2em; text-align: center; color: #aaa;">
            Mental health is an essential part of overall health and well-being. It affects how we think, feel, and act. When we care for our mental health, we are more resilient, make better decisions, and can manage stress more effectively.
        </p>
        </div>
    """, unsafe_allow_html=True)
    
    def load_quotes(filename="quotes.txt"):
        with open(filename, "r", encoding="utf-8") as file:
            quotes = file.readlines()
        return [quote.strip() for quote in quotes]

    # Add custom CSS for styling
    st.markdown(
        """
        <style>
        .quote-container {
            display: flex;
            justify-content: center;
            align-items: center;
            
        }

        .quote-box {
            position: relative;
            background-color: #c9b8d8; 
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            font-family: 'Georgia', serif;
            color: #000;
            font-size: 1.5em;
            text-align: center;
            line-height: 1.8;
            margin:0.5em;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

    # Load the quotes
    quotes = load_quotes()

    # Display a random quote
    random_quote = random.choice(quotes)
    quote_text, author = random_quote.split("-", 1) if "-" in random_quote else (random_quote, "Unknown")

    st.markdown('<div class="quote-container">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="quote-box">
            {quote_text.strip()}<br><br>
            <em>— {author.strip()}</em>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            st.session_state.page = "Login"

    with col2:
        if st.button("Sign Up"):
            st.session_state.page = "Signup"

def sign_up_page():
    st.title("Sign Up")
    fname = st.text_input("Choose a First Name")
    lname = st.text_input("Choose a Last Name")
    phnno = st.text_input("Enter your phone number (e.g., +1234567890):")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")

    if st.button("Sign Up"):
        if sign_up(username, password, fname, lname, phnno):
            st.success("Sign up successful! Redirecting to login...")
            st.session_state.page = "Login"
        else:
            st.error("Username already exists. Please choose another.")

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.page = "Home"
        else:
            st.error("Invalid username or password.")

def app_pages():
    st.title(f"Welcome, {st.session_state.username}")

    tabs = st.tabs(["Home", "About", "Contact Us", "Depression Test", "Meditation","Breathing Exercise","Logout"])
    
    with tabs[0]:
        st.header("Home")
        st.write("Welcome to the Depression Prediction Application.")

    with tabs[1]:
        st.header("About")
        st.write("This application helps predict depression levels based on user inputs.")

    with tabs[2]:
        st.header("Contact Us")
        st.write("For queries, email us at support@example.com.")

    with tabs[3]:

        st.header("Depression Test")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Student"):
                st.session_state.show_student_test = not st.session_state.show_student_test
                st.session_state.show_working_test = False
                st.session_state.show_common_for_all_test = False
                

        with col2:
            if st.button("Working/Business"):
                st.session_state.show_working_test = not st.session_state.show_working_test
                st.session_state.show_student_test = False
                st.session_state.show_common_for_all_test = False
                
        
        with col3:
            if st.button("Common_for_all"):
                    st.session_state.show_common_for_all_test = not st.session_state.show_common_for_all_test
                    st.session_state.show_student_test = False
                    st.session_state.show_working_test = False


        if st.session_state.show_student_test:
            std_depression_test()

        if st.session_state.show_working_test:
            Work_depression_test()
        
        if st.session_state.show_common_for_all_test:
            Common_for_all_depression_test()
    
    with tabs[4]:
        # def initialize_timer(minutes):
        #     st.session_state['remaining_time'] = minutes * 60
        #     st.session_state['is_running'] = True

        # def countdown_timer(timer_placeholder):
        #     while st.session_state['remaining_time'] > 0 and st.session_state['is_running']:
        #         mins_left, secs_left = divmod(st.session_state['remaining_time'], 60)
        #         timer_placeholder.markdown(f"<h1 style='font-size: 100px; text-align: center;'> 🧘🏻 {mins_left:02}:{secs_left:02} 🧘🏻</h1>", unsafe_allow_html=True)
        #         time.sleep(1)
        #         st.session_state['remaining_time'] -= 1
        #         if st.session_state['remaining_time'] <= 0:
        #             st.session_state['is_running'] = False
        #             timer_placeholder.markdown(f"<h1 style='font-size: 60px; text-align: center;'>You did a Great Job! 🥳", unsafe_allow_html=True)
        #             st.session_state['is_audio_playing'] = False  

        # def encode_audio_to_base64(audio_file_path):
        #     with open(audio_file_path, "rb") as audio_file:
        #         encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")
        #     return encoded_audio

        # st.markdown(
        #     """
        #     <div style="text-align: center; font-size: 40px; color:rgb(2, 135, 252); font-weight: bold">
        #     🧘🏻 Meditation Timer 🧘🏻
        #     </div>
        #     """, unsafe_allow_html=True)

        # minutes = st.number_input("Enter the number of minutes for your meditation session:", min_value=1, max_value=120, value=5)

        # if 'remaining_time' not in st.session_state:
        #     st.session_state['remaining_time'] = 0
        #     st.session_state['is_running'] = False
        #     st.session_state['is_audio_playing'] = False  # Track audio state

        # timer_placeholder = st.empty()
        # btn1, btn2 = st.columns(2)

        # with btn1:
        #     if st.button("Start Meditation Timer") and not st.session_state['is_running']:
        #         st.session_state['is_running'] = True
                
        #         # Play audio only when the timer starts and if audio isn't playing
        #         if not st.session_state['is_audio_playing']:
        #             audio_folder = "audio"
        #             selected = os.path.join(audio_folder, "audio_1.mp3")
        #             html_string = f"""
        #             <audio id="meditation_audio" autoplay loop>
        #                 <source src="data:audio/mp3;base64,{encode_audio_to_base64(selected)}" type="audio/mp3">
        #             </audio>
        #             """
        #             st.markdown(html_string, unsafe_allow_html=True)
        #             st.session_state['is_audio_playing'] = True
                
        #         initialize_timer(minutes)
        #         countdown_timer(timer_placeholder)
        #         st.balloons()

        # with btn2:
        #     if st.button("Reset Timer") and st.session_state['is_running']:
        #         st.session_state['is_running'] = False
        #         st.session_state['remaining_time'] = 0
        #         timer_placeholder.markdown(f"<h1 style='font-size: 70px; text-align: center;'>Timer Reset⏳", unsafe_allow_html=True)
                
        #         # Stop the audio when timer is reset
        #         if st.session_state['is_audio_playing']:
        #             st.session_state['is_audio_playing'] = False
        #             st.markdown("""
        #             <script>
        #                 var audio = document.getElementById("meditation_audio");
        #                 audio.pause();
        #                 audio.currentTime = 0;  // Reset audio
        #             </script>
        #             """, unsafe_allow_html=True)
        def initialize_timer(minutes):
            st.session_state['remaining_time'] = minutes * 60
            st.session_state['is_running'] = True

        def countdown_timer(timer_placeholder):
            while st.session_state['remaining_time'] > 0 and st.session_state['is_running']:
                mins_left, secs_left = divmod(st.session_state['remaining_time'], 60)
                timer_placeholder.markdown(f"<h1 style='font-size: 100px; text-align: center;'> 🧘🏻 {mins_left:02}:{secs_left:02} 🧘🏻</h1>", unsafe_allow_html=True)
                time.sleep(1)
                st.session_state['remaining_time'] -= 1
                if st.session_state['remaining_time'] <= 0:
                    st.session_state['is_running'] = False
                    timer_placeholder.markdown(f"<h1 style='font-size: 60px; text-align: center;'>You did a Great Job! 🥳", unsafe_allow_html=True)

        
        st.markdown(
                """
                <div style="text-align: center; font-size: 40px; color:rgb(2, 135, 252); font-weight: bold">
                   🧘🏻 Meditation Timer 🧘🏻
                </div>
                """, unsafe_allow_html=True)


        minutes = st.number_input("Enter the number of minutes for your meditation session:", min_value=1, max_value=120, value=5)

        if 'remaining_time' not in st.session_state:
            st.session_state['remaining_time'] = 0
            st.session_state['is_running'] = False

        timer_placeholder = st.empty()
        btn1, btn2 = st.columns(2)
        audio_files = [ "audio/audio_1.mp3",
                       "audio/audio_2.mp3",
                       "audio/audio_3.mp3",
                       "audio/audio_4.mp3",
                       "audio/audio_5.mp3"
                       ]
        with btn1:
            if st.button("Start Meditation Timer") and not st.session_state['is_running']:
                st.session_state['is_running'] = True
                # selected_audio = audio_files[random.randint(0, len(audio_files)-1)]
                # audio_folder = "audio"
                # selected = os.path.join(audio_folder, "audio_1.mp3")
                
                # st.audio(selected_audio, format="audio/mp3", start_time=0, autoplay=True, loop=True)  # Plays the audio
                # st.markdown(f"""
                #     <audio autoplay loop>
                #         <source src="{selected}" type="audio/mp3">
                #     </audio>
                # """, unsafe_allow_html=True)
                # audio_player = st.empty() 
                # html_string = f"""<audio autoplay loop src="{selected}" type="audio/mp3"></audio>"""

                # audio_player.markdown(html_string, unsafe_allow_html=True) 
                # st.html(f"""<audio autoplay loop src="{selected}" type="audio/mp3"></audio>""")
                initialize_timer(minutes)
                countdown_timer(timer_placeholder)
                st.balloons()

        with btn2:
            if st.button("Reset Timer") and st.session_state['is_running']:
                st.session_state['is_running'] = False
                st.session_state['remaining_time'] = 0
                timer_placeholder.markdown(f"<h1 style='font-size: 70px; text-align: center;'>Timer Reset⏳", unsafe_allow_html=True)
    
    with tabs[5]:
        def countdown(emoji_display):
            for i in range(3, 0, -1):
                emoji_display.markdown(f"""
                <div style="text-align: center; font-size: 80px; font-weight: bold;">
                {i}
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1)  

        def breathing_phase(phase, duration, emoji_display):
            phase_names = {
                "breathe_in": "Breathe In",
                "hold": "Hold",
                "exhale": "Exhale"
            }
            colors = {
                "breathe_in": "#4CAF50",  # Green for breathing in
                "hold": "#FF9800",         # Orange for holding
                "exhale": "#F44336"        # Red for exhaling
            }

            emoji_display.markdown(f"""
            <div style="text-align: center; font-size: 60px; font-weight: bold; color: {colors[phase]};">
            {phase_names[phase]}
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(duration)  

        def start_breathing_cycle():
            status_text = st.empty()
            emoji_display = st.empty()  

            for cycle in range(1, 6):  # 5 cycles
                status_text.markdown(f"""
                <div style="text-align: center; font-size: 30px; font-weight: bold;">
                Cycle {cycle}
                </div>
                """, unsafe_allow_html=True)
                countdown(emoji_display)
                breathing_phase("breathe_in", 5, emoji_display)
                breathing_phase("hold", 5, emoji_display)
                breathing_phase("exhale", 5, emoji_display)
            st.markdown("<h3 class='celebration' style='text-align: center'>🎉 Great Job! You completed the exercise! 🎉</h3>", unsafe_allow_html=True)
            st.balloons()

        # Streamlit page layout
        st.markdown(
            """
            <div style="text-align: center; font-size: 36px; color: #4CAF50; font-weight: bold;">
            🌿 Breathing Exercise for Stress Relief 🌿
            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            """
            <div style="text-align: center; font-size: 20px; color: #6C757D;">
                Follow along with this simple exercise to reduce stress and feel more relaxed.
            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            """
            <div style="display:flex; justify-content:center">
            <div style=" font-size: 18px; color: #007BFF;">
                1. Breathe in for 5 seconds.<br>
                2. Hold your breath for 5 seconds.<br>
                3. Exhale slowly for 5 seconds.<br>
                Repeat for 5 cycles. Let's begin... <br><br>
            </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Start Exercise", key="start_exercise", use_container_width=True):
            start_breathing_cycle()
     
                        
    with tabs[6]:
        st.header("Logout")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.page = "Landing"

def std_depression_test():
    st.title("Depression Test")

    age = st.number_input('Student Age', min_value=0, max_value=100, step=1)
    academic_pressure = st.selectbox('Academic Pressure',  [1.0,2.0,3.0,4.0,5.0])
    cgpa = st.number_input('CGPA', min_value=0.0, max_value=10.0, step=0.1)
    study_satisfaction = st.number_input('Study Satisfaction (0 - Very Dissatisfied, 10 - Very Satisfied)', min_value=0.0, max_value=10.0, step=0.1)
    study_hours = st.number_input('Studying in hours per day', min_value=0.0, max_value=10.0, step=0.1)
    gender = st.selectbox('Gender', ['Male', 'Female'])
    sleep_duration = st.selectbox('Sleep Duration per day', model.get('sleep Duration', [4, 5, 6, 7, 8, 9]))
    dietary = st.selectbox('Dietary Habits', ['Healthy', 'Moderate', 'Unhealthy', 'Others'])
    suicide = st.selectbox('Have you ever had suicidal thoughts? (Yes/No)', ['Yes', 'No'])
    family_illness = st.selectbox('Family History of Mental Illness? (Yes/No)', ['Yes', 'No'])

    if st.button("Predict"):
        try:
            input_data = preprocess_input(age, academic_pressure, cgpa, study_satisfaction, study_hours, gender, sleep_duration, dietary, suicide, family_illness)
            prediction = svc.predict(input_data)

            if prediction[0] == 1:
                st.error("The model predicts a high likelihood of depression. Please seek professional help.")
            else:
                st.success("The model predicts no significant signs of depression.")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")




def Work_depression_test():
    st.title("Working/Business Depression Test")

    # Input features
    Age = st.number_input('Employee Age', min_value=0, max_value=100, step=1)
    Work_Pressure = st.selectbox('Work Pressure', model1['Work Pressure'].unique())
    Job_satisfaction = st.number_input('Job Satisfaction (0 - Very Dissatisfied, 5 - Very Satisfied)', min_value=0.0, max_value=10.0, step=0.1)
    work_hours = st.number_input('Working in hours per day',min_value=0, max_value=100, step=1)
    Financial_stress = st.number_input('Financial Stress', min_value=0, max_value=100, step=1)
    gender = st.selectbox('Employee Gender', ['Male', 'Female'])
    sleep_duration = st.selectbox('Sleep Duration per day of Employee', [4, 6, 8, 9])
    dietary = st.selectbox('Dietary Habits of Employee', ['Healthy', 'Moderate', 'Unhealthy'])
    suicide = st.selectbox('Have you ever had suicidal thoughts or not? (Yes/No)', ['Yes', 'No'])
    family_illness = st.selectbox('Family History of Mental Illness? [Yes/No]', ['Yes', 'No'])

    if st.button("Predicts"):
        try:
            input_data = preprocess_input(Age, Work_Pressure, Job_satisfaction, work_hours, Financial_stress, gender, sleep_duration, dietary, suicide, family_illness)
            prediction = svc1.predict(input_data)

            if prediction[0] == 1:
                st.error("The model predicts a high likelihood of depression. Please seek professional help.")
            else:
                st.success("The model predicts no significant signs of depression.")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")


def Common_for_all_depression_test():
    st.title("Common For All Depression Test")

    Gender = st.selectbox('Gender',model2['Gender'].unique())
    Country = st.selectbox('select your country', model2['Country'].unique())
    Ocupation = st.selectbox('Occupation', model2['Occupation'].unique())
    self_employed = st.selectbox('self_employed', model2['self_employed'].unique())
    family_history = st.selectbox('family_history',model2['family_history'].unique())
    Days_Indoors = st.selectbox('Days_Indoors', model2['Days_Indoors'].unique())
    Growing_Stress = st.selectbox('Growing_Stress', model2['Growing_Stress'].unique())
    Changes_Habits = st.selectbox('Changes_Habits', model2['Changes_Habits'].unique())
    Mental_Health_History = st.selectbox('Mental_Health_History', model2['Mental_Health_History'].unique())
    Mood_Swings = st.selectbox('Mood_Swings', model2['Mood_Swings'].unique())
    Coping_Struggles = st.selectbox('Coping_Struggles', model2['Coping_Struggles'].unique())
    Work_Interest = st.selectbox('Work_Interest', model2['Work_Interest'].unique())
    Social_Weakness = st.selectbox('Social_Weakness', model2['Social_Weakness'].unique())
    mental_health_interview = st.selectbox('mental_health_interview', model2['mental_health_interview'].unique())
    care_options = st.selectbox('care_options', model2['care_options'].unique())


    if st.button("Predicts"):
            try:
                input_data = preprocess_input1(Gender,Country,Ocupation,self_employed,family_history,Days_Indoors,Growing_Stress,Changes_Habits,Mental_Health_History,Mood_Swings,Coping_Struggles,Work_Interest,Social_Weakness,mental_health_interview,care_options)
                prediction = GB.predict(input_data)

                if prediction[0] == 0:
                    st.error("The model predicts a high likelihood of depression. Please seek professional help.")
                else:
                    st.success("The model predicts no significant signs of depression.")
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")

if __name__ == "__main__":
    main()
