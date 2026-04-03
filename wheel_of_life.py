import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Wheel of Life",
    layout="centered"
)

st.title("🛞 Wheel of Life_Mind Your Trap")
st.write("https://mindyourtrap.com/")
st.write(
    "Rate each area of your life from **0 (very low)** to **9 (excellent)**."
)

areas = [
    "Emotional & Mental Well‑Being",
    "Environment & Physical Well‑Being",
    "Career & Professional Fulfillment",
    "Financial Security & Freedom",
    "Romantic & Intimate Relationship",
    "Family Life",
    "Friendships & Social Connection",
    "Joy & Inner Peace",
    "Personal Growth & Self‑Development",
    "Play, Creativity & Adventure",
    "Purpose & Contribution",
    "Physical Well‑Being"
]

st.subheader("🎚️ Your Ratings")

scores = {}
for area in areas:
    scores[area] = st.slider(
        area,
        min_value=1,
        max_value=10,
        value=5
    )

df = pd.DataFrame(
    list(scores.items()),
    columns=["Life Area", "Score"]
)

st.subheader("📊 Wheel of Life Chart")

def plot_wheel_of_life(dataframe):
    labels = dataframe["Life Area"].tolist()
    scores = dataframe["Score"].tolist()

    scores += scores[:1]
    angles = np.linspace(
        0, 2 * np.pi, len(labels) + 1, endpoint=True
    )

    fig = plt.figure(figsize=(7, 7))
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, scores, linewidth=2)
    ax.fill(angles, scores, alpha=0.25)

    ax.set_thetagrids(
        angles[:-1] * 180 / np.pi,
        labels
    )

    #ax.set_ylim(0, 9)
    ax.set_yticks(range(0, 10))
    ax.set_title("Your Life Balance", pad=20)

    st.pyplot(fig)

plot_wheel_of_life(df)

st.subheader("🧾 Score Summary")
st.dataframe(df, use_container_width=True)

average_score = df["Score"].mean()
st.metric("Overall Life Balance Score", f"{average_score:.2f} / 10")

st.caption("Built with Streamlit 🚀")
