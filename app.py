# app.py
import streamlit as st
from datetime import date
import pandas as pd

# Import Groq client only if you intend to use it.
# If you don't have groq installed or want to use OpenAI, replace call_model accordingly.
try:
    from groq import Groq
    _HAS_GROQ = True
except Exception:
    _HAS_GROQ = False

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Fitness Assistant", page_icon="💪", layout="wide")

# ---------- HELPERS ----------
def detect_intent(text: str) -> str:
    """Return one of: 'medical', 'nutrition', 'workout', 'motivation'."""
    text = (text or "").lower()
    medical_keywords = [
        'pain', 'injury', 'hurt', 'doctor', 'hospital', 'medical',
        'arthritis', 'chest', 'headache', 'sick', 'sore', 'ill',
    ]
    workout_keywords = ['workout', 'exercise', 'gym', 'lift', 'hiit', 'cardio', 'strength']
    nutrition_keywords = ['diet', 'food', 'meal', 'nutrition', 'snack', 'calorie', 'protein', 'kcal', 'carb']

    if any(word in text for word in medical_keywords):
        return 'medical'
    if any(word in text for word in nutrition_keywords):
        return 'nutrition'
    if any(word in text for word in workout_keywords):
        return 'workout'
    return 'motivation'

def generate_prompt(intent: str, user_input: str) -> str:
    """Format the prompt to send to the model based on intent."""
    base = (
        "You are a helpful, concise fitness assistant.\n"
        f"User intent: {intent}\n"
        f"User message: {user_input}\n\n"
    )
    if intent == 'workout':
        base += (
            "Return: a short structured exercise plan (exercises, sets, reps, rest). "
            "Keep it practical and safe for a general audience."
        )
    elif intent == 'nutrition':
        base += (
            "Return: a 1-day meal plan with approximate calorie estimates and a quick macro breakdown. "
            "Ask questions only if necessary."
        )
    elif intent == 'medical':
        base += (
            "Return: a short non-diagnostic safety-first response that encourages consulting a healthcare professional. "
            "Do NOT give medical diagnoses or prescriptions."
        )
    else:
        base += "Return: a short motivational message or quote with 1-2 actionable tips."
    return base

def call_model(api_key: str, prompt: str) -> str:
    """
    Call the Groq model (or return helpful errors). 
    Replace implementation here if you want to use a different provider.
    """
    if not api_key:
        return "⚠️ No API key provided. Please enter your Groq API key in the sidebar."

    if not _HAS_GROQ:
        return "⚠️ Groq client library not installed in this environment. Install `groq` or replace call_model with another client."

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        # Log minimal info and return friendly error
        return f"⚠️ Error calling model: {e}"

# ---------- SIDEBAR ----------
# --- SIDEBAR ---
st.sidebar.title("💪 Fitness AI")
st.sidebar.markdown("...") # Your markdown link

# Securely get the API key from secrets for deployment 🔑
api_key = st.secrets["GROQ_API_KEY"]

st.sidebar.markdown("---")
st.sidebar.header("Your Profile")
# ... (the rest of your sidebar code for Name, Age, Sex, etc.)
st.sidebar.markdown("---")
st.sidebar.header("Your Profile")
default_name = "Swastika"  # friendly default from your context
name = st.sidebar.text_input("Name", value=default_name, key="profile_name")
age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=20, key="profile_age")
sex = st.sidebar.selectbox("Sex", ["Female", "Male", "Other"], key="profile_sex")
goal = st.sidebar.selectbox("Goal", ["Weight Loss", "Muscle Gain", "Endurance", "General Fitness"], key="profile_goal")
st.sidebar.write(f"🏁 Goal: **{goal}**")
st.sidebar.caption(f"App last updated: {date.today().strftime('%d %b %Y')}")
st.sidebar.markdown("---")
st.sidebar.write("Tip: Don't hardcode your API key into the file. Use the sidebar or `secrets.toml`.")

# ---------- NAVIGATION ----------
page = st.sidebar.radio("Go to", ["Chat Assistant", "Dashboard"], index=0)

# ---------- SESSION STATE SETUP ----------
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of dicts: {"role": "user"/"assistant", "content": str}

# ---------- DASHBOARD PAGE ----------
if page == "Dashboard":
    st.title("📊 Fitness Dashboard")
    st.subheader("👤 Personal Info")
    col1, col2, col3 = st.columns(3)
    col1.metric("Name", name)
    col2.metric("Age", age)
    col3.metric("Sex", sex)

    st.subheader("🏋️ Weekly Workout Plan (example)")
    data = {
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "Workout": [
            "Chest & Triceps", "Back & Biceps", "Legs", "Core + Cardio", "Shoulders", "Yoga/Active Rest"
        ],
        "Duration (mins)": [60, 55, 65, 40, 50, 30],
    }
    df = pd.DataFrame(data)
    st.table(df)

    st.subheader("📈 Weekly Workout Duration (mins)")
    st.line_chart(df["Duration (mins)"])
    st.caption(f"Last updated: {date.today().strftime('%d %B %Y')}")

# ---------- CHAT PAGE ----------
elif page == "Chat Assistant":
    st.title("💬 Fitness Chat Assistant")

    # Display previous messages
    if st.session_state.messages:
        for msg in st.session_state.messages:
            role = msg.get("role", "assistant")
            content = msg.get("content", "")
            with st.chat_message(role):
                st.markdown(content)

    # Single chat input (unique key)
    user_input = st.chat_input("Ask me about workouts, meals, or motivation!", key="fitness_chat")

    if user_input:
        # Append and display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Detect intent
        intent = detect_intent(user_input)

        # Medical intent - show immediate safety response (no external call)
        if intent == 'medical':
            disclaimer = (
                "**Disclaimer:** I am an AI assistant, not a medical professional. "
                "For anything that sounds like an injury, persistent pain, or an emergency please consult a qualified healthcare professional."
            )
            with st.chat_message("assistant"):
                st.warning(disclaimer)
            st.session_state.messages.append({"role": "assistant", "content": disclaimer})
        else:
            # Build prompt and call model
            prompt = generate_prompt(intent, user_input)
            with st.chat_message("assistant"):
                # Show a temporary placeholder while generating (Streamlit will render immediately)
                st.markdown("🤖 Generating response...")
            # Call model (synchronously)
            model_reply = call_model(api_key, prompt)
            # Replace placeholder by appending next message (simple approach)
            with st.chat_message("assistant"):
                st.markdown(model_reply)
            st.session_state.messages.append({"role": "assistant", "content": model_reply})

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Built with ❤️ — edit the code to customize model, prompts, or UI.")
