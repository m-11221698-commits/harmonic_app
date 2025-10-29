import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- YouTube playlists ---
youtube_playlists = {
    "K-pop": [
        "https://www.youtube.com/watch?v=gdZLi9oWNZg",  # BTS - Dynamite
        "https://www.youtube.com/watch?v=ioNng23DkIM",  # BLACKPINK - How You Like That
        "https://www.youtube.com/watch?v=MBdVXkSdhwU"   # BTS - Boy With Luv
    ],
    "English pop": [
        "https://www.youtube.com/watch?v=UceaB4D0jpo",  # Ed Sheeran - Perfect
        "https://www.youtube.com/watch?v=2Vv-BfVoq4g",  # Ed Sheeran - Shape of You
        "https://www.youtube.com/watch?v=kXYiU_JCYtU"   # Linkin Park - Numb
    ],
    "Jazz": [
        "https://www.youtube.com/watch?v=HMnrl0tmd3k",  # Chet Baker - Almost Blue
        "https://www.youtube.com/watch?v=VMkIuKXwmlU",  # Dave Brubeck - Take Five
        "https://www.youtube.com/watch?v=zqNTltOGh5c"   # Miles Davis - So What
    ],
    "Rock and Roll": [
        "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",  # Queen - Bohemian Rhapsody
        "https://www.youtube.com/watch?v=xbhCPt6PZIU",  # The Beatles - Come Together
        "https://www.youtube.com/watch?v=ktvTqknDobU"   # Imagine Dragons - Radioactive
    ],
    "Classical": [
        "https://www.youtube.com/watch?v=GRxofEmo3HA",  # Vivaldi - Spring
        "https://www.youtube.com/watch?v=4Tr0otuiQuU",  # Beethoven - Moonlight Sonata
        "https://www.youtube.com/watch?v=Rb0UmrCXxVA"   # Mozart - Eine kleine Nachtmusik
    ],
    "Hip-Hop": [
        "https://www.youtube.com/watch?v=ioNng23DkIM",  # (Example) BLACKPINK – How You Like That (rap sections)
        "https://www.youtube.com/watch?v=E5ONTXHS2mM",  # Eminem - Lose Yourself
        "https://www.youtube.com/watch?v=YVkUvmDQ3HY"   # Eminem - Without Me
    ],
    "EDM": [
...         "https://www.youtube.com/watch?v=60ItHLz5WEA",  # Alan Walker - Faded
...         "https://www.youtube.com/watch?v=IcrbM1l_BoI",  # Avicii - Wake Me Up
...         "https://www.youtube.com/watch?v=fLexgOxsZu0"   # Mark Ronson - Uptown Funk
...     ],
...     "R&B / Soul": [
...         "https://www.youtube.com/watch?v=450p7goxZqg",  # The Weeknd - Blinding Lights
...         "https://www.youtube.com/watch?v=YVkUvmDQ3HY",  # Eminem - Without Me (crossover)
...         "https://www.youtube.com/watch?v=bnVUHWCynig"   # Bruno Mars - Versace on the Floor
...     ],
...     "Country": [
...         "https://www.youtube.com/watch?v=1vrEljMfXYo",  # John Denver - Take Me Home, Country Roads
...         "https://www.youtube.com/watch?v=Z9bajItFz8w",  # Dolly Parton - 9 to 5
...         "https://www.youtube.com/watch?v=Fq3QmtV8vT0"   # Luke Bryan - Play It Again
...     ],
...     "Lo-fi Chill": [
...         "https://www.youtube.com/watch?v=5qap5aO4i9A",  # Lofi Girl - Beats to relax/study to
...         "https://www.youtube.com/watch?v=hHW1oY26kxQ",  # Chillhop - Relaxing beats
...         "https://www.youtube.com/watch?v=jfKfPfyJRdk"   # Lofi hip hop radio
...     ]
... }
... 
... # --- Mood list ---
... mood_list = [
...     "happy", "sad", "chill", "excited", "satisfied", "thrilling",
...     "confident", "depressed", "anxious", "overwhelmed", "stressed", "sleepy"
... ]
... 
... # --- Data file ---
... DATA_FILE = "mood_data.csv"
... 
... def load_data():
...     try:
...         df = pd.read_csv(DATA_FILE)
...         df["date"] = pd.to_datetime(df["date"])
...         return df
...     except FileNotFoundError:
...         return pd.DataFrame(columns=["date", "day_rating", "mood", "genre", "experience_rating"])
... 
... def save_data(df):
...     df.to_csv(DATA_FILE, index=False)
... 
... # --- Streamlit setup ---
... st.set_page_config(page_title="🎵 Mood Tracker & Music Playlist", layout="centered")
... st.title("🎧 Mood Tracker & Music Playlist Generator")
... st.write("Track your emotions, listen to music based on your mood, and view your emotional trends!")
... 
data = load_data()

# ----------------------------
# USER INPUT SECTION
# ----------------------------
day_rating = st.slider("1️⃣ How was your day? (Rate 1-10)", 1, 10, 5)
mood_selected = st.selectbox("2️⃣ How are you feeling right now?", mood_list)
genre_selected = st.selectbox("3️⃣ What kind of genre of music do you want?", list(youtube_playlists.keys()))

# Show Playlist
if st.button("🎵 Show My Playlist"):
    st.subheader(f"Here are some {genre_selected} songs for your mood:")
    for song in youtube_playlists[genre_selected]:
        st.write(f"[▶️ Watch here]({song})")

experience_rating = st.slider("4️⃣ Was it great? Rate your experience (1-5)", 1, 5, 3)

# Save entry
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

# ----------------------------
# STATISTICS SECTION
# ----------------------------
st.header("📊 Mood & Genre Statistics")

if not data.empty:
    # --- Mood Frequency Chart ---
    mood_counts = data["mood"].value_counts()
    st.subheader("🎭 Mood Frequency Chart")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.bar(mood_counts.index, mood_counts.values, color="lightcoral")
    ax1.set_title("Mood Frequency Over Time")
    ax1.set_xlabel("Mood")
    ax1.set_ylabel("Count")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # --- Genre Frequency Chart ---
    genre_counts = data["genre"].value_counts()
    st.subheader("🎶 Genre Frequency Chart")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.bar(genre_counts.index, genre_counts.values, color="skyblue")
    ax2.set_title("Genre Frequency Over Time")
    ax2.set_xlabel("Genre")
    ax2.set_ylabel("Count")
    plt.xticks(rotation=30)
    st.pyplot(fig2)

    # --- Summary Statistics ---
    st.subheader("🏆 Summary Statistics")
    top_mood = mood_counts.idxmax()
    top_genre = genre_counts.idxmax()

    st.markdown(f"**Most Frequent Mood:** 🥇 `{top_mood}` ({mood_counts[top_mood]} times)")
    st.markdown(f"**Most Listened Genre:** 🎧 `{top_genre}` ({genre_counts[top_genre]} times)")

    # ----------------------------
    # WEEKLY / BIWEEKLY STATISTICS
    # ----------------------------
    st.header("📅 Weekly / Biweekly Mood Trends")

    data["week"] = data["date"].dt.isocalendar().week
    weekly_avg = data.groupby("week")["day_rating"].mean().reset_index()

    st.subheader("📈 Weekly Average Day Rating")
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.plot(weekly_avg["week"], weekly_avg["day_rating"], marker='o', color="mediumseagreen")
    ax3.set_title("Average Day Rating per Week")
    ax3.set_xlabel("Week Number")
    ax3.set_ylabel("Average Rating (1-10)")
    ax3.grid(True)
    st.pyplot(fig3)

    avg_day_rating = data["day_rating"].mean()
    avg_experience_rating = data["experience_rating"].mean()

    st.markdown(f"**Average Day Rating:** 🌞 {avg_day_rating:.2f}/10")
    st.markdown(f"**Average Experience Rating:** 🎧 {avg_experience_rating:.2f}/5")

    st.subheader("🗂️ Recent Mood Records")
    st.dataframe(data.tail(10))

else:
    st.info("No data available yet. Save your first mood entry to start tracking!")

st.write("---")

