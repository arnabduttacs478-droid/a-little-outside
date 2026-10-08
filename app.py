import os
import streamlit as st
from groq import Groq


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="A Little Outside",
    page_icon="🌿",
    layout="centered"
)


# ---------------------------------------------------------
# GROQ API
# ---------------------------------------------------------

groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    try:
        groq_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        groq_key = None

if not groq_key:
    st.error("GROQ_API_KEY is not configured.")
    st.stop()

client = Groq(api_key=groq_key)


# ---------------------------------------------------------
# AI SYSTEM PROMPT
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are the gentle guide inside an app called "A Little Outside".

Your purpose is to help someone leave the screen for a few minutes and
experience a meaningful moment in the real world.

You are NOT a therapist, doctor, fitness coach, productivity coach,
or generic motivational chatbot.

Your response should feel like a warm human invitation to step outside,
not like a list of instructions or a wellness checklist.

IMPORTANT:

- Understand the person's emotional situation.
- Respect the time they have.
- Create ONE specific outdoor experience.
- Make the experience feel personal to what they shared.
- If they shared a personal memory, gently connect the experience to
  the feeling or atmosphere of that memory.
- The activity can be simple: walking, sitting somewhere, looking at
  the sky, watching trees, feeling the breeze, listening to sounds,
  noticing sunlight, observing surroundings, etc.
- Give several small things they MAY notice or try while outside.
- Use gentle sensory suggestions: sight, sound, air, temperature,
  smells, textures.
- You may suggest closing their eyes briefly IF it is safe and
  appropriate. Never suggest closing eyes while walking or near traffic.
- Never require a particular location. Adapt to ordinary places such
  as a balcony, terrace, campus, garden, courtyard, street, or park.
- Never make the experience sound like exercise or fitness training.
- Never diagnose the person.
- Never provide medical advice.
- Never claim that nature or music treats a mental-health condition.

MUSIC:

Music is optional and secondary to the outdoor experience.

If appropriate, suggest a MUSIC MOOD or STYLE, such as:
"soft instrumental music", "gentle acoustic music", or "quiet piano".

Do not claim music is therapy.
Do not provide copyrighted lyrics.

MOST IMPORTANT:

The user should eventually stop looking at the screen.

Do not repeatedly tell them to stop using their phone.

Instead, explain naturally that the phone can stay away so they can
notice the moment without trying to photograph, record, post, or document it.

The final part should gently invite them to put the phone away and
experience the moment.

WRITING STYLE:

- Warm
- Personal
- Calm
- Emotionally meaningful
- Visual
- Natural
- Never clinical
- Never robotic
- Never like a fitness instruction
- Never like a numbered self-help checklist

Write as if you are gently accompanying the person outside.

Do NOT ask another question.

Structure the response naturally with:

1. A short emotional opening.
2. A small outdoor experience with several gentle things they can
   notice or try.
3. An optional music suggestion when appropriate.
4. A natural closing invitation to put the phone away.

Keep it around 150-220 words.
"""


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("A Little Outside 🌿")

st.write(
    "A little AI. A little music. A little nature. "
    "A reason to step outside."
)

st.caption(
    "The screen is only the beginning. "
    "The real experience happens outside."
)

st.divider()


# ---------------------------------------------------------
# WHAT ARE YOU FEELING?
# ---------------------------------------------------------

st.subheader("What is on your mind?")

input_mode = st.radio(
    "Choose how you'd like to begin:",
    [
        "🌿 Choose what I'm feeling",
        "💭 Tell me what's on my mind"
    ],
    horizontal=True
)


if input_mode == "🌿 Choose what I'm feeling":

    feeling = st.selectbox(
        "Choose what feels closest:",
        [
            "😮‍💨 I need to breathe",
            "🏠 I miss home",
            "🧠 My mind is crowded",
            "🌧️ It's been a difficult day",
            "☀️ I want a little happiness",
            "🌿 I just need to get outside"
        ]
    )

    user_thought = feeling

else:

    user_thought = st.text_area(
        "Tell me what's on your mind",
        placeholder=(
            "You don't have to explain it perfectly. "
            "Just tell me what you're feeling or what happened..."
        ),
        height=120
    )


# ---------------------------------------------------------
# PERSONAL MEMORY
# ---------------------------------------------------------

st.subheader("A small memory, if you'd like")

st.caption(
    "Sometimes a good memory can help us find the feeling "
    "we want to reconnect with."
)

memory = st.text_area(
    "Optional",
    placeholder=(
        "Maybe a place, person, sound, smell, season, "
        "or a small moment that still makes you smile..."
    ),
    height=100,
    label_visibility="collapsed"
)


# ---------------------------------------------------------
# AVAILABLE TIME
# ---------------------------------------------------------

st.subheader("How much time do you have?")

available_time = st.selectbox(
    "Choose a little time for yourself:",
    [
        "5 minutes",
        "10 minutes",
        "20 minutes",
        "30+ minutes"
    ]
)


# ---------------------------------------------------------
# GENERATE EXPERIENCE
# ---------------------------------------------------------

st.divider()

generate = st.button(
    "Give me a little outside 🌿",
    use_container_width=True
)


if generate:

    if not user_thought.strip():
        st.warning("Tell me a little about what's on your mind first.")
        st.stop()

    user_prompt = f"""
The person says:

{user_thought}

They have:

{available_time}

Optional personal memory:

{memory if memory.strip() else "No personal memory was shared."}

Create their "little outside".

Do not simply recommend an activity.

Instead, guide them through a small outdoor moment. Tell them where
they could go in a flexible way, what they might do when they arrive,
and what they could notice around them.

Give them freedom. Use phrases such as "you could", "if you'd like",
or "perhaps" rather than commanding every action.

Make the experience emotionally connected to what they shared.

If they shared a memory, let that memory influence the atmosphere of
the experience without inventing details.

Make the person feel that they are being invited into a moment,
not given a task.

The experience should feel suitable for their available time.

Music may be suggested as an optional companion.

End naturally by encouraging them to put the phone away so they can
experience the surroundings instead of documenting them.
"""

    with st.spinner("Creating your little outside... 🌿"):

        try:

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",

                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],

                max_tokens=450,

                temperature=0.8
            )

            experience = response.choices[0].message.content

        except Exception as e:

            st.error(
                "Something went wrong while creating your experience."
            )

            st.caption(str(e))

            st.stop()


    # -----------------------------------------------------
    # SHOW EXPERIENCE
    # -----------------------------------------------------

    st.divider()

    st.subheader("Your little outside 🌿")

    st.markdown(experience)

    st.divider()

    st.info(
        "When you're ready, let the screen become less important. "
        "The moment is waiting outside."
    )

    # -----------------------------------------------------
# GO OUTSIDE — FINAL TRANSITION
# -----------------------------------------------------

if "going_outside" not in st.session_state:
    st.session_state.going_outside = False


if not st.session_state.going_outside:

    if st.button(
        "🌿 I'm going outside",
        use_container_width=True
    ):
        st.session_state.going_outside = True
        st.rerun()


else:

    st.empty()

    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 80px 20px 100px 20px;
        ">

        <div style="font-size: 70px;">🌿</div>

        <h1>Go.</h1>

        <p style="font-size: 20px;">
        You don't need to capture this moment.
        </p>

        <p style="font-size: 20px;">
        You don't need to share it.
        </p>

        <br>

        <p style="font-size: 22px;">
        <strong>Just give yourself a few minutes to be there.</strong>
        </p>

        <br>

        <p style="font-size: 18px;">
        We'll be here when you come back.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )