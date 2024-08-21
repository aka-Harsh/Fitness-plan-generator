
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()

# Configure the Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the updated questions and options
questions = [
    ("What is your primary fitness goal?", ["Weight loss", "Muscle gain", "Improve endurance", "Increase flexibility", "General fitness", "Rehabilitation from injury"]),
    ("How often do you currently exercise?", ["Not at all", "1-2 times per week", "3-4 times per week", "5-6 times per week", "Daily"]),
    ("What is your current fitness level?", ["Beginner (Little to no exercise experience)", "Intermediate (Regular exercise, moderate experience)", "Advanced (Frequent exercise, extensive experience)", "Athlete (Highly trained, professional level)"]),
    ("What type of exercise do you prefer?", ["Cardio (Running, cycling, swimming)", "Strength training (Weightlifting, bodyweight exercises)", "Flexibility (Yoga, Pilates)", "Mixed (A combination of cardio, strength, and flexibility)", "Functional training (Exercises that improve daily movement)"]),
    ("What is your available workout time per session?", ["15-30 minutes", "30-45 minutes", "45-60 minutes", "60-90 minutes", "90+ minutes"]),
    ("Do you have any dietary preferences or restrictions?", ["No specific preference", "Vegetarian", "Vegan", "Low-carb", "High-protein", "Keto", "Gluten-free", "Other (with a field to specify)"]),
    ("What is your primary motivation for starting a fitness plan?", ["Improve health", "Enhance physical appearance", "Reduce stress", "Improve athletic performance", "Recover from injury"]),
    ("How do you prefer to exercise?", ["At the gym", "At home", "Outdoors", "With a group", "Alone", "With a trainer"]),
    ("Do you have any injuries or physical limitations?", ["No", "Yes (with a field to specify the injury or limitation)"]),
    ("What type of diet do you follow?", ["Balanced", "High-protein", "Low-carb", "Keto", "Vegan", "Vegetarian", "Paleo", "Custom (with a field to specify)"]),
    ("How much time can you commit to working out per week?", ["1-2 hours", "3-4 hours", "5-6 hours", "7+ hours"]),
    ("What is your sleep pattern like?", ["Less than 5 hours per night", "5-6 hours per night", "7-8 hours per night", "9+ hours per night"]),
    ("Do you prefer morning or evening workouts?", ["Morning", "Evening", "No preference"]),
    ("How do you usually track your progress?", ["Weight scale", "Body measurements", "Fitness tracker or app", "Visual appearance", "Workout performance (strength, speed, endurance)"]),
    ("Are you looking for a short-term or long-term fitness plan?", ["Short-term (4-8 weeks)", "Medium-term (8-16 weeks)", "Long-term (16+ weeks)"])
]

# Function to get a response from the Gemini model
def get_gemini_response(selected_choices):
    model = genai.GenerativeModel('gemini-1.5-flash')
    input_prompt = f"You are a fitness coach based on {selected_choices}, create a personalized fitness plan using all the {selected_choices} to develop the plan."
    
    try:
        response = model.generate_content([input_prompt])
        response_text = response.text  # Ensure this is the correct attribute
        st.write("Raw API Response:", response_text)  # Print raw response for debugging
        return response_text
    except Exception as e:
        st.write("Error:", str(e))
        return "An error occurred while processing the request."

# Streamlit app layout
st.set_page_config(page_title="Fitness Coach ", layout="wide")
st.header("Your Personalized Fitness Plan")

# Create columns to display questions side by side
num_columns = 3  # Number of columns you want
col_width = 1.0 / num_columns  # Width of each column
cols = st.columns(num_columns, gap="small")

# Collect responses to the questions
selected_choices = []
for idx, (question, opts) in enumerate(questions):
    col = cols[idx % num_columns]  # Distribute questions across columns
    with col:
        choice = st.radio(question, opts, key=idx)
        selected_choices.append(choice)

# Submit button
if st.button("Submit for Analysis"):
    st.subheader("Assessment Result")
    response = get_gemini_response(selected_choices)
