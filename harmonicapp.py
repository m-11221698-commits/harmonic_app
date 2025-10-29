import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- YouTube playlists ---
youtube_playlists = {
    "K-pop": [
        "https://www.youtube.com/watch?v=gdZLi9oWNZg",
        "https://www.youtube.com/watch?v=ioNng23DkIM",
        "https://www.youtube.com/watch?v=MBdVXkSdhwU"
    ],
    "English pop": [
        "https://www.youtube.com/watch?v=UceaB4D0jpo",
        "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
        "https://www.youtube.com/watch?v=kXYiU_JCYtU"
    ],
    "Jazz": [
        "https://www.youtube.com/watch?v=HMnrl0tmd3k",
        "https://www.youtube.com/watch?v=VMkIuKXwmlU",
        "https://www.youtube.com/watch?v=zqNTltOGh5c"
    ],
    "Rock and Roll": [
        "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",
        "https://www.youtube.com/watch?v=xbhCPt6PZIU",
        "https://www.youtube.com/watch?v=ktvTqknDobU"
    ],
    "Classical": [
        "https://www.youtube.com/watch?v=GRxofEmo3HA",
        "https://www.youtube.com/watch?v=4Tr0otuiQuU",
        "https://www.youtube.com/watch?v=Rb0UmrCXxVA"
    ],
    "Hip-Hop": [
        "https://www.youtube.com/watch?v=ioNng23DkIM",
        "https://www.youtube.com/watch?v=E5ONTXHS2mM",
        "https://www.youtube.com/watch?v=YVkUvmDQ3HY"
    ],
    "EDM": [
        "https://www.youtube.com/watch?v=60ItHLz5WEA",
        "https://www.youtube.com/watch?v=IcrbM1l_BoI",
        "https://www.youtube.com/watch?v=fLexgOxsZu0"
    ],
    "R&B / Soul": [
        "https://www.youtube.com/watch?v=450p7goxZqg",
        "https://www.youtube.com/watch?v=YVkUvmDQ3HY",
        "https://www.youtube.com/watch?v=bnVUHWCynig"
    ],
    "Country": [
        "https://www.youtube.com/watch?v=1vrEljMfXYo",
        "https://www.youtube.com/watch?v=Z9bajItFz8w",
        "https://www.youtube.com/watch?v=Fq3QmtV8vT0"
    ],
    "Lo-fi Chill": [
        "https://www.youtube.com/watch?v=5qap5aO4i9A",
        "https://www.youtube.com/watch?v=hHW1oY26kxQ",
        "https://www.youtube.com/watch?v=jfKfPfyJRdk"
    ]
}

# --- Mood list ---
mood_list = [
    "happy", "sad", "chill", "excited", "satisfied", "thrilling",
    "confident", "depressed", "anxious", "overwhelmed", "stressed", "sleepy"
]

# --- Data file ---
DATA_FILE = "mood_data.csv"

def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        df["date"] = pd.to_datetime(df["date"])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["date", "day_rating", "mood", "genre", "experience_rating"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- Streamlit setup ---
st.set_page_config(page_title="🎵 Mood Tracker & Music Playlist", layout="centered")
st.title("🎧 Mood Tracker & Music Playlist Generator")
st.write("Track your emotions, listen to music based on your mood, and view your emotional trends!")

data = load_data()

# USER INPUT SECTION
day_rating = st.slider("1️⃣ How was your day? (Rate 1-10)", 1, 10, 5)
mood_selected = st.selectbox("2️⃣ How are you feeling right now?", mood_list)
genre_selected = st.selectbox("3️⃣ What kind of genre of music do you want?", list(youtube_playlists.keys()))

if st.button("🎵 Show My Playlist"):
    st.subheader(f"Here are some {genre_selected} songs for your mood:")
    for song in youtube_playlists[genre_selected]:
        st.write(f"[▶️ Watch here]({song})")

experience_rating = st.slider("4️⃣ Was it great? Rate your experience (1-5)", 1, 5, 3)

if st.button("💾 Save My Mood Data"):
    new_entry = pd.DataFrame({
        "date": [datetime.now().strftime("%Y-%m-%d")],
        "day_rating": [day_rating],
        "mood": [mood_selected],
        "genre": [genre_selected],
        "experience_rating": [experience_rating]
    })
    data = pd.concat([data, new_entry], ignore_index=True)
    save_data(data)
    st.success("✅ Your mood data has been saved successfully!")

st.header("📊 Mood & Genre Statistics")

if not data.empty:
    mood_counts = data["mood"].value_counts()
    st.subheader("🎭 Mood Frequency Chart")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.bar(mood_counts.index, mood_counts.values)
    ax1.set_title("Mood Frequency Over Time")
    ax1.set_xlabel("Mood")
    ax1.set_ylabel("Count")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    genre_counts = data["genre"].value_counts()
    st.subheader("🎶 Genre Frequency Chart")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.bar(genre_counts.index, genre_counts.values)
    ax2.set_title("Genre Frequency Over Time")
    ax2.set_xlabel("Genre")
    ax2.set_ylabel("Count")
    plt.xticks(rotation=30)
    st.pyplot(fig2)

    st.subheader("🏆 Summary Statistics")
    top_mood = mood_counts.idxmax()
    top_genre = genre_counts.idxmax()

    st.markdown(f"**Most Frequent Mood:** 🥇 `{top_mood}`")
    st.markdown(f"**Most Listened Genre:** 🎧 `{top_genre}`")

    st.header("📅 Weekly Mood Trends")
    data["week"] = data["date"].dt.isocalendar().week
    weekly_avg = data.groupby("week")["day_rating"].mean().reset_index()

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.plot(weekly_avg["week"], weekly_avg["day_rating"], marker='o')
    ax3.set_xlabel("Week")
    ax3.set_ylabel("Average Rating")
    ax3.grid(True)
    st.pyplot(fig3)

    st.dataframe(data.tail(10))
else:
    st.info("No data yet — save your first mood entry!")

st.write("---")
st.caption("Created with ❤ using Streamlit | Music Mood Tracker Project")


