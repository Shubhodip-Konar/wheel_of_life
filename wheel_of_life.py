import re

import smtplib

from io import StringIO, BytesIO

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from email.mime.image import MIMEImage

 

import streamlit as st

import pandas as pd

import matplotlib.pyplot as plt

import numpy as np

 

# -----------------------------

# PAGE CONFIG

# -----------------------------

st.set_page_config(

    page_title="Wheel of Life",

    layout="centered"

)

 

# -----------------------------

# CONSTANTS

# -----------------------------

RECIPIENT_EMAIL = "lets_explore@mindyourtrap.com"

SMTP_SERVER = "smtp.gmail.com"

SMTP_PORT = 587

 

AREAS = [
    "Health and Vitality",
 
    "Emotional & Mental Well-Being",

    "Environment & Physical Surroundings",

    "Career & Professional Fulfillment",

    "Financial Security & Freedom",

    "Romantic & Intimate Relationship",

    "Family Life",

    "Friendships & Social Connection",

    "Personal Growth & Self Development",

    "Joy & Inner Peace",

    "Play, Creativity & Adventure",

    "Purpose & Contribution"

]

 

# Enough colors for all 12 life areas

COLORS = plt.cm.tab20(np.linspace(0, 1, len(AREAS)))

 

# -----------------------------

# SESSION STATE

# -----------------------------

if "assessment_started" not in st.session_state:

    st.session_state.assessment_started = False

 

if "submitted" not in st.session_state:

    st.session_state.submitted = False

 

# -----------------------------

# HELPERS

# -----------------------------

def is_valid_email(email: str) -> bool:

    """

    Basic email format validation.

    """

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return bool(re.match(pattern, email.strip()))

 

def build_scores_dataframe(scores_dict):

    return pd.DataFrame(

        list(scores_dict.items()),

        columns=["Life Area", "Score"]

    )

 

def create_wheel_figure(scores_dict):

    """

    Create the polar wheel figure and return the matplotlib figure.

    """

    labels = list(scores_dict.keys())

    values = list(scores_dict.values())

    n = len(labels)

 

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)

    width = 2 * np.pi / n

 

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))

 

    # Start from top and move clockwise

    ax.set_theta_offset(np.pi / 2)

    ax.set_theta_direction(-1)

 

    bars = ax.bar(

        angles,

        values,

        width=width,

        bottom=0,

        color=COLORS,

        edgecolor="black",

        linewidth=1

    )

 

    ax.set_ylim(0, 10)

    ax.set_yticks(range(1, 11))

    ax.set_yticklabels([])

    ax.set_xticks([])

 

    ax.set_title("Wheel of Life", fontsize=16, pad=20)

 

    ax.legend(

        bars,

        labels,

        loc="center left",

        bbox_to_anchor=(1.08, 0.5),

        fontsize=9,

        frameon=False

    )

 

    plt.tight_layout()

    return fig

 

def figure_to_png_bytes(fig):

    """

    Convert matplotlib figure to PNG bytes for email attachment.

    """

    buf = BytesIO()

    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")

    buf.seek(0)

    return buf.read()

 

def send_email(name, user_email, df, average_score, wheel_png_bytes):

    """

    Send assessment results to the fixed recipient and attach wheel image.

    Gmail sender credentials are read from Streamlit secrets.

    """

    sender_email = st.secrets["gmail_sender"]

    sender_password = st.secrets["gmail_app_password"]

    app_name = st.secrets.get("app_name", "WheelOfLife_MYT")

 

    subject = f"{app_name} - New Wheel of Life Submission from {name}"

 

    # Plain text score table

    table_buffer = StringIO()

    df.to_string(table_buffer, index=False)

    score_table = table_buffer.getvalue()

 

    text_body = f"""

New Wheel of Life Assessment Submitted

 

Participant Details

-------------------

Name: {name}

Email: {user_email}

 

Scores

------

{score_table}

 

Overall Life Balance Score: {average_score:.2f} / 10

"""

 

    html_rows = "".join(

        f"<tr><td style='padding:8px;border:1px solid #ddd;'>{row['Life Area']}</td>"

        f"<td style='padding:8px;border:1px solid #ddd;text-align:center;'>{row['Score']}</td></tr>"

        for _, row in df.iterrows()

    )

 

    html_body = f"""

    <html>

        <body style="font-family: Arial, sans-serif; color: #222;">

            <h2>New Wheel of Life Assessment Submitted</h2>

 

            <h3>Participant Details</h3>

            <p><strong>Name:</strong> {name}<br>

            <strong>Email:</strong> {user_email}</p>

 

            <h3>Scores</h3>

            <table style="border-collapse: collapse; width: 100%; max-width: 700px;">

                <thead>

                    <tr>

                        <th style="padding:8px;border:1px solid #ddd;background:#f5f5f5;text-align:left;">Life Area</th>

                        <th style="padding:8px;border:1px solid #ddd;background:#f5f5f5;text-align:center;">Score</th>

                    </tr>

                </thead>

                <tbody>

                    {html_rows}

                </tbody>

            </table>

 

            <p style="margin-top:16px;">

                <strong>Overall Life Balance Score:</strong> {average_score:.2f} / 10

            </p>

 

            <p>The wheel chart is attached as an image.</p>

        </body>

    </html>

    """

 

    # Root mixed message for text/html + image attachment

    msg = MIMEMultipart("mixed")

    msg["From"] = sender_email

    msg["To"] = RECIPIENT_EMAIL

    msg["Subject"] = subject

 

    # Alternative part for plain text + HTML

    alt_part = MIMEMultipart("alternative")

    alt_part.attach(MIMEText(text_body, "plain"))

    alt_part.attach(MIMEText(html_body, "html"))

    msg.attach(alt_part)

 

    # Attach wheel image

    image_part = MIMEImage(wheel_png_bytes, _subtype="png")

    image_part.add_header("Content-Disposition", "attachment", filename="wheel_of_life.png")

    msg.attach(image_part)

 

    # Send mail

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    server.starttls()

    server.login(sender_email, sender_password)

    server.sendmail(sender_email, RECIPIENT_EMAIL, msg.as_string())

    server.quit()

 

# -----------------------------

# HEADER

# -----------------------------

st.title("🛞 Wheel of Life Assessment")

st.write("https://mindyourtrap.com/")


 

# -----------------------------

# USER DETAILS

# -----------------------------

st.subheader("👤 Your Details")

 

name = st.text_input(

    "Full Name",

    key="name_input",

    placeholder="Enter your full name"

)

 

user_email = st.text_input(

    "Email Address",

    key="email_input",

    placeholder="Enter your email address"

)

 

name_filled = bool(name.strip())

email_filled = bool(user_email.strip())

email_valid = is_valid_email(user_email) if email_filled else False

details_valid = name_filled and email_valid

 

if email_filled and not email_valid:

    st.warning("Please enter a valid email address.")

 

col1, col2 = st.columns([1, 1])

 

with col1:

    if st.button("▶️ Start Assessment", disabled=not details_valid, use_container_width=True):

        st.session_state.assessment_started = True

        st.session_state.submitted = False

        st.rerun()

 

with col2:

    if st.button("🔄 Reset", use_container_width=True):

        st.session_state.assessment_started = False

        st.session_state.submitted = False

        for area in AREAS:

            if f"slider_{area}" in st.session_state:

                del st.session_state[f"slider_{area}"]

        st.rerun()

 

if not st.session_state.assessment_started:

    st.info("Enter your name and a valid email, then click **Start Assessment** to begin.")

 

# -----------------------------

# ASSESSMENT

# -----------------------------

if st.session_state.assessment_started and details_valid:

    st.subheader("🎚️ Your Ratings")
    st.write("Rate each area of your life from **1 (very low)** to **10 (excellent)**.")

 

    scores = {}

    for area in AREAS:

        scores[area] = st.slider(

            area,

            min_value=1,

            max_value=10,

            value=5,

            key=f"slider_{area}"

        )

 

    df = build_scores_dataframe(scores)

    average_score = df["Score"].mean()

 

    st.subheader("📊 Wheel of Life")

    fig = create_wheel_figure(scores)

    st.pyplot(fig)

 

    st.subheader("🧾 Score Summary")

    st.dataframe(df, use_container_width=True)

    st.metric("Overall Life Balance Score", f"{average_score:.2f} / 10")

 

    if st.button("📨 Submit Assessment", use_container_width=True):

        try:

            wheel_png = figure_to_png_bytes(fig)

            send_email(

                name=name.strip(),

                user_email=user_email.strip(),

                df=df,

                average_score=average_score,

                wheel_png_bytes=wheel_png

            )

            st.session_state.submitted = True

            st.success("Assessment submitted successfully.")

        except Exception as e:

            st.error(f"Unable to send email. Error: {e}")

 

    plt.close(fig)

 

# -----------------------------

# FOOTER

# -----------------------------

st.caption("Built with Streamlit 🚀")
