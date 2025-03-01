import streamlit as st
import pandas as pd
import numpy as np
import random
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="NBA Dawg Bowl Fantasy Draft",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .captain {
        background-color: #FFD700;
        border-radius: 5px;
        padding: 5px;
        font-weight: bold;
    }
    .player-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        background-color: #f9f9f9;
    }
    .player-name {
        font-weight: bold;
        font-size: 18px;
        color: #000000;
    }
    .player-details {
        color: #555;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Mock data - just player names and salaries
def get_dawg_bowl_contestants():
    return [
        {"id": 101, "name": "SamOlson31", "salary": 9800},
        {"id": 102, "name": "In3us", "salary": 10200},
        {"id": 103, "name": "bestballviper", "salary": 10500},
        {"id": 104, "name": "DFSKing99", "salary": 9500},
        {"id": 105, "name": "NBAGuru42", "salary": 8800},
        {"id": 106, "name": "FantasyPro", "salary": 9300},
        {"id": 107, "name": "CelticsNation", "salary": 8400},
        {"id": 108, "name": "LakeShow23", "salary": 8900},
        {"id": 109, "name": "HoopDreams", "salary": 7900},
        {"id": 110, "name": "StatKing", "salary": 7600},
        {"id": 111, "name": "DFSmaster", "salary": 9400},
        {"id": 112, "name": "LineupLock", "salary": 9100},
        {"id": 113, "name": "OptimalDFS", "salary": 8600},
        {"id": 114, "name": "PickSixer", "salary": 7100},
        {"id": 115, "name": "CapWiz", "salary": 7400},
        {"id": 116, "name": "FadeThePublic", "salary": 8200},
        {"id": 117, "name": "SlateBreaker", "salary": 9000},
        {"id": 118, "name": "ValueHunter", "salary": 8000},
    ]

def simulate_performance(selected_players, captain_id):
    # Simple performance simulation
    results = []
    total_points = 0
    
    for player in selected_players:
        # Generate random points between 20-60
        fantasy_points = random.uniform(20, 60)
        
        # Apply captain multiplier
        multiplier = 1.5 if player["id"] == captain_id else 1.0
        final_points = fantasy_points * multiplier
        
        results.append({
            "id": player["id"],
            "name": player["name"],
            "fantasy_points": fantasy_points,
            "multiplier": multiplier,
            "final_points": final_points
        })
        
        total_points += final_points
    
    # Sort by fantasy points for display
    results.sort(key=lambda x: x["final_points"], reverse=True)
    
    return results, total_points

# Main app
def main():
    st.title("🏀 NBA Dawg Bowl Fantasy Draft")
    
    # Sidebar for instructions and settings
    with st.sidebar:
        st.header("How It Works")
        st.write("""
        1. Draft your lineup of NBA Dawg Bowl competitors
        2. Select 1 Captain (scores 1.5x points) and 5 Flex players
        3. Stay under the salary cap
        4. Submit your lineup to see results
        """)
        
        st.header("Settings")
        salary_cap = st.slider("Salary Cap", 40000, 60000, 50000, 1000)
    
    # Initialize session state
    if 'selected_players' not in st.session_state:
        st.session_state.selected_players = []
    if 'captain_id' not in st.session_state:
        st.session_state.captain_id = None
    if 'simulated' not in st.session_state:
        st.session_state.simulated = False
    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = []
    if 'total_points' not in st.session_state:
        st.session_state.total_points = 0
        
    # Main content
    if not st.session_state.simulated:
        # Show available players
        st.header("Available Dawg Bowl Competitors")
        all_players = get_dawg_bowl_contestants()
        
        # Filter and sort options
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("Sort By", ["Salary (High to Low)", "Salary (Low to High)", "Name (A-Z)"])
        with col2:
            search = st.text_input("Search Player")
        
        # Apply filters and sorting
        filtered_players = all_players
        
        if search:
            filtered_players = [p for p in filtered_players if search.lower() in p["name"].lower()]
        
        # Apply sorting
        if sort_by == "Salary (High to Low)":
            filtered_players.sort(key=lambda x: x["salary"], reverse=True)
        elif sort_by == "Salary (Low to High)":
            filtered_players.sort(key=lambda x: x["salary"])
        elif sort_by == "Name (A-Z)":
            filtered_players.sort(key=lambda x: x["name"])
        
        # Display players in a grid
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for i, player in enumerate(filtered_players):
            # Organize in 3 columns
            with cols[i % 3]:
                with st.container():
                    st.markdown(f"""
                    <div class="player-card">
                        <div class="player-name">{player["name"]}</div>
                        <div class="player-details">Salary: ${player["salary"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if player["id"] not in [p["id"] for p in st.session_state.selected_players]:
                            if len(st.session_state.selected_players) < 6:
                                if st.button(f"Add as FLEX", key=f"flex_{player['id']}"):
                                    st.session_state.selected_players.append(player)
                                    st.experimental_rerun()
                        else:
                            if st.button(f"Remove", key=f"remove_{player['id']}"):
                                st.session_state.selected_players = [p for p in st.session_state.selected_players if p["id"] != player["id"]]
                                if st.session_state.captain_id == player["id"]:
                                    st.session_state.captain_id = None
                                st.experimental_rerun()
                    
                    with col_b:
                        if player["id"] not in [p["id"] for p in st.session_state.selected_players]:
                            if len(st.session_state.selected_players) < 6:
                                if st.button(f"Add as CAPTAIN", key=f"captain_{player['id']}"):
                                    st.session_state.selected_players.append(player)
                                    st.session_state.captain_id = player["id"]
                                    st.experimental_rerun()
                        elif st.session_state.captain_id != player["id"]:
                            if st.button(f"Make CAPTAIN", key=f"make_captain_{player['id']}"):
                                st.session_state.captain_id = player["id"]
                                st.experimental_rerun()
        
        # Show selected lineup
        st.header("Your Lineup")
        
        if len(st.session_state.selected_players) > 0:
            total_salary = sum(player["salary"] for player in st.session_state.selected_players)
            remaining_salary = salary_cap - total_salary
            
            st.write(f"Salary: ${total_salary:,} / ${salary_cap:,} (${remaining_salary:,} remaining)")
            
            # Progress bar for salary cap
            st.progress(min(1.0, total_salary / salary_cap))
            
            # Display roster
            cols = st.columns(6)
            for i, player in enumerate(st.session_state.selected_players):
                with cols[i]:
                    is_captain = player["id"] == st.session_state.captain_id
                    position_label = "CAPTAIN" if is_captain else "FLEX"
                    
                    st.markdown(f"""
                    <div class="player-card {'captain' if is_captain else ''}">
                        <div class="player-name">{player["name"]}</div>
                        <div class="player-details">{position_label}</div>
                        <div class="player-details">${player["salary"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Check if lineup is valid for submission
            if len(st.session_state.selected_players) == 6 and st.session_state.captain_id is not None and total_salary <= salary_cap:
                if st.button("Submit Lineup", type="primary"):
                    # Simulate contest results
                    results, total = simulate_performance(st.session_state.selected_players, st.session_state.captain_id)
                    st.session_state.simulation_results = results
                    st.session_state.total_points = total
                    st.session_state.simulated = True
                    st.experimental_rerun()
            else:
                if len(st.session_state.selected_players) < 6:
                    st.warning(f"Please select {6 - len(st.session_state.selected_players)} more players")
                elif st.session_state.captain_id is None:
                    st.warning("Please select a captain")
                elif total_salary > salary_cap:
                    st.error(f"Lineup exceeds salary cap by ${total_salary - salary_cap:,}")
    
    else:
        # Show simulation results
        st.header("Results")
        
        # Add a back button
        if st.button("Create New Lineup"):
            st.session_state.selected_players = []
            st.session_state.captain_id = None
            st.session_state.simulated = False
            st.session_state.simulation_results = []
            st.session_state.total_points = 0
            st.experimental_rerun()
        
        st.subheader(f"Total Fantasy Points: {st.session_state.total_points:.2f}")
        
        # Visualize player contributions
        fig = px.bar(
            [result for result in st.session_state.simulation_results],
            x="name",
            y="final_points",
            title="Fantasy Points by Player",
            labels={"name": "Player", "final_points": "Fantasy Points"},
            text="final_points"
        )
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Display results table
        performance_data = []
        for result in st.session_state.simulation_results:
            performance_data.append({
                "Player": f"{result['name']} {'(C)' if result['multiplier'] > 1 else ''}",
                "Base Points": round(result["fantasy_points"], 1),
                "Multiplier": result["multiplier"],
                "Total Points": round(result["final_points"], 1)
            })
        
        performance_df = pd.DataFrame(performance_data)
        st.table(performance_df)
        
        # Mock leaderboard
        st.header("Leaderboard")
        
        # Generate random scores around the user's score
        user_score = st.session_state.total_points
        other_scores = [random.uniform(user_score * 0.8, user_score * 1.2) for _ in range(9)]
        other_scores.append(user_score)
        all_scores = sorted(other_scores, reverse=True)
        user_rank = all_scores.index(user_score) + 1
        
        # Create user list properly
        user_names = ["DawgMaster", "HustleKing", "CourtGeneral", "DefenseWizard", "FlexCapitol"]
        # Add remaining names
        for i in range(5, 10):
            user_names.append(f"Player{i+1}")
        # Replace the correct position with "You"
        user_names[user_rank - 1] = "You"
        
        leaderboard_data = {
            "Rank": list(range(1, 11)),
            "User": user_names,
            "Points": [round(score, 2) for score in all_scores],
            "Prize": ["$1,000", "$500", "$250", "$100", "$50", "$25", "$25", "$25", "$25", "$0"]
        }
        
        leaderboard_df = pd.DataFrame(leaderboard_data)
        st.table(leaderboard_df)

if __name__ == "__main__":
    main()
