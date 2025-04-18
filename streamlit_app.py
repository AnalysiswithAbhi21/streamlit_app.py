import streamlit as st
import time
from random import randint

# Initialize session state variables
if 'player_index' not in st.session_state:
    st.session_state.player_index = 0
if 'coins' not in st.session_state:
    st.session_state.coins = {'Team A': 1000, 'Team B': 1000}  # Starting coins
if 'teams' not in st.session_state:
    st.session_state.teams = {'Team A': [], 'Team B': []}
if 'current_bid' not in st.session_state:
    st.session_state.current_bid = 0
if 'current_bidder' not in st.session_state:
    st.session_state.current_bidder = None
if 'player_time' not in st.session_state:
    st.session_state.player_time = randint(10, 15)  # Random auction time for each player

# Define the players with their base prices, categories, and image links
players = [
    {"name": "Vaishnav", "category": "Batsman", "base_price": 100, "image": "https://via.placeholder.com/150?text=Vaishnav"},
    {"name": "Sahil", "category": "Bowler", "base_price": 80, "image": "https://via.placeholder.com/150?text=Sahil"},
    {"name": "Daya", "category": "All-rounder", "base_price": 120, "image": "https://via.placeholder.com/150?text=Daya"},
    {"name": "Zarkar", "category": "Batsman", "base_price": 90, "image": "https://via.placeholder.com/150?text=Zarkar"},
    {"name": "Shrnav", "category": "Bowler", "base_price": 70, "image": "https://via.placeholder.com/150?text=Shrnav"},
    {"name": "Rohit", "category": "All-rounder", "base_price": 130, "image": "https://via.placeholder.com/150?text=Rohit"},
    {"name": "Abhi", "category": "Batsman", "base_price": 110, "image": "https://via.placeholder.com/150?text=Abhi"},
    {"name": "Bilat", "category": "Bowler", "base_price": 75, "image": "https://via.placeholder.com/150?text=Bilat"},
    {"name": "Prashant", "category": "All-rounder", "base_price": 100, "image": "https://via.placeholder.com/150?text=Prashant"},
    {"name": "Rohan", "category": "Batsman", "base_price": 95, "image": "https://via.placeholder.com/150?text=Rohan"}
]

# Set page layout
st.set_page_config(page_title="Haribhau Cricket League Auction", layout="wide")

# Display header
st.markdown("# 🏏 Haribhau Cricket League Auction")
st.markdown("### 🏆 2 Teams - Auction with 1000 coins each")
st.markdown("### 🎯 Bid players based on their base price and category")

# Show teams and remaining coins in a neat grid
st.sidebar.markdown("### 📊 Team Status")
for team, members in st.session_state.teams.items():
    st.sidebar.markdown(f"**{team}**")
    st.sidebar.markdown(f"Players: {', '.join(members) if members else 'No players yet'}")
    st.sidebar.markdown(f"Coins Left: {st.session_state.coins[team]}")

# Check if auction is over
if st.session_state.player_index >= len(players):
    st.success("🎉 Auction Completed! Final Team Results Below:")
    for team, members in st.session_state.teams.items():
        st.markdown(f"### {team}")
        st.markdown(f"**Players**: {', '.join(members) if members else 'No players assigned'}")
    st.stop()

# Current player being auctioned with image
current_player = players[st.session_state.player_index]
st.markdown(f"### 👤 Now Auctioning: **{current_player['name']}**")
st.image(current_player['image'], caption=current_player['name'], width=150)
st.markdown(f"**Category**: {current_player['category']}")
st.markdown(f"**Base Price**: {current_player['base_price']} Coins")
st.markdown(f"**💸 Current Bid**: {st.session_state.current_bid}")
if st.session_state.current_bidder:
    st.markdown(f"**🔝 Highest Bidder**: {st.session_state.current_bidder}")

# Bidding columns (for each team)
col1, col2 = st.columns(2)
for col, team in zip((col1, col2), ['Team A', 'Team B']):
    with col:
        st.markdown(f"#### {team}")
        st.markdown(f"**🪙 Coins Left**: {st.session_state.coins[team]}")
        if st.button(f"{team} Bid +10", key=f"{team}_bid"):
            if st.session_state.coins[team] >= st.session_state.current_bid + 10:
                st.session_state.current_bid += 10
                st.session_state.current_bidder = team

# Finalize bid and move to the next player
if st.button("🏁 Finalize Bid"):
    if st.session_state.current_bidder:
        winner = st.session_state.current_bidder
        cost = st.session_state.current_bid
        st.session_state.teams[winner].append(current_player['name'])
        st.session_state.coins[winner] -= cost

    # Move to the next player after finalizing the bid
    st.session_state.player_index += 1  # Move to the next player
    st.session_state.current_bid = 0  # Reset current bid
    st.session_state.current_bidder = None  # Reset the current bidder
    st.session_state.player_time = randint(10, 15)  # Set a new random auction time for next player

# Show "Next Player" button for manual progression
if st.button("Next Player"):
    # Ensure the next player is available
    if st.session_state.player_index < len(players):
        st.session_state.player_index += 1
        st.session_state.current_bid = 0  # Reset current bid
        st.session_state.current_bidder = None  # Reset the current bidder
        st.session_state.player_time = randint(10, 15)  # Set a new random auction time for next player

# Show live team status
st.divider()
st.markdown("### 📊 Live Team Status")
col1, col2 = st.columns(2)
for col, team in zip((col1, col2), ['Team A', 'Team B']):
    with col:
        st.markdown(f"**{team}**")
        st.markdown(f"Players: {', '.join(st.session_state.teams[team]) if st.session_state.teams[team] else 'No players yet'}")
