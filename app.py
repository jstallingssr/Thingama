import openai
import streamlit as st
import random
import json
from typing import NamedTuple
from functools import partial
from time import time

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(
    page_title="Class Creator Thing-a-ma-jig!",
    page_icon="🧊",
    layout="centered",
    
)
with open("style.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

class ChatResponse(NamedTuple):
    content: str


def send_app(app: str, difficulty: str) -> ChatResponse:
    with open('official_resources.json', 'r') as f:
        resources = json.load(f)

    # Select three resources randomly
    selected_resources = random.sample(resources.get(app, []), 3)
    
    prompt = (
        f"Create a {difficulty}-level lesson plan for {app}. The class should focus on a specific feature "
        f"of the software and be achievable within a 45-60 minute timeframe. "
        f"Please provide the following details in markdown format:\n"
        f"- A catchy title\n"
        f"- An outline detailing up to three levels of depth\n"
        f"- Three to five specific deliverables for the students to create during the class\n"
        f"- A list of required materials, including software, hardware, and other necessary items\n"
        f"- An 'Additional Resources' section containing up to three links to the official documentation: {', '.join(selected_resources)}\n\n"
        f"Please ensure that no class is repeated within a user's session and that no time estimates "
        f"are provided for each item. Thank you."
    )


    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.8,
    )

    return ChatResponse(response.choices[0].text.strip())

def retrieve_ai_answer(app: str, difficulty: str) -> str:
    return send_app(app, difficulty).content.strip()

get_code_info = partial(retrieve_ai_answer)

@st.cache_data(show_spinner=False)
def get_cached_code_info(app: str, difficulty: str, unique_id: float) -> str:
    return get_code_info(app=app, difficulty=difficulty)


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
}

def display_widgets() -> tuple:
    st.image("images/lblApp.png")
   # response = st.empty()
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
    ]
    selected_option = st.selectbox("Select:", options)
    app = selected_option
    app_logo_path = app_logos.get(app, "")

    st.image("images/lblDiff.png")
    difficulty = st.select_slider(
        "Select:", options=["Beginner", "Intermediate", "Expert"]
    )

    class_outline = None  # Initialize class_outline with None
    unique_id = None  # Initialize unique_id with None

    if st.button("Generate a Class!", key="generate_class_button"):
        unique_id = time()  # Generate a new unique identifier
        with st.spinner(text="Building your class - hang tight! This can take up to 30 seconds..."):

            class_outline = get_cached_code_info(
                app=app, difficulty=difficulty, unique_id=unique_id
            )
            if app_logo_path:
                st.image(app_logo_path)
            st.markdown(f"\n{class_outline}")
            st.button("Build a New Class", key="new_class_button")

        return app_logo_path, class_outline, app, difficulty

    return None, None, None, None

def main() -> None:
    st.image("images/app.png")
    st.markdown(
        "The **Class Creator Thing-a-ma-jig!** is an innovative educational tool that leverages artificial intelligence to create lesson plans for a wide array of software applications. Choose from a curated list of programs, including Blender, Unreal Engine, Unity, and more. Each class can be comfortably completed within a 45-60 minute time frame, and the difficulty level can be customized to match your student's skill level."
    )

    f"Whether you are teaching a one-off class or looking for fresh ideas for your existing students, create unique and comprehensive class outlines with just a few clicks using the **Class Creator Thing-a-ma-jig**!"

    app_logo_path, class_outline, app, difficulty, = display_widgets()

    if class_outline is not None:

        #if app_logo_path:
            #st.image(app_logo_path)

        new_class_clicked = False  # Variable to track whether "New Class" button was clicked

        #st.markdown(f"**App:** {app}")
        #st.markdown(f"**Difficulty:** {difficulty}")

        #new_class_clicked = st.button("New Class")

        if new_class_clicked:
            st.stop()

if __name__ == "__main__":
    main()