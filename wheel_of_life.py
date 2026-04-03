import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Wheel of Life",
    layout="centered"
)

st.title("🛞 Wheel of Life Assessment")
st.write("https://mindyourtrap.com/")
st.write(
    "Rate each area of your life from **1 (very low)** to **10 (excellent)**."
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
colors = [
    "#4E79A7",  # Emotional & Mental Well-Being (Blue)
    "#59A14F",  # Environment & Physical Well-Being (Green)
    "#F28E2B",  # Career & Professional Fulfillment (Orange)
    "#E15759",  # Financial Security & Freedom (Red)
    "#B07AA1",  # Family Life (Purple)
    "#FF9DA7",  # Play, Creativity & Adventure (Pink)
    "#76B7B2",  # Personal Growth & Self-Development (Teal)
    "#EDC948",  # Purpose & Contribution (Yellow)
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


def plot_polar_wheel(scores_dict):
    labels = list(scores_dict.keys())
    values = list(scores_dict.values())
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    width = 2 * np.pi / N
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    #start from top and go clockwise
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    bars = ax.bar(angles, values, width=width, bottom=0.0, color=colors, edgecolor="black")
    
    # legends on the right side
    #axis settings
    ax.set_ylim(0, 10)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title("Your Life Balance", pad=20)
    ax.legend(bars, labels, loc="center left", bbox_to_anchor=(1.1, 0.5), title="Life Areas")
    st.pyplot(fig)

plot_polar_wheel(scores)

st.subheader("🧾 Score Summary")
st.dataframe(df, use_container_width=True)

average_score = df["Score"].mean()
st.metric("Overall Life Balance Score", f"{average_score:.2f} / 10")

st.caption("Built with Streamlit 🚀")
