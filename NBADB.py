import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Fantasy Players Contest",
    page_icon="🏆",
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

# Mock data functions
def get_available_contests():
    return [
        {
            "id": 1,
            "name": "NBA DFS $10K Showdown",
            "entry_fee": 20,
            "prize_pool": 10000,
            "max_entries": 100,
            "current_entries": 87,
            "start_time": "Today at 7:30 PM ET",
            "teams": ["Lakers vs Celtics"]
        },
        {
            "id": 2,
            "name": "NBA $5K Winner Takes All",
            "entry_fee": 50,
            "prize_pool": 5000,
            "max_entries": 50,
            "current_entries": 32,
            "start_time": "Today at 8:00 PM ET",
            "teams": ["Warriors vs Nets"]
        },
        {
            "id": 3,
            "name": "NBA $2K 50/50",
            "entry_fee": 10,
            "prize_pool": 2000,
            "max_entries": 200,
            "current_entries": 156,
            "start_time": "Today at 9:00 PM ET",
            "teams": ["Heat vs Mavericks"]
        }
    ]

def get_fantasy_players(contest_id):
    # Mock fantasy player data (usernames) with historical performance and cost
    players = []
    
    if contest_id == 1:
        players = [
            {"id": 101, "username": "SamOlson31", "avg_finish": 12.3, "avg_points": 348.7, "contest_history": "1st, 5th, 12th, 8th, 35th", "salary": 9800, "team": "Team A"},
            {"id": 102, "username": "In3us", "avg_finish": 7.8, "avg_points": 362.5, "contest_history": "2nd, 4th, 9th, 16th", "salary": 10200, "team": "Team A"},
            {"id": 103, "username": "bestballviper", "avg_finish": 5.2, "avg_points": 371.8, "contest_history": "1st, 3rd, 7th, 10th", "salary": 10500, "team": "Team B"},
            {"id": 104, "username": "DFSKing99", "avg_finish": 8.9, "avg_points": 357.2, "contest_history": "2nd, 6th, 8th, 19th", "salary": 9500, "team": "Team B"},
            {"id": 105, "username": "NBAGuru42", "avg_finish": 15.7, "avg_points": 341.3, "contest_history": "5th, 11th, 18th, 29th", "salary": 8800, "team": "Team A"},
            {"id": 106, "username": "FantasyPro", "avg_finish": 10.1, "avg_points": 352.9, "contest_history": "3rd, 7th, 13th, 17th", "salary": 9300, "team": "Team B"},
            {"id": 107, "username": "CelticsNation", "avg_finish": 18.3, "avg_points": 335.1, "contest_history": "8th, 15th, 22nd, 28th", "salary": 8400, "team": "Team A"},
            {"id": 108, "username": "LakeShow23", "avg_finish": 14.2, "avg_points": 343.6, "contest_history": "6th, 12th, 15th, 24th", "salary": 8900, "team": "Team B"},
            {"id": 109, "username": "HoopDreams", "avg_finish": 22.7, "avg_points": 328.4, "contest_history": "11th, 19th, 26th, 35th", "salary": 7900, "team": "Team A"},
            {"id": 110, "username": "StatKing", "avg_finish": 25.1, "avg_points": 321.5, "contest_history": "14th, 21st, 27th, 38th", "salary": 7600, "team": "Team B"},
            {"id": 111, "username": "DFSmaster", "avg_finish": 9.5, "avg_points": 355.7, "contest_history": "3rd, 8th, 10th, 17th", "salary": 9400, "team": "Team A"},
            {"id": 112, "username": "LineupLock", "avg_finish": 11.8, "avg_points": 350.3, "contest_history": "4th, 9th, 12th, 22nd", "salary": 9100, "team": "Team B"},
            {"id": 113, "username": "OptimalDFS", "avg_finish": 16.4, "avg_points": 339.2, "contest_history": "7th, 13th, 19th, 26th", "salary": 8600, "team": "Team A"},
            {"id": 114, "username": "PickSixer", "avg_finish": 30.2, "avg_points": 312.8, "contest_history": "18th, 25th, 33rd, 45th", "salary": 7100, "team": "Team B"},
            {"id": 115, "username": "CapWiz", "avg_finish": 27.8, "avg_points": 318.3, "contest_history": "16th, 24th, 31st, 40th", "salary": 7400, "team": "Team A"},
            {"id": 116, "username": "FadeThePublic", "avg_finish": 19.6, "avg_points": 332.7, "contest_history": "9th, 17th, 23rd, 29th", "salary": 8200, "team": "Team B"},
            {"id": 117, "username": "SlateBreaker", "avg_finish": 13.1, "avg_points": 346.8, "contest_history": "5th, 10th, 14th, 23rd", "salary": 9000, "team": "Team A"},
            {"id": 118, "username": "ValueHunter", "avg_finish": 21.3, "avg_points": 330.5, "contest_history": "10th, 18th, 25th, 32nd", "salary": 8000, "team": "Team B"},
        ]
    # Add more contests here with their fantasy players...
    elif contest_id == 2:
        players = [
            {"id": 201, "username": "WarriorsFan30", "avg_finish": 6.7, "avg_points": 365.2, "contest_history": "1st, 4th, 8th, 13th", "salary": 9900, "team": "Team C"},
            {"id": 202, "username": "NetsDynasty", "avg_finish": 9.3, "avg_points": 356.1, "contest_history": "3rd, 5th, 11th, 18th", "salary": 9400, "team": "Team D"},
            # Add more players for this contest...
        ]
    
    return players

def simulate_contest_results(selected_players, captain_id):
    # Simulate fantasy performance
    results = []
    total_points = 0
    
    # Generate contest finishing positions for all selected players
    contest_finish_positions = []
    for player in selected_players:
        # Generate random finish position around their average
        avg_finish = player["avg_finish"]
        # More variance for lower-ranked players
        variance = max(5, avg_finish * 0.4)
        finish = max(1, int(random.gauss(avg_finish, variance)))
        
        # Calculate fantasy points based on finish position
        # 1st: 100 pts, 2nd: 90 pts, 3rd: 85 pts, then decrease by smaller amounts
        if finish == 1:
            fantasy_points = 100
        elif finish == 2:
            fantasy_points = 90
        elif finish == 3:
            fantasy_points = 85
        elif finish <= 5:
            fantasy_points = 80 - ((finish - 3) * 5)
        elif finish <= 10:
            fantasy_points = 70 - ((finish - 5) * 3)
        elif finish <= 20:
            fantasy_points = 55 - ((finish - 10) * 2)
        elif finish <= 50:
            fantasy_points = 35 - ((finish - 20) * 0.5)
        else:
            fantasy_points = max(10, 20 - ((finish - 50) * 0.2))
        
        # Apply captain multiplier
        multiplier = 1.5 if player["id"] == captain_id else 1.0
        final_points = fantasy_points * multiplier
        
        results.append({
            "id": player["id"],
            "username": player["username"],
            "team": player["team"],
            "finish_position": finish,
            "fantasy_points": fantasy_points,
            "multiplier": multiplier,
            "final_points": final_points
        })
        
        total_points += final_points
    
    # Sort by finish position for display
    results.sort(key=lambda x: x["finish_position"])
    
    return results, total_points

# Main app
def main():
    st.title("🏆 Fantasy Players Contest")
    
    # Sidebar for instructions and settings
    with st.sidebar:
        st.header("How It Works")
        st.write("""
        1. Select a contest to enter
        2. Draft your lineup of fantasy players (other DFS users)
        3. Select 1 Captain (scores 1.5x points) and 5 Flex players
        4. Stay under the salary cap
        5. Earn points based on how your drafted players finish in the contest
        """)
        
        st.header("Settings")
        salary_cap = st.slider("Salary Cap", 40000, 60000, 50000, 1000)
        entry_fee = st.number_input("Entry Fee ($)", 1, 100, 20)
        
        st.header("My Entries")
        st.write("You have 0 active entries")
        
        if st.button("View Past Results"):
            st.write("No past results found")
    
    # Initialize session state
    if 'selected_contest' not in st.session_state:
        st.session_state.selected_contest = None
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
    if not st.session_state.selected_contest and not st.session_state.simulated:
        st.header("Available Contests")
        
        contests = get_available_contests()
        for contest in contests:
            with st.container():
                st.markdown(f"""
                <div class="contest-card">
                    <div class="contest-title">{contest['name']}</div>
                    <div class="contest-details">
                        Entry Fee: ${contest['entry_fee']} | Prize Pool: ${contest['prize_pool']:,} | 
                        Entries: {contest['current_entries']}/{contest['max_entries']} | {contest['start_time']}
                    </div>
                    <div class="contest-details">
                        Teams: {', '.join(contest['teams'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Enter Contest", key=f"enter_{contest['id']}"):
                    st.session_state.selected_contest = contest["id"]
                    st.experimental_rerun()
    
    elif not st.session_state.simulated:
        # Contest selected, show player selection
        contest_id = st.session_state.selected_contest
        contests = get_available_contests()
        selected_contest = next((c for c in contests if c["id"] == contest_id), None)
        
        if selected_contest:
            st.header(f"Enter: {selected_contest['name']}")
            st.subheader(f"Prize Pool: ${selected_contest['prize_pool']:,} | Entry Fee: ${selected_contest['entry_fee']}")
            
            # Back button
            if st.button("← Back to Contests"):
                st.session_state.selected_contest = None
                st.experimental_rerun()
            
            # Show available fantasy players
            st.header("Available Fantasy Players")
            fantasy_players = get_fantasy_players(contest_id)
            
            # Filter and sort options
            col1, col2, col3 = st.columns(3)
            with col1:
                sort_by = st.selectbox("Sort By", ["Salary (High to Low)", "Salary (Low to High)", 
                                                  "Avg Finish (Best)", "Avg Finish (Worst)",
                                                  "Avg Points (High to Low)", "Avg Points (Low to High)"])
            with col2:
                team_filter = st.selectbox("Filter by Team", ["All"] + list(set(p["team"] for p in fantasy_players)))
            with col3:
                search = st.text_input("Search Username")
            
            # Apply filters and sorting
            filtered_players = fantasy_players
            if team_filter != "All":
                filtered_players = [p for p in filtered_players if p["team"] == team_filter]
            
            if search:
                filtered_players = [p for p in filtered_players if search.lower() in p["username"].lower()]
            
            # Apply sorting
            if sort_by == "Salary (High to Low)":
                filtered_players.sort(key=lambda x: x["salary"], reverse=True)
            elif sort_by == "Salary (Low to High)":
                filtered_players.sort(key=lambda x: x["salary"])
            elif sort_by == "Avg Finish (Best)":
                filtered_players.sort(key=lambda x: x["avg_finish"])
            elif sort_by == "Avg Finish (Worst)":
                filtered_players.sort(key=lambda x: x["avg_finish"], reverse=True)
            elif sort_by == "Avg Points (High to Low)":
                filtered_players.sort(key=lambda x: x["avg_points"], reverse=True)
            elif sort_by == "Avg Points (Low to High)":
                filtered_players.sort(key=lambda x: x["avg_points"])
            
            # Display players in a grid
            col1, col2 = st.columns(2)
            
            for i, player in enumerate(filtered_players):
                # Alternate between columns
                with col1 if i % 2 == 0 else col2:
                    with st.container():
                        st.markdown(f"""
                        <div class="player-card">
                            <div class="player-name">{player["username"]}</div>
                            <div class="player-details">{player["team"]} | ${player["salary"]}</div>
                            <div class="player-stats">Avg Finish: {player["avg_finish"]} | Avg Points: {player["avg_points"]}</div>
                            <div class="player-stats">History: {player["contest_history"]}</div>
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
                            <div class="player-name">{player["username"]}</div>
                            <div class="player-details">{position_label} | {player["team"]}</div>
                            <div class="player-stats">${player["salary"]}</div>
                            <div class="player-stats">Avg Finish: {player["avg_finish"]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Check if lineup is valid for submission
                if len(st.session_state.selected_players) == 6 and st.session_state.captain_id is not None and total_salary <= salary_cap:
                    if st.button("Submit Lineup", type="primary"):
                        # Simulate contest results
                        results, total = simulate_contest_results(st.session_state.selected_players, st.session_state.captain_id)
                        st.session_state.simulation_results = results
                        st.session_state.total_points = total
                        st.session_state.simulated = True
                        st.experimental_rerun()
                else:
                    if len(st.session_state.selected_players) < 6:
                        st.warning(f"Please select {6 - len(st.session_state.selected_players)} more fantasy players")
                    elif st.session_state.captain_id is None:
                        st.warning("Please select a captain")
                    elif total_salary > salary_cap:
                        st.error(f"Lineup exceeds salary cap by ${total_salary - salary_cap:,}")
    
    else:
        # Show simulation results
        st.header("Contest Results")
        
        # Add a back button
        if st.button("Create New Entry"):
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
            x="username",
            y="final_points",
            color="team",
            title="Fantasy Points by Player",
            labels={"username": "Fantasy Player", "final_points": "Fantasy Points", "team": "Team"},
            text="final_points"
        )
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig, use_container_width=True)
        
        # Create a table showing player finish positions
        st.subheader("Player Finish Positions")
        
        for result in st.session_state.simulation_results:
            if result["multiplier"] > 1:
                captain_label = " (CAPTAIN)"
            else:
                captain_label = ""
                
            st.markdown(f"""
            <div class="player-card {'captain' if result['multiplier'] > 1 else ''}">
                <div class="player-name">{result['username']}{captain_label}</div>
                <div class="player-details">{result['team']}</div>
                <div class="player-stats">
                    <b>Finish Position:</b> {result['finish_position']}{get_position_suffix(result['finish_position'])} place
                </div>
                <div class="player-stats">
                    <b>Fantasy Points:</b> {result['fantasy_points']:.1f} × {result['multiplier']} = {result['final_points']:.1f}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show payout structure
        st.header("Contest Payout Structure")
        contest_id = st.session_state.selected_contest
        contests = get_available_contests()
        selected_contest = next((c for c in contests if c["id"] == contest_id), None)
        
        if selected_contest:
            prize_pool = selected_contest["prize_pool"]
            
            payout_data = {
                "Position": ["1st", "2nd", "3rd", "4th", "5th", "6-10th", "11-20th"],
                "Payout": [
                    f"${int(prize_pool * 0.25):,}",
                    f"${int(prize_pool * 0.15):,}",
                    f"${int(prize_pool * 0.10):,}",
                    f"${int(prize_pool * 0.07):,}",
                    f"${int(prize_pool * 0.05):,}",
                    f"${int(prize_pool * 0.03):,} each",
                    f"${int(prize_pool * 0.01):,} each"
                ]
            }
            
            payout_df = pd.DataFrame(payout_data)
            st.table(payout_df)
        
        # Mock user leaderboard
        st.header("Your Contest Results")
        user_score = random.uniform(300, 400)  # Random score for the user
        
        leaderboard_data = {
            "Rank": [1, 2, 3, "...", 15, "...", 42],
            "User": ["FantasyPro99", "DFSChamp", "NBA_Lineup_God", "...", "You", "...", "LastPlace"],
            "Points": [389.5, 372.3, 366.8, "...", user_score, "...", 212.4],
            "Winnings": [f"${int(prize_pool * 0.25):,}", f"${int(prize_pool * 0.15):,}", f"${int(prize_pool * 0.10):,}", "...", "$0", "...", "$0"]
        }
        
        leaderboard_df = pd.DataFrame(leaderboard_data)
        st.table(leaderboard_df)
        
        # Recommendations for next contest
        st.header("Recommendations for Next Contest")
        st.write("Based on today's results, consider these changes for your next entry:")
        
        recommendations = [
            "Choose players with more consistent top-10 finishes",
            "Diversify your lineup with players from different teams",
            "Consider lower-salary players who are trending upward",
            "Pick a captain who specializes in the specific game format being played"
        ]
        
        for rec in recommendations:
            st.markdown(f"- {rec}")

def get_position_suffix(position):
    if position % 10 == 1 and position != 11:
        return "st"
    elif position % 10 == 2 and position != 12:
        return "nd"
    elif position % 10 == 3 and position != 13:
        return "rd"
    else:
        return "th"

if __name__ == "__main__":
    main()
