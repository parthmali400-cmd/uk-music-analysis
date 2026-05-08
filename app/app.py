import streamlit as st
import pandas as pd

st.set_page_config(page_title="UK Music Analysis", layout="wide")

st.title("🎵 UK Top 50 Playlist Analysis")

# Load data
df = pd.read_csv("data/uk_top50.csv")

# Fix date
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

# Clean data
df['artist'] = df['artist'].str.lower().str.strip()
df['is_collab'] = df['artist'].str.contains('&')
df['duration_min'] = df['duration_ms'] / 60000

# Sidebar filters
st.sidebar.header("Filters")
selected_artist = st.sidebar.selectbox("Select Artist", ["All"] + list(df['artist'].unique()))

if selected_artist != "All":
    df = df[df['artist'] == selected_artist]

# KPIs
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Songs", len(df))
col2.metric("Explicit %", round(df['is_explicit'].mean()*100, 2))
col3.metric("Collaboration %", round(df['is_collab'].mean()*100, 2))

# Charts
st.subheader("🎤 Top Artists")
st.bar_chart(df['artist'].value_counts().head(10))

st.subheader("💿 Album Type Distribution")
st.bar_chart(df['album_type'].value_counts())

st.subheader("🔞 Explicit Content")
st.bar_chart(df['is_explicit'].value_counts())

st.subheader("⏱️ Track Duration")
st.line_chart(df['duration_min'])

# Show data
st.subheader("📄 Dataset Preview")
st.dataframe(df)