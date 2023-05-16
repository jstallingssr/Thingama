from typing import NamedTuple
from functools import partial
import openai
import streamlit as st
from time import time

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(
    page_title="Class Creator Thing-a-ma-jig!",
    page_icon="🧊",
    layout="centered",
)

with open("style.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

    st.image("img/logo.png")


class ChatResponse(NamedTuple):
    content: str


def send_app(app: str, difficulty: str) -> ChatResponse:
    prompt = (
        f"I would like a lesson plan for {app} at the {difficulty} level. "
        f"These are educational classes, where students will learn a skill using the selected app. "
        f"This should be a very specific feature in the software, not a general overview. "
        f"Each class should be able to be completed within 45-60 minutes."
        f"Please provide only one class outline with a catchy title shown at the top. "
        f"The outline should be formatted in markdown, outline format. "
        f"The outline should be very detailed, up to three levels deep. "
        f"Each class should include three to five specific items that the student will create and deliver "
        f"or deliver during class (a game feature, an art asset, a texture, etc.). "
        f"Do not repeat any suggested classes during a user's session."
        f"Each outline should also have an additional resource section at the bottom with relevant links"
        f"When providing additional resources, please only use OFFICIAL resources such as https://docs.blender.org/ "
        f"https://docs.unrealengine.com/ do not link to videos or fan sites"
        f"No mention should be made of time, how long to complete, etc."
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
    "Blender": "img/blender.png",
    "Unreal Engine": "img/unreal.png",
    "Microsoft Excel": "img/excel.png",
    "Roblox": "img/roblox.png",
    "Ableton Live": "img/ableton.png",
    "Godot": "img/godot.png",
    "BandLab": "img/bandlab.png",
    "Unity": "img/unity.png",
    "Construct 3": "img/construct.png",
    "Minecraft": "img/minecraft.png",
    "Krita": "img/krita.png",
}


def display_widgets() -> tuple:
    st.subheader("First, choose a software application from the list below:")

    response = st.empty()
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

    st.subheader("Next, select the level of difficulty for this class:")
    difficulty = st.select_slider(
        "Select:", options=["Beginner", "Intermediate", "Advanced", "Expert"]
    )

    class_outline = None  # Initialize class_outline with None
    unique_id = None  # Initialize unique_id with None

    if st.button("Generate a Class!"):
        unique_id = time()  # Generate a new unique identifier
        with st.spinner(text="Building your class, hang tight! This can take up to 30 seconds..."):
            class_outline = get_cached_code_info(
                app=app, difficulty=difficulty, unique_id=unique_id
            )
            st.markdown(f"**Class Outline:**\n{class_outline}")
            st.button("New Class")

        app_logo = app_logos.get(app, None)  # Get the app logo
        return class_outline, app, difficulty, app_logo

    return None, None, None, None  # Return None values
def main() -> None:
    st.markdown(
        "The **Class Creator Thing-a-ma-jig!** is an innovative educational tool that leverages artificial intelligence to create lesson plans for a wide array of software applications. Choose from a curated list of programs, including Blender, Unreal Engine, Unity, and more."
    )

    f"Each class can be comfortably completed within a 45-60 minute time frame, and the difficulty level can be customized to match your student's skill, ranging from Beginner to Expert."
    f"Whether you are teaching a one-off class or looking for fresh ideas for your existing students, create unique and comprehensive class outlines with just a few clicks using the Class Creator Thing-a-ma-jig!)"

    class_outline, app, difficulty, app_logo = display_widgets()

    if class_outline is not None:
        new_class_clicked = False  # Variable to track whether "New Class" button was clicked

        st.markdown(f"**App:** {app}")
        st.markdown(f"**Difficulty:** {difficulty}")

        if app_logo:  # If there's a logo for the app, display it
            st.image(app_logo)

        new_class_clicked = st.button("New Class")

        if new_class_clicked:
            st.stop()

if __name__ == "__main__":
    main()

