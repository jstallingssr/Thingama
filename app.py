# This app is an innovative educational tool that leverages 
# artificial intelligence to create lesson plans 
# for a wide array of software applications including Blender, 
# Unreal Engine, Unity, and more. Each class can be 
# comfortably completed within a 45-60 minute time 
# frame, and the difficulty level can be customized 
# to match a student's skill level.

import openai
import streamlit as st
import random
import json
from typing import NamedTuple
from functools import partial
from time import time

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set Streamlit page configuration
st.set_page_config(
    page_title="Class Creator Thing-a-ma-jig!",
    page_icon="🧊",
    layout="centered",
)

# Load custom CSS style
with open("style.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# NamedTuple for representing a chat response
class ChatResponse(NamedTuple):
    content: str

# Function to send an application and difficulty to OpenAI API and get a lesson plan as a response
def send_app(app: str, difficulty: str) -> ChatResponse:
    # Load the available resources from a JSON file
    with open("resources.json", "r") as f:
        resources = json.load(f)

    # Select three random resources for the given app
    selected_resources = random.sample(resources.get(app, []), 3)

    # Prepare the prompt for generating a lesson plan
    prompt = (
        f"Create a {difficulty}-level lesson plan for {app}. The class should focus on a specific feature "
        f"of the software and be achievable within a 45-60 minute timeframe. "
        f"Please provide the following details in markdown format:\n"
        f"- A catchy title\n"
        f"- An outline detailing at least three levels of depth\n"
        f"- Three to five specific deliverables for the students to create during the class\n"
        f"- A list of required materials, including software, hardware, and other necessary items\n"
        f"- An 'Additional Resources' section containing up to three links to the official documentation: {', '.join(selected_resources)}\n\n"
        f"Please ensure that no class is repeated within a user's session and that no time estimates "
        f"are provided for each item. Thank you."
    )

    # Send the prompt to OpenAI API for generating a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1800,
        n=1,
        stop=None,
        temperature=0.9,
    )

    # Return the generated class response as a ChatResponse object
    return ChatResponse(response.choices[0].text.strip())

# Function to retrieve the AI-generated lesson plan as a string
def retrieve_ai_answer(app: str, difficulty: str) -> str:
    return send_app(app, difficulty).content.strip()

# Partial function to retrieve the AI-generated lesson plan using the application and difficulty arguments
get_code_info = partial(retrieve_ai_answer)

# Cache the result of the AI-generated lesson plan for a given app, difficulty, and unique ID
@st.cache_data(show_spinner=False)
def get_cached_code_info(app: str, difficulty: str, unique_id: float) -> str:
    return get_code_info(app=app, difficulty=difficulty)

# Dictionary mapping application names to their respective logo image paths
app_logos = {
    "Blender": "images/blender.png",
    "Unreal Engine": "images/unreal.png",
    "Microsoft Excel": "images/excel.png",
    "Roblox": "images/roblox.png",
    "Ableton Live": "images/ableton.png",
    "Godot": "images/godot.png",
    "BandLab": "images/bandlab.png",
    "Unity": "images/unity.png",
    "Construct 3": "images/construct.png",
    "Minecraft": "images/minecraft.png",
    "Krita": "images/krita.png",
    "Twinmotion": "images/twinmotion.png",
}

# Function to display the Streamlit widgets and get user input
def display_widgets() -> tuple:
    # Display the image for the application selection
    st.image("images/lblApp.png")

    # List of available application options
    options = [
        "Blender",
        "Unreal Engine",
        "Microsoft Excel",
        "Roblox",
        "Ableton Live",
        "Godot",
        "BandLab",
        "Unity",
        "Construct 3",
        "Minecraft",
        "Krita",
        "Twinmotion",
    ]

    # Select an application from the dropdown menu
    selected_option = st.selectbox("Select:", options)
    app = selected_option
    app_logo_path = app_logos.get(app, "")

    # Display the image for the difficulty selection
    st.image("images/lblDiff.png")

    # Select a difficulty level using a slider
    difficulty = st.select_slider(
        "Select:", options=["Beginner", "Intermediate", "Expert"]
    )

    class_outline = None
    unique_id = None

    # Generate a class button
    if st.button("Generate a Class!", key="generate_class_button"):
        unique_id = time()
        with st.spinner(
            text="Building your class - hang tight! This can take up to 30 seconds..."
        ):
            # Get the AI-generated lesson plan from cache or generate a new one
            class_outline = get_cached_code_info(
                app=app, difficulty=difficulty, unique_id=unique_id
            )

            # Display the application logo if available
            if app_logo_path:
                st.image(app_logo_path)

            # Display the generated class outline
            st.markdown(f"\n{class_outline}")

            # Button to build a new class
            st.button("Build a New Class", key="new_class_button")

        return app_logo_path, class_outline, app, difficulty

    return None, None, None, None

# Main function to run the Streamlit application
def main() -> None:
    # Display the main image and introduction
    st.image("images/app.png")
    st.markdown(
        "The **Class Creator Thing-a-ma-jig!** is an innovative educational tool that leverages artificial intelligence to create lesson plans for a wide array of software applications. Choose from a curated list of programs, including Blender, Unreal Engine, Unity, and more. Each class can be comfortably completed within a 45-60 minute time frame, and the difficulty level can be customized to match your student's skill level."
    )

    # Function description missing here, consider adding it
    f"Whether you are teaching a one-off class or looking for fresh ideas for your existing students, create unique and comprehensive class outlines with just a few clicks using the **Class Creator Thing-a-ma-jig**!"

    # Display the widgets and get user input
    (
        class_outline,
    ) = display_widgets()

    # Check if a class outline is generated
    if class_outline is not None:
        # Function description missing here, consider adding it
        new_class_clicked = False

        if new_class_clicked:
            st.stop()

if __name__ == "__main__":
    main()
