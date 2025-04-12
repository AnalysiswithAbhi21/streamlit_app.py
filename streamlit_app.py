import streamlit as st
from streamlit_extras.colored_header import colored_header

# Initialize session state variables
if 'player_index' not in st.session_state:
    st.session_state.player_index = 0
if 'coins' not in st.session_state:
    st.session_state.coins = {'Team A': 100, 'Team B': 100}
if 'teams' not in st.session_state:
    st.session_state.teams = {'Team A': [], 'Team B': []}
if 'current_bid' not in st.session_state:
    st.session_state.current_bid = 0
if 'current_bidder' not in st.session_state:
    st.session_state.current_bidder = None
if 'rerun' not in st.session_state:
    st.session_state.rerun = False  # Add the rerun flag

# Trigger rerun if the session_state 'rerun' is set to True
if 'rerun' in st.session_state and st.session_state.rerun:
    st.session_state.rerun = False  # Reset the rerun flag
    st.experimental_rerun()  # Trigger a rerun

# Player list
players = [
    "Vaishnav", "Sahil", "Daya", "Zarkar", "Shrnav",
    "Rohit", "Abhi", "Bilat", "Prashant", "Rohan"
]

st.set_page_config(page_title="2-Team Auction", layout="centered")
colored_header("🏏 Haribhau Cricket League Auction", description="Bid players with 100 coins each", color_name="violet-70")

# Check if auction is over
if st.session_state.player_index >= len(players):
    st.success("🎉 Auction Completed! Final Team Results Below:")
    for team, members in st.session_state.teams.items():
        with st.expander(team):
            st.markdown(f"**Players**: {', '.join(members) if members else 'No players assigned'}")
    st.stop()

# Current player being auctioned
current_player = players[st.session_state.player_index]
st.markdown(f"### 👤 Now Auctioning: `{current_player}`")
st.markdown(f"**💸 Current Bid:** `{st.session_state.current_bid}`")
if st.session_state.current_bidder:
    st.markdown(f"**🔝 Highest Bidder:** `{st.session_state.current_bidder}`")

# Bidding columns
col1, col2 = st.columns(2)
for col, team in zip((col1, col2), ['Team A', 'Team B']):
    with col:
        st.markdown(f"#### {team}")
        st.markdown(f"**🪙 Coins Left:** {st.session_state.coins[team]}")
        if st.button(f"{team} Bid +5", key=team):
            if st.session_state.coins[team] >= st.session_state.current_bid + 5:
                st.session_state.current_bid += 5
                st.session_state.current_bidder = team

# Finalize bid
if st.button("🏁 Finalize Bid"):
    if st.session_state.current_bidder:
        winner = st.session_state.current_bidder
        cost = st.session_state.current_bid
        st.session_state.teams[winner].append(current_player)
        st.session_state.coins[winner] -= cost
    st.session_state.player_index += 1
    st.session_state.current_bid = 0
    st.session_state.current_bidder = None
    st.session_state.rerun = True  # Set the rerun flag to True to trigger re-run

# Team display
st.divider()
st.markdown("### 📊 Live Team Status")
col1, col2 = st.columns(2)
for col, team in zip((col1, col2), ['Team A', 'Team B']):
    with col:
        st.markdown(f"**{team}**")
        st.markdown(f"{', '.join(st.session_state.teams[team]) if st.session_state.teams[team] else 'No players yet'}")
