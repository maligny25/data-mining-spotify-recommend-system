import pandas as pd
import streamlit as st


st.set_page_config(page_title="Spotify Recommender", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("spotify_features_scaled.csv")
    df["display_name"] = df["track_name"] + " - " + df ["artists"]
    return df

df = load_data()

if "selected_songs" not in st.session_state:
    st.session_state.selected_songs = []

if "current_page" not in st.session_state:
    st.session_state.current_page = 1

PAGE_SIZE = 20

def add_song(song_dict):
    if not any(s["track_id"] == song_dict["track_id"] for s in st.session_state.selected_songs):
        st.session_state.selected_songs.append(song_dict)

def remove_song(track_id):
    st.session_state.selected_songs = [
        s for s in st.session_state.selected_songs if s["track_id"] != track_id
    ]

st.title("Spotify Recommender 🎵")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 Song Search")
    search_query = st.text_input("Write an artist or a song name:", "")

    if search_query.strip():
        display_df = df[df["display_name"].str.contains(search_query, case=False,na=False)]
    else:
        display_df = df

    total_songs = len(display_df)
    total_pages = max(1, (total_songs-1) // PAGE_SIZE + 1)

    if st.session_state.current_page > total_pages:
        st.session_state.current_page = 1

    start_idx = (st.session_state.current_page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE
    page_tracks = display_df.iloc[start_idx:end_idx]

    st.caption(f"{total_songs:,} songs - Page {st.session_state.current_page} / {total_pages}")

    for _, row in page_tracks.iterrows():
        r_col1, r_col2 = st.columns([5,1])

        with r_col1:
            st.write(f"**{row['track_name']}** - *{row['artists']}*")
        with r_col2:
            if st.button("➕", key=f"add_{row['track_id']}"):
                add_song({
                    "track_id": row["track_id"],
                    "track_name": row["track_name"],
                    "artists": row["artists"],
                    "track_genre" : row["track_genre"],
                })
                st.rerun()

    st.divider()
    nav1 ,nav2, nav3 = st.columns([1,2,1])
    with nav1:
        if st.button("◀ Previous", disabled = st.session_state.current_page <= 1):
            st.session_state.current_page -= 1
            st.rerun()
    with nav2:
        st.markdown(f"<div style='text-align: center; padding-top: 5px; '>Sayfa <b>{st.session_state.current_page}</b> / {total_pages}</div>", unsafe_allow_html=True)
    with nav3:
        if st.button("Next ▶", disabled = (st.session_state.current_page >= total_pages)):
            st.session_state.current_page += 1
            st.rerun()

with col2:
    st.subheader("📋 Selected Songs")

    if not st.session_state.selected_songs:
        st.info("You must select at least one song. You can select the songs from the list on left side.")
    else:
        st.write(f"Selected Songs Count: **{len(st.session_state.selected_songs)}**")

        for song in st.session_state.selected_songs:
            s_col1, s_col2 = st.columns([5,1])
            with s_col1:
                st.write(f"🎵 **{song['track_name']}** - **{song['artists']}**")
            with s_col2:
                if st.button("❌", key=f"del_{song['track_id']}"):
                    remove_song(song["track_id"])
                    st.rerun()