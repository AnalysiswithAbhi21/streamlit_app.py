import streamlit as st
from random import randint

# Initialize session state variables
if 'player_index' not in st.session_state:
    st.session_state.player_index = 0
if 'coins' not in st.session_state:
    st.session_state.coins = {'Team A': 1000, 'Team B': 1000}  # Increased starting coins for better bidding
if 'teams' not in st.session_state:
    st.session_state.teams = {'Team A': [], 'Team B': []}
if 'current_bid' not in st.session_state:
    st.session_state.current_bid = 0
if 'current_bidder' not in st.session_state:
    st.session_state.current_bidder = None
if 'player_time' not in st.session_state:
    st.session_state.player_time = randint(10, 15)  # Random time for player bidding in seconds
if 'rerun' not in st.session_state:
    st.session_state.rerun = False  # For rerunning the app

# Trigger rerun if the session_state 'rerun' is set to True
if 'rerun' in st.session_state and st.session_state.rerun:
    st.session_state.rerun = False  # Reset the rerun flag
    st.experimental_rerun()  # Trigger a rerun

# Define the players with their base prices and categories
players = [
    {"name": "Vaishnav", "category": "Batsman", "base_price": 100},
    {"name": "Sahil", "category": "Bowler", "base_price": 80},
    {"name": "Daya", "category": "All-rounder", "base_price": 120},
    {"name": "Zarkar", "category": "Batsman", "base_price": 90},
    {"name": "Shrnav", "category": "Bowler", "base_price": 70},
    {"name": "Rohit", "category": "All-rounder", "base_price": 130},
    {"name": "Abhi", "category": "Batsman", "base_price": 110},
    {"name": "Bilat", "category": "Bowler", "base_price": 75},
    {"name": "Prashant", "category": "All-rounder", "base_price": 100},
    {"name": "Rohan", "category": "Batsman", "base_price": 95}
]

# Set page layout
st.set_page_config(page_title="Haribhau Cricket League Auction", layout="centered")

# Display header
st.markdown("# 🏏 Haribhau Cricket League Auction")
st.markdown("## 🏆 2 Teams - Auction with 1000 coins each")
st.markdown("### 🎯 Bid players based on their base price and category")

# Show teams and remaining coins
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

# Current player being auctioned
current_player = players[st.session_state.player_index]
st.markdown(f"### 👤 Now Auctioning: {current_player['name']}")
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

# Finalize bid
if st.button("🏁 Finalize Bid"):
    if st.session_state.current_bidder:
        winner = st.session_state.current_bidder
        cost = st.session_state.current_bid
        st.session_state.teams[winner].append(current_player['name'])
        st.session_state.coins[winner] -= cost
    st.session_state.player_index += 1
    st.session_state.current_bid = 0
    st.session_state.current_bidder = None
    st.session_state.rerun = True  # Set the rerun flag to True to trigger re-run

# Show live team status
st.divider()
st.markdown("### 📊 Live Team Status")
col1, col2 = st.columns(2)
for col, team in zip((col1, col2), ['Team A', 'Team B']):
    with col:
        st.markdown(f"**{team}**")
        st.markdown(f"Players: {', '.join(st.session_state.teams[team]) if st.session_state.teams[team] else 'No players yet'}")
