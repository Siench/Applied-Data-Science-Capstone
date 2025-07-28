#Excute in the terminal
#python3.11 -m pip install pandas dash
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/t4-Vy4iOU19i8y6E3Px_ww/spacex-dash-app.py"
#python3.11 spacex-dash-app.py
#


# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),

    # TASK 1: Dropdown for Launch Site
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                 ],
                 value='ALL',
                 placeholder='Select a Launch Site',
                 searchable=True),
    html.Br(),

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3: Range Slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=min_payload,
                    max=max_payload,
                    step=1000,
                    marks={int(i): f'{int(i)}' for i in range(0, 11000, 2500)},
                    value=[min_payload, max_payload]),
    html.Br(),

    # TASK 4: Scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Pie chart callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(site):
    if site == 'ALL':
        df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df, names='Launch Site',
                     title='Total Success Launches By Site')
    else:
        df = spacex_df[spacex_df['Launch Site'] == site]
        count = df['class'].value_counts().reset_index()
        count.columns = ['Outcome', 'Count']
        count['Outcome'] = count['Outcome'].replace({1: 'Success', 0: 'Failure'})
        fig = px.pie(count, names='Outcome', values='Count',
                     title=f'Total Launch Outcomes for {site}')
    return fig

# TASK 4: Scatter plot callback
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def update_scatter(site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)

    if site == 'ALL':
        df = spacex_df[mask]
        title = 'Correlation between Payload and Success for All Sites'
    else:
        df = spacex_df[(spacex_df['Launch Site'] == site) & mask]
        title = f'Correlation between Payload and Success for {site}'

    fig = px.scatter(df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title=title)
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
