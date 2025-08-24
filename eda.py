import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="FIFA WC 2022 EDA", layout="wide")

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<h1 style='text-align: center;'>FIFA World Cup 2022: Argentina Victory</h1>", unsafe_allow_html=True)

banner = Image.open("banner.jpg")
# st.image(banner, use_container_width=True)
st.image(banner, width=800)

st.markdown("The FIFA World Cup 2022 was the 22nd edition of the tournament. In this edition, 32 teams participated. For the first time in FIFA World Cup history, the tournament was hosted by a Middle Eastern country, Qatar. All 64 matches were played across 8 venues in 5 cities. This tournament was marked by several notable events and surprises. For the first time, a Middle Eastern team, Morocco, reached the semi-finals. Additionally, Saudi Arabia defeated Argentina, which had won the World Cup twice before, and ultimately won the tournament. There are many aspects of this tournament that we will explore and analyze in the Exploratory Data Analysis."
)



# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    group_data = pd.read_csv("group_stats.csv")
    team_data = pd.read_csv("team_data.csv")
    group_data = group_data.drop("Unnamed: 0", axis=1)
    new_value_group = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H'}
    group_data['group'] = group_data['group'].replace(new_value_group)
    return group_data, team_data

group_data, team_data = load_data()

# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Group Data Analysis", "Team Data Analysis"])

# -------------------------------
# GROUP DATA ANALYSIS
# -------------------------------
if page == "Group Data Analysis":

    st.markdown("""
### In this Exploratory Data Analysis, we will find the following from Group Data:

- **Team with Most Wins:** Identify the team that won the most matches.  
- **Team with Most Goals Scored:** Find out which team scored the highest number of goals.  
- **Team with No Wins:** Determine which team failed to win a single match.  
- **Team with Most Goals Conceded:** Identify which team allowed the most goals against them.  
- **Team with Highest Goal Difference:** Calculate which team has the highest goal difference (goals scored minus goals conceded).  
- **Highest Points in Group Stage:** Find out which team accumulated the most points in the group stage.  
- **Teams Qualifying for Round of 16:** Determine which teams advanced to the Round of 16 based on their group performance.  
""")
    
    st.header("📊 Group Stage Analysis")
    st.dataframe(group_data.head())

    st.write("In the group stage of the FIFA World Cup 2022, each team played 3 matches. What’s interesting is that no team was able to win all 3 matches, showing how close and tough the competition was.")

    # Most Wins
    team_won = group_data[group_data['wins']== 2]['team']
    st.subheader("Teams with Most Wins (2 wins)")
    # st.write(", ".join(team_won))
    for team in team_won:
        st.write(f"- {team}")

    # Most Goals
    most_goals = group_data['goals_scored'].max()
    most_goals_team = group_data[group_data['goals_scored'] == most_goals]['team']
    st.subheader("Team(s) with Most Goals Scored")
    
    for team in most_goals_team:
        st.write(f"- {team} → {most_goals} goals")

    

    # Teams with no wins
    not_won = group_data[group_data['wins'] == 0]['team']
    st.subheader("Teams with No Wins")

    for team in not_won:
        st.write(f"- {team}")

    # Goals Conceded
    goal_against = group_data['goals_against'].max()
    conceded = group_data[group_data['goals_against']==goal_against][['team','goals_against']]
    st.subheader("Most Goals Conceded")
    for _, row in conceded.iterrows():
        st.write(f"- {row['team']} → {row['goals_against']} goals")

    # Highest Points
    highest_points = group_data['points'].max()
    high_pts_teams = group_data[group_data['points']==highest_points]['team']
    st.subheader("Highest Points in Group Stage")
    for team in high_pts_teams:
        st.write(f"- {team} → {highest_points} points")

    # Qualified Teams
    st.subheader("Teams Qualified for Round of 16")

    qualified = (
        group_data.sort_values(by=['group', 'points'], ascending=[True, False])
        .groupby('group')
        .head(2)[['group', 'team', 'points']]
    )

    for _, row in qualified.iterrows():
        st.write(f"- Group {row['group']}: {row['team']} → {row['points']} points")


    st.subheader("We observed another setback as Germany, a four-time FIFA World Cup champion, failed to advance beyond the group stage.")
# -------------------------------
# TEAM DATA ANALYSIS
# -------------------------------
if page == "Team Data Analysis":

    st.markdown("""
### In the team data, we will analyze the following:

1. **Number of players used** during the tournament.
2. **Average age of players** in each team to understand team experience.
3. **Possession percentage** to see which teams controlled the game more.
4. **Games played vs goals scored** to assess attacking performance.
5. **Yellow cards received** to understand disciplinary behavior.
6. **Red cards received** for serious fouls or misconduct.
7. **Goals scored vs goals conceded** to analyze overall goal performance.
8. **Shots on target** to measure offensive efficiency.
9. **Games won, lost, and drawn** by each team.
10. **Clean sheets** to understand defensive strength and consistency.
11. **Completed passes** to measure passing accuracy and control.
12. **Corner kicks won** by each team for attacking opportunities.
13. **Points per game** to evaluate overall performance across matches.
14. **Offsides committed** to understand timing and positioning in attacks.
15. **Penalties won** by each team during the tournament.
16. **Penalties conceded** to understand defensive discipline.
17. **Own goals scored** to highlight defensive errors.
18. **Aerial duels won** to measure dominance in the air.
19. **Aerial duels lost** to understand weaknesses in aerial challenges.
20. **Expected goals (xG) vs actual goals** to assess finishing quality and efficiency.
""")
    
    st.header("⚽ Team Analysis")
    st.dataframe(team_data.head())

    # Plotly bar chart
    fig = px.bar(
        team_data.sort_values('players_used', ascending=True),
        y='team',
        x='players_used',
        width=900,
        height=800
    )

    # Color setup
    colors = ['green'] * len(team_data)
    colors[29] = 'blue'
    fig.update_traces(marker_color=colors)

    # Layout
    fig.update_layout(
        title='NUMBER OF PLAYERS USED BY THE TEAMS',
        title_x=0.5,
        xaxis_title='PLAYERS USED',
        yaxis_title='TEAM'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write("A total of 680 players participated in the tournament. The average number of players used by each team is 21. The minimum number of players used by Wales and Ecuador is 18, while Brazil used a maximum of 26 players.")


    

    # Average Age
    fig = px.bar(team_data.sort_values('avg_age', ascending=True), y= 'team', x= 'avg_age', width = 900,
    height = 800)

    fig.update_layout(
        title = 'AVERAGE AGE OF TEAM',
        title_x = 0.5,
        xaxis_title = 'AVERAGE AGE',
        yaxis_title = 'TEAM'
    )

    colors = ['green'] * len(team_data)

    colors[18] = 'blue';



    fig.update_traces(marker_color = colors )



    st.plotly_chart(fig, use_container_width=True)


    # Possession
    fig = px.bar(team_data.sort_values('possession', ascending=True), y= 'team', x= 'possession', width = 900,
    height = 800)

    fig.update_layout(
        title = 'POSSESSION OF TEAMS',
        title_x = 0.5,
        xaxis_title = 'POSSESSION',
        yaxis_title = 'TEAM'
    )

    colors = ['green'] * len(team_data)

    colors[26] = 'blue';



    fig.update_traces(marker_color = colors )

    st.plotly_chart(fig, use_container_width=True)

    st.write("Spain has the highest possession at 75.8%, while Costa Rica has the lowest at 31.3%")

    # Games vs Goals
    fig = px.bar(team_data, x = 'team', y=['games', 'goals'], barmode='group', color_discrete_map={'goals': 'green', 'games': 'red'})

    fig.update_layout(
        template = 'plotly_dark',
        title = 'COMPARISION OF GAMES PLAYED AND GOALS SCORED',
        title_x = 0.5, 
        xaxis_title = 'TEAM',
        yaxis_title = 'GAMES / GOALS',
        bargap = 0.1
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Following are the teams who scored the highest goals throughout the tournament:**
1. France : 16  
2. Argentina : 15  
3. England : 13  
4. Portugal : 12  
5. Netherlands : 10  
""")

    # Yellow Cards
    fig = px.bar(team_data.sort_values('cards_yellow'), y='team', x='cards_yellow',
                 title="Yellow Cards by Teams", orientation='h', height=700)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("England and Spain showed great discipline and sportsmanship throughout the tournament, receiving the fewest yellow cards. Along with that, they were also the top scorers in the group stage, each netting 9 goals — a perfect mix of fair play and strong performance.")

    # Goals vs Conceded
    fig = px.bar(team_data, x = 'team', y=['goals', 'gk_goals_against'], barmode='group', color_discrete_map={'gk_goals_against': 'red', 'goals': 'blue'})

    fig.update_layout(
        template = 'plotly_dark',
        title = 'COMPARISION OF GOALS SCORED AND GOALS CONCEALED',
        title_x = 0.5, 
        xaxis_title = 'TEAM',
        yaxis_title = 'GAMES / GOALS CONCEALED',
        bargap = 0.1
    )
    st.plotly_chart(fig, use_container_width=True)

    # import plotly.graph_objects as go 

#     max_xg = team_data['xg'].max()
#     team_data['x_pos'] = team_data['xg'] / max_xg * 100
#     team_data['y_pos'] = np.linspace(20, 80, len(team_data)) 

#     fig = go.Figure()

#     fig.add_trace(go.Scatter(
#         x=team_data['x_pos'],
#         y=team_data['y_pos'],
#         mode='markers+text',
#         marker=dict(
#             size=25,
#             color=team_data['xg'],
#             colorscale='Viridis',
#             line=dict(color='black', width=1)
#         ),
#         text=team_data['team'],
#         textposition='bottom center',
#         textfont=dict(size=12, color='black'),
#         hovertemplate='<b>%{text}</b><br>xG: %{marker.color:.2f}<extra></extra>'
#     ))

#     fig.add_shape(type='rect', x0=0, y0=0, x1=100, y1=100, line=dict(color='green', width=3))
#     fig.add_shape(type='line', x0=50, y0=0, x1=50, y1=100, line=dict(color='green', width=2)) 

#     fig.add_shape(type='line', x0=100, y0=40, x1=100, y1=60, line=dict(color='red', width=4))  
#     fig.add_shape(type='line', x0=0, y0=40, x1=0, y1=60, line=dict(color='gray', width=2))      

#     fig.update_layout(
#         title='Team Positions Based on Expected Goals (xG)',
#         xaxis=dict(title='Pitch Length', range=[-5, 105], showgrid=False, visible=False),
#         yaxis=dict(title='Pitch Width', range=[0, 100], showgrid=False, visible=False),
#         plot_bgcolor='white',
#         width=900,
#         height=500,
#         showlegend=False,
#         margin=dict(l=20, r=20, t=60, b=20)
# )   

    # Clean Sheets
    fig = px.line(team_data.sort_values('gk_clean_sheets', ascending=False), x='team', y='gk_clean_sheets', width = 1000,
    height = 600)

    fig.update_layout(
        title = 'Teams Concealed 0 Goals In Matches',
        title_x = 0.5,
        xaxis_title = 'TEAM',
        yaxis_title = 'Clean Sheet'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Morocco remained only team in the tournament having highest 4 clean sheets while playing 7 matches. Argentina and England concealed no goals in 3 matches.")

    # Passes Completed
    top_passes = team_data[['team','passes_completed']].sort_values('passes_completed',ascending=False).head(5).reset_index(drop=True)
    st.subheader("Top 5 Teams with Most Passes Completed")
    # st.table(top_passes)
    st.table(top_passes.set_index("team"))

    st.markdown("A high number of passes often shows how strong a team is — it helps build better attacks and keeps control in defense. Teams like Argentina, Croatia, Spain, France, and England completed the most passes in the tournament. All of them made it to the Round of 16 and performed really well, proving that good passing is a key part of a strong and successful team.")

    # Corner Kicks
    top_corners = team_data[['team','corner_kicks']].sort_values('corner_kicks',ascending=False).head(5)
    st.subheader("Top 5 Teams with Most Corner Kicks")
    st.table(top_corners.set_index("team"))

    # Points per Game
    points_per_game = team_data[['team', 'points_per_game']].sort_values(by="points_per_game", ascending=False).head(10)
    points_per_game_sort = points_per_game.sort_values(by='points_per_game', ascending=True)

    fig = px.bar(points_per_game_sort, x='points_per_game', y='team', orientation='h',
                title='Top 5 Teams by Points per Game' , color='points_per_game')

    st.plotly_chart(fig, use_container_width=True)


    fig = px.bar(team_data.sort_values('gk_wins', ascending=False), x='team', y=['gk_wins', 'gk_ties', 'gk_losses'], width = 1000,
    height = 600)

    fig.update_layout(
        title = 'Wins / Ties / Losses',
        title_x = 0.5,
        xaxis_title = 'TEAM',
        yaxis_title = 'Result'
    )

    colors = {'gk_wins': 'green', 'gk_ties': 'blue', 'gk_losses':'red'}


    for trace, column in zip(fig.data, ['gk_wins', 'gk_ties', 'gk_losses']):
        trace.marker.color = colors[column]

    st.plotly_chart(fig, use_container_width=True)

    # Offsides
    offsides = team_data[['team', 'offsides']].sort_values(by='offsides', ascending=False);


    fig = px.scatter(offsides, x = 'team', y = 'offsides', size='offsides', title="Offsides by team", color="team");
    st.plotly_chart(fig, use_container_width=True)


    pen_won = team_data[['team', 'pens_won']]
    pen_won_filtered = pen_won[pen_won['pens_won'] > 0].sort_values(by="pens_won", ascending=False).reset_index(drop=True)

    # Streamlit section
    st.subheader("Penalties Won by Teams")

    # Show as table

# Show as ranked list
    for index, row in pen_won_filtered.iterrows():
        st.write(f"{index + 1}) {row['team']} = {row['pens_won']}")

    own_goals = team_data[['team', 'own_goals']].sort_values(by="own_goals", ascending=False)
    own_goals = own_goals[own_goals['own_goals'] > 0].reset_index(drop=True)


    pen_conc = team_data[['team', 'pens_conceded']].sort_values(by="pens_conceded", ascending=False)
    pen_conc = pen_conc[pen_conc['pens_conceded'] > 0].reset_index(drop=True)

    st.write("Throughout the tournament, Argentina scored a total of 15 goals, 5 of which came from penalties. This means Argentina scored only 10 goals from open play.")

    # Streamlit section
    st.subheader("Penalties Conceded by Teams")



    # Also display as a ranked list
    for index, row in pen_conc.iterrows():
        st.write(f"{index + 1}) {row['team']} = {row['pens_conceded']}")

    st.write("Across the tournament, France conceded 8 goal` in total — with 4 of them being scored from penalties.")   

    # Streamlit title
    st.subheader("Own Goals by Teams")

    # Or show as a ranked list
    for index, row in own_goals.iterrows():
        st.write(f"{index + 1}) {row['team']} = {row['own_goals']}")

    st.write("Interestingly, Argentina and Morocco were the sole teams to record own goals in the entire tournament.")

    # Aerial Duels Won
    fig = px.bar(team_data.sort_values(by='aerials_won', ascending=True), x='aerials_won', y='team', height=800, width=900, title='Aerials Won by the Teams')

    fig.add_vline(
        x=80,
        line_dash="dot",     
        line_color="red",
        line_width=3
    )

    colors = ["green"] * len(team_data)

    colors[29] = 'red';
    colors[31] = 'blue';

    fig.update_traces(marker_color = colors)
    st.plotly_chart(fig, use_container_width=True)

    st.write("France, Croatia, and Argentina won the most aerial duels in the tournament. This shows the physical strength of their players and how they dominated the field, especially in high-pressure situations.");

    # Aerial Duels Lost
    sorted_data = team_data.sort_values(by='aerials_lost', ascending=True)

    colors = ["green"] * len(sorted_data)
    colors[31] = "blue"

    fig = go.Figure()

    # Add sticks
    fig.add_trace(go.Scatter(
        x=sorted_data['team'],
        y=sorted_data['aerials_lost'],
        mode='lines+markers',
        line=dict(color='gray', width=1),
        marker=dict(color=colors, size=12),
        hovertext=sorted_data['team'],
        hoverinfo='text+y',
        showlegend=False
    ))

    # Add reference line
    fig.add_hline(y=80, line_dash="dot", line_color="red", line_width=3)

    fig.update_layout(
        title="Aerial Lost by Teams",
        xaxis_title="Team",
        yaxis_title="Aerials Lost",
        height=600,
        width=1000,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("Interestingly, France, Croatia, Argentina, and Morocco also had a high number of aerial duels lost. However, this didn’t hurt their performance much, because the number of aerials they won was still greater. It shows that while they took risks, their success in the air made a real difference on the field.")