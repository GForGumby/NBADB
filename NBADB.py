import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

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
    .saved-lineup {
        margin-bottom: 20px;
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f5f5f5;
    }
    .admin-panel {
        margin-top: 30px;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# Player names and salaries for the NBA Dawg Bowl
def get_dawg_bowl_contestants():
    return [
        {"id": 101, "name": "spartan", "salary": 7500},
        {"id": 102, "name": "lofireball15", "salary": 6800},
        {"id": 103, "name": "jordanchand", "salary": 10000},
        {"id": 104, "name": "chezze", "salary": 7000},
        {"id": 105, "name": "fflinx", "salary": 8500},
        {"id": 106, "name": "lavalord", "salary": 9000},
        {"id": 107, "name": "welchman", "salary": 6800},
        {"id": 108, "name": "lolhotdogz", "salary": 8000},
        {"id": 109, "name": "thewood1105", "salary": 9500},
        {"id": 110, "name": "weather1981", "salary": 6200},
        {"id": 111, "name": "jtmckenzi", "salary": 11500},
        {"id": 112, "name": "in3us", "salary": 11200},
        {"id": 113, "name": "bestballviper", "salary": 9000},
        {"id": 114, "name": "awe419", "salary": 10000},
        {"id": 115, "name": "crblake2", "salary": 9200},
        {"id": 116, "name": "smerenda8", "salary": 9000},
        {"id": 117, "name": "generalblue", "salary": 6500},
        {"id": 118, "name": "bamntru", "salary": 6800},
        {"id": 119, "name": "patrickbarnesyoutube", "salary": 8000},
        {"id": 120, "name": "dallas102701", "salary": 7000},
        {"id": 121, "name": "babystevie", "salary": 9000},
        {"id": 122, "name": "samolson31", "salary": 12000},
    ]

# Functions to save and load lineups
def save_lineup(username, lineup, captain_id):
    """Save a user's lineup to a JSON file"""
    lineup_data = {
        "username": username,
        "entry_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lineup": lineup,
        "captain_id": captain_id
    }
    
    # Create lineups directory if it doesn't exist
    if not os.path.exists("lineups"):
        os.makedirs("lineups")
    
    # Save to a file named after the username
    filename = f"lineups/{username.lower().replace(' ', '_')}.json"
    
    with open(filename, "w") as f:
        json.dump(lineup_data, f)
    
    return True

def load_all_lineups():
    """Load all saved lineups"""
    lineups = []
    
    if not os.path.exists("lineups"):
        return lineups
    
    for filename in os.listdir("lineups"):
        if filename.endswith(".json"):
            with open(f"lineups/{filename}", "r") as f:
                try:
                    lineup_data = json.load(f)
                    lineups.append(lineup_data)
                except json.JSONDecodeError:
                    st.error(f"Error loading {filename}")
    
    return lineups

def export_lineups_to_csv():
    """Export all lineups to a CSV file for analysis"""
    lineups = load_all_lineups()
    
    if not lineups:
        return None
    
    # Create a list for CSV data
    csv_data = []
    
    for lineup in lineups:
        username = lineup["username"]
        captain_id = lineup["captain_id"]
        
        # Add each player in the lineup
        for player in lineup["lineup"]:
            role = "Captain" if player["id"] == captain_id else "Flex"
            csv_data.append({
                "Username": username,
                "Player": player["name"],
                "Role": role,
                "Salary": player["salary"],
                "Entry Time": lineup["entry_time"]
            })
    
    # Convert to DataFrame and save
    df = pd.DataFrame(csv_data)
    csv_filename = f"dawg_bowl_lineups_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(csv_filename, index=False)
    
    return csv_filename

# Main app
def main():
    st.title("🏀 NBA Dawg Bowl Fantasy Draft")
    
    # Sidebar for instructions and admin functions
    with st.sidebar:
        st.header("How It Works")
        st.write("""
        1. Enter your username
        2. Draft your lineup of NBA Dawg Bowl competitors
        3. Select 1 Captain (will score 1.5x points) and 5 Flex players
        4. Stay under the salary cap
        5. Submit your lineup
        
        After the contest concludes, the admin can enter the fantasy points for each player and see who wins!
        """)
        
        st.header("Settings")
        salary_cap = st.slider("Salary Cap", 40000, 60000, 50000, 1000)
        
        # Admin section in sidebar
        st.header("Admin Functions")
        admin_password = st.text_input("Admin Password", type="password")
        
        if admin_password == "admin123":  # Simple password for demo
            if st.button("View All Entries"):
                st.session_state.show_admin = True
            if st.button("Export All Entries to CSV"):
                csv_file = export_lineups_to_csv()
                if csv_file:
                    st.success(f"Exported to {csv_file}")
                else:
                    st.warning("No entries to export")
        
    # Initialize session state
    if 'selected_players' not in st.session_state:
        st.session_state.selected_players = []
    if 'captain_id' not in st.session_state:
        st.session_state.captain_id = None
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'show_admin' not in st.session_state:
        st.session_state.show_admin = False
    
    # Admin panel (when activated)
    if st.session_state.show_admin:
        st.header("Admin Panel - All Entries")
        
        lineups = load_all_lineups()
        
        if not lineups:
            st.warning("No entries found")
        else:
            for lineup in lineups:
                with st.expander(f"{lineup['username']} - Entered at {lineup['entry_time']}"):
                    st.write("**Captain:** " + next((player["name"] for player in lineup["lineup"] if player["id"] == lineup["captain_id"]), "Unknown"))
                    
                    # Show all players
                    player_list = []
                    for player in lineup["lineup"]:
                        role = "Captain" if player["id"] == lineup["captain_id"] else "Flex"
                        player_list.append({
                            "Player": player["name"],
                            "Role": role,
                            "Salary": f"${player['salary']}"
                        })
                    
                    st.table(pd.DataFrame(player_list))
        
        if st.button("Back to Draft"):
            st.session_state.show_admin = False
            st.experimental_rerun()
            
        # Stop here if admin panel is shown
        return
        
    # Main Draft Screen
    if not st.session_state.submitted:
        # Get username
        username = st.text_input("Enter Your Username")
        
        if not username:
            st.warning("Please enter your username to continue")
            return
        
        # Show available players
        st.header("Available Competitors")
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
            filtered_players.sort(key=lambda x: x["name"].lower())
        
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
                    if save_lineup(username, st.session_state.selected_players, st.session_state.captain_id):
                        st.session_state.submitted = True
                        st.experimental_rerun()
                    else:
                        st.error("Error saving lineup. Please try again.")
            else:
                if len(st.session_state.selected_players) < 6:
                    st.warning(f"Please select {6 - len(st.session_state.selected_players)} more players")
                elif st.session_state.captain_id is None:
                    st.warning("Please select a captain")
                elif total_salary > salary_cap:
                    st.error(f"Lineup exceeds salary cap by ${total_salary - salary_cap:,}")
    
    else:
        # Show submission confirmation
        st.success("Your lineup has been submitted successfully!")
        
        st.write("### Your Lineup")
        
        # Show the lineup that was submitted
        for player in st.session_state.selected_players:
            is_captain = player["id"] == st.session_state.captain_id
            role = "CAPTAIN" if is_captain else "FLEX"
            
            st.markdown(f"""
            <div class="player-card {'captain' if is_captain else ''}">
                <div class="player-name">{player["name"]}</div>
                <div class="player-details">{role} | ${player["salary"]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Create Another Lineup"):
            st.session_state.selected_players = []
            st.session_state.captain_id = None
            st.session_state.submitted = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
