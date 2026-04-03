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
    "#1f77b4",  # Emotional & Mental Well-Being (Blue)
    "#2ca02c",  # Environment & Physical Well-Being (Green)
    "#ff7f0e",  # Career & Professional Fulfillment (Orange)
    "#d62728",  # Financial Security & Freedom (Red)
    "#9467bd",  # Family Life (Purple)
    "#8c564b",  # Play, Creativity & Adventure (Brown)
    "#17becf",  # Personal Growth & Self-Development (Cyan)
    "#bcbd22",  # Purpose & Contribution (Olive)
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

st.subheader("📊 Wheel of Life")


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
    ax.set_yticks(range(1,11))
    ax.set_yticklabels([])
    ax.set_xticks([])
    #ax.legend(bars, labels, loc="center left", bbox_to_anchor=(1.1, 0.5), fontsize=14, handlelength=2)

    #radial labels
    label_radius = 10.5
    for angle, label in zip(angles, labels):
        rotation = np.degrees(angle)
        if np.pi / 2 < angle < 3 * np.pi / 2:
            rotation += 180
            ha = "right"
        else:
            ha = "left"
        ax.text(angle, label_radius,label,rotation=rotation,rotation_mode="anchor",ha=ha,va="center",fontsize=11)
    st.pyplot(fig)

plot_polar_wheel(scores)

st.subheader("🧾 Score Summary")
st.dataframe(df, use_container_width=True)

average_score = df["Score"].mean()
st.metric("Overall Life Balance Score", f"{average_score:.2f} / 10")

st.caption("Built with Streamlit 🚀")
