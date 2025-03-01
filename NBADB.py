import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

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
    }
    .player-details {
        color: #555;
        font-size: 14px;
    }
    .player-stats {
        margin-top: 5px;
        font-size: 14px;
    }
    .button-container {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }
    .contest-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #f5f5f5;
    }
    .contest-title {
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 5px;
    }
    .contest-details {
        color: #555;
        font-size: 14px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Mock data functions for NBA Dawg Bowl contestants
def get_dawg_bowl_contestants():
    return [
        {"id": 101, "name": "SamOlson31", "team": "Team Alpha", "avg_points": 48.7, "dawg_rating": 9.2, "salary": 9800, 
         "stats": "3.5 blocks/game, 8.7 dunks/tournament", "previous_finish": "Runner-up (2024)"},
        {"id": 102, "name": "In3us", "team": "Team Alpha", "avg_points": 52.5, "dawg_rating": 9.5, "salary": 10200, 
         "stats": "42% shooting, 12.3 steals/tournament", "previous_finish": "Quarter-finals (2024)"},
        {"id": 103, "name": "bestballviper", "team": "Team Bravo", "avg_points": 51.8, "dawg_rating": 9.8, "salary": 10500, 
         "stats": "Most Defensive Player 2024", "previous_finish": "Champion (2024)"},
        {"id": 104, "name": "DFSKing99", "team": "Team Bravo", "avg_points": 47.2, "dawg_rating": 8.9, "salary": 9500, 
         "stats": "11.2 rebounds/game, 5.5 blocks/tournament", "previous_finish": "Semi-finals (2024)"},
        {"id": 105, "name": "NBAGuru42", "team": "Team Alpha", "avg_points": 44.3, "dawg_rating": 8.5, "salary": 8800, 
         "stats": "3-pt specialist, 45% from downtown", "previous_finish": "Quarter-finals (2024)"},
        {"id": 106, "name": "FantasyPro", "team": "Team Bravo", "avg_points": 46.9, "dawg_rating": 8.7, "salary": 9300, 
         "stats": "Most Valuable Dawg nominee 2024", "previous_finish": "Semi-finals (2024)"},
        {"id": 107, "name": "CelticsNation", "team": "Team Charlie", "avg_points": 42.1, "dawg_rating": 7.8, "salary": 8400, 
         "stats": "Fast break specialist, 7.3 assists/game", "previous_finish": "Round of 16 (2024)"},
        {"id": 108, "name": "LakeShow23", "team": "Team Charlie", "avg_points": 43.6, "dawg_rating": 8.2, "salary": 8900, 
         "stats": "Clutch performer, 89% FT shooting", "previous_finish": "Quarter-finals (2024)"},
        {"id": 109, "name": "HoopDreams", "team": "Team Delta", "avg_points": 38.4, "dawg_rating": 7.2, "salary": 7900, 
         "stats": "Rising star, first Dawg Bowl appearance", "previous_finish": "N/A (First appearance)"},
        {"id": 110, "name": "StatKing", "team": "Team Delta", "avg_points": 41.5, "dawg_rating": 7.6, "salary": 7600, 
         "stats": "Consistent scorer, 18.7 ppg", "previous_finish": "Round of 16 (2024)"},
        {"id": 111, "name": "DFSmaster", "team": "Team Echo", "avg_points": 45.7, "dawg_rating": 8.4, "salary": 9400, 
         "stats": "Double-double machine", "previous_finish": "Semi-finals (2024)"},
        {"id": 112, "name": "LineupLock", "team": "Team Echo", "avg_points": 44.3, "dawg_rating": 8.1, "salary": 9100, 
         "stats": "Defensive specialist, 2.3 steals/game", "previous_finish": "Quarter-finals (2024)"},
        {"id": 113, "name": "OptimalDFS", "team": "Team Foxtrot", "avg_points": 39.2, "dawg_rating": 7.4, "salary": 8600, 
         "stats": "Inside-outside threat", "previous_finish": "Round of 16 (2024)"},
        {"id": 114, "name": "PickSixer", "team": "Team Foxtrot", "avg_points": 35.8, "dawg_rating": 6.8, "salary": 7100, 
         "stats": "Sixth man specialist", "previous_finish": "Round of 32 (2024)"},
        {"id": 115, "name": "CapWiz", "team": "Team Golf", "avg_points": 38.3, "dawg_rating": 7.0, "salary": 7400, 
         "stats": "Hustle stats leader", "previous_finish": "Round of 32 (2024)"},
        {"id": 116, "name": "FadeThePublic", "team": "Team Golf", "avg_points": 42.7, "dawg_rating": 7.9, "salary": 8200, 
         "stats": "Momentum changer, crowd favorite", "previous_finish": "Round of 16 (2024)"},
        {"id": 117, "name": "SlateBreaker", "team": "Team Hotel", "avg_points": 46.8, "dawg_rating": 8.6, "salary": 9000, 
         "stats": "All-around player, triple-double threat", "previous_finish": "Quarter-finals (2024)"},
        {"id": 118, "name": "ValueHunter", "team": "Team Hotel", "avg_points": 40.5, "dawg_rating": 7.5, "salary": 8000, 
         "stats": "Efficient shooter, 52% FG", "previous_finish": "Round of 32 (2024)"},
    ]

def simulate_dawg_bowl_performance(selected_players, captain_id):
    # Simulate fantasy performance
    results = []
    total_points = 0
    
    # Generate random performance stats for each player
    for player in selected_players:
        # Base points correlated to dawg rating and average points
        base_points = player["avg_points"] * (0.8 + random.random() * 0.4)  # 80-120% of average
        
        # Generate random stats
        points = round(random.uniform(10, 30), 1)
        rebounds = round(random.uniform(3, 12), 1)
        assists = round(random.uniform(2, 8), 1)
        blocks = round(random.uniform(0, 4), 1)
        steals = round(random.uniform(0, 3), 1)
        
        # Calculate fantasy points
        fantasy_points = points + (rebounds * 1.2) + (assists * 1.5) + (blocks * 3) + (steals * 3)
        
        # Adjust based on dawg rating - higher dawg rating means more consistency
        consistency_factor = 0.9 + (player["dawg_rating"] / 100)
        adjusted_points = fantasy_points * consistency_factor
        
        # Apply captain multiplier
        multiplier = 1.5 if player["id"] == captain_id else 1.0
        final_points = adjusted_points * multiplier
        
        results.append({
            "id": player["id"],
            "name": player["name"],
            "team": player["team"],
            "dawg_rating": player["dawg_rating"],
            "points": points,
            "rebounds": rebounds,
            "assists": assists,
            "blocks": blocks,
            "steals": steals,
            "fantasy_points": adjusted_points,
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
        4. Earn points based on player performance in the Dawg Bowl
        5. Compete against friends for the highest score
        """)
        
        st.header("Settings")
        salary_cap = st.slider("Salary Cap", 40000, 60000, 50000, 1000)
        entry_fee = st.number_input("Entry Fee ($)", 1, 100, 20)
        
        st.header("About NBA Dawg Bowl")
        st.write("""
        The NBA Dawg Bowl is an intense competition showcasing the toughest, most competitive players in basketball. 
        
        These players bring energy, hustle, and a fierce competitive spirit to every play - the true definition of "dawgs" on the court.
        
        Draft wisely - dawg mentality matters!
        """)
    
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
        # Show contest banner
        st.header("NBA Dawg Bowl 2025")
        st.subheader("Draft your ultimate lineup of basketball dawgs!")
        
        # Show available players
        st.header("Available Dawg Bowl Competitors")
        all_players = get_dawg_bowl_contestants()
        
        # Filter and sort options
        col1, col2, col3 = st.columns(3)
        with col1:
            sort_by = st.selectbox("Sort By", ["Dawg Rating (High to Low)", "Salary (High to Low)", "Salary (Low to High)", 
                                              "Avg Points (High to Low)", "Team"])
        with col2:
            team_filter = st.selectbox("Filter by Team", ["All"] + list(set(p["team"] for p in all_players)))
        with col3:
            search = st.text_input("Search Player")
        
        # Apply filters and sorting
        filtered_players = all_players
        if team_filter != "All":
            filtered_players = [p for p in filtered_players if p["team"] == team_filter]
        
        if search:
            filtered_players = [p for p in filtered_players if search.lower() in p["name"].lower()]
        
        # Apply sorting
        if sort_by == "Dawg Rating (High to Low)":
            filtered_players.sort(key=lambda x: x["dawg_rating"], reverse=True)
        elif sort_by == "Salary (High to Low)":
            filtered_players.sort(key=lambda x: x["salary"], reverse=True)
        elif sort_by == "Salary (Low to High)":
            filtered_players.sort(key=lambda x: x["salary"])
        elif sort_by == "Avg Points (High to Low)":
            filtered_players.sort(key=lambda x: x["avg_points"], reverse=True)
        elif sort_by == "Team":
            filtered_players.sort(key=lambda x: x["team"])
        
        # Display players in a grid
        col1, col2 = st.columns(2)
        
        for i, player in enumerate(filtered_players):
            # Alternate between columns
            with col1 if i % 2 == 0 else col2:
                with st.container():
                    st.markdown(f"""
                    <div class="player-card">
                        <div class="player-name">{player["name"]}</div>
                        <div class="player-details">{player["team"]} | ${player["salary"]} | Dawg Rating: {player["dawg_rating"]}/10</div>
                        <div class="player-stats">Avg Fantasy Points: {player["avg_points"]}</div>
                        <div class="player-stats">Stats: {player["stats"]}</div>
                        <div class="player-stats">Previous: {player["previous_finish"]}</div>
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
        st.header("Your Dawg Bowl Lineup")
        
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
                        <div class="player-details">{position_label} | {player["team"]}</div>
                        <div class="player-stats">${player["salary"]}</div>
                        <div class="player-stats">Dawg Rating: {player["dawg_rating"]}/10</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Check if lineup is valid for submission
            if len(st.session_state.selected_players) == 6 and st.session_state.captain_id is not None and total_salary <= salary_cap:
                if st.button("Submit Lineup", type="primary"):
                    # Simulate contest results
                    results, total = simulate_dawg_bowl_performance(st.session_state.selected_players, st.session_state.captain_id)
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
        st.header("Dawg Bowl Performance Results")
        
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
            color="team",
            title="Fantasy Points by Player",
            labels={"name": "Player", "final_points": "Fantasy Points", "team": "Team"},
            text="final_points"
        )
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig, use_container_width=True)
        
        # Display detailed stats table
        st.subheader("Player Performance Details")
        
        performance_data = []
        for result in st.session_state.simulation_results:
            performance_data.append({
                "Player": f"{result['name']} {'(C)' if result['multiplier'] > 1 else ''}",
                "PTS": result["points"],
                "REB": result["rebounds"],
                "AST": result["assists"],
                "BLK": result["blocks"],
                "STL": result["steals"],
                "Base Points": round(result["fantasy_points"], 1),
                "Multiplier": result["multiplier"],
                "Total Points": round(result["final_points"], 1)
            })
        
        performance_df = pd.DataFrame(performance_data)
        st.table(performance_df)
        
        # Show detailed player performances
        st.subheader("Player Breakdown")
        
        col1, col2 = st.columns(2)
        
        # Captain highlight in first column
        captain = next((p for p in st.session_state.simulation_results if p["multiplier"] > 1), None)
        with col1:
            if captain:
                st.markdown("### Captain Performance")
                st.markdown(f"""
                <div class="player-card captain">
                    <div class="player-name">{captain['name']} (CAPTAIN)</div>
                    <div class="player-details">{captain['team']} | Dawg Rating: {captain['dawg_rating']}/10</div>
                    <div class="player-stats">
                        <b>Stats:</b> {captain['points']} PTS, {captain['rebounds']} REB, 
                        {captain['assists']} AST, {captain['blocks']} BLK, {captain['steals']} STL
                    </div>
                    <div class="player-stats">
                        <b>Fantasy Points:</b> {captain['fantasy_points']:.1f} × {captain['multiplier']} = {captain['final_points']:.1f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Team composition chart
        with col2:
            st.markdown("### Team Composition")
            team_data = {}
            for result in st.session_state.simulation_results:
                if result["team"] in team_data:
                    team_data[result["team"]] += 1
                else:
                    team_data[result["team"]] = 1
            
            fig = px.pie(
                names=list(team_data.keys()),
                values=list(team_data.values()),
                title="Players by Team"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Show dawg rating distribution
        st.subheader("Dawg Rating Distribution")
        dawg_ratings = [player["dawg_rating"] for player in st.session_state.simulation_results]
        
        fig = px.histogram(
            x=dawg_ratings,
            nbins=10,
            range_x=[5, 10],
            labels={"x": "Dawg Rating"},
            title="Distribution of Dawg Ratings in Your Lineup"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Mock leaderboard
        st.header("Global Leaderboard")
        
        # Generate random scores around the user's score
        user_score = st.session_state.total_points
        other_scores = [random.uniform(user_score * 0.8, user_score * 1.2) for _ in range(9)]
        other_scores.append(user_score)
        all_scores = sorted(other_scores, reverse=True)
        user_rank = all_scores.index(user_score) + 1
        
        leaderboard_data = {
            "Rank": list(range(1, 11)),
            "User": ["DawgMaster", "HustleKing", "CourtGeneral", "DefenseWizard", "FlexCapitol" 
                     "You" if i == user_rank - 1 else f"Player{i+1}" for i in range(10)],
            "Points": [round(score, 2) for score in all_scores],
            "Prize": ["$1,000", "$500", "$250", "$100", "$50", "$25", "$25", "$25", "$25", "$0"]
        }
        
        # Adjust the user's entry
        leaderboard_data["User"][user_rank - 1] = "You"
        
        leaderboard_df = pd.DataFrame(leaderboard_data)
        st.table(leaderboard_df)
        
        # Strategy recommendations
        st.header("Strategy Insights")
        
        # Calculate some insights
        avg_dawg_rating = sum(player["dawg_rating"] for player in st.session_state.simulation_results) / len(st.session_state.simulation_results)
        captain_dawg_rating = next((p["dawg_rating"] for p in st.session_state.simulation_results if p["multiplier"] > 1), 0)
        
        st.write(f"Your lineup's average Dawg Rating: {avg_dawg_rating:.1f}/10")
        st.write(f"Your captain's Dawg Rating: {captain_dawg_rating}/10")
        
        if captain_dawg_rating > 9:
            st.success("Great captain choice! High Dawg Rating players make excellent captains.")
        elif captain_dawg_rating < 8:
            st.warning("Consider selecting a captain with a higher Dawg Rating next time.")
        
        if avg_dawg_rating > 8.5:
            st.success("Your lineup has excellent overall Dawg mentality!")
        elif avg_dawg_rating < 7.5:
            st.warning("Try selecting players with higher Dawg Ratings to improve your score.")
        
        # Share or save button
        if st.button("Share Results"):
            st.success("Results shared! (This would connect to social media in a real app)")

if __name__ == "__main__":
    main()
