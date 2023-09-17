import pandas as pd
import plotly.express as px
import sys
from plotly.subplots import make_subplots
import plotly.graph_objs as go

# Check if the user provided a CSV file path as a command-line argument
if len(sys.argv) < 2:
    print("Please provide the path to the CSV file as a command-line argument.")
    sys.exit(1)

# Get the CSV file path from the command-line argument
csv_file_path = sys.argv[1]

# Read the CSV file into a Pandas DataFrame
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"File not found: {csv_file_path}")
    sys.exit(1)

# Replace empty values with "NO LABEL" in all columns
df = df.fillna('NO LABEL').replace('', 'NO LABEL')

# Create a DataFrame for Consumer Hostname when 'Consumer app' is empty
consumer_hostname_df = df[df['Consumer app'] == 'NO LABEL']
consumer_hostname_grouped = consumer_hostname_df.groupby(['Consumer Hostname', 'Consumer app']).size().reset_index(name='Count')
consumer_hostname_grouped.to_csv('consumer_hostname_output.csv', index=False)

# Create a DataFrame for Provider Hostname when 'Provider app' is empty
provider_hostname_df = df[df['Provider app'] == 'NO LABEL']
provider_hostname_grouped = provider_hostname_df.groupby(['Provider Hostname', 'Provider app']).size().reset_index(name='Count')
provider_hostname_grouped.to_csv('provider_hostname_output.csv', index=False)

# Group the DataFrame by the specified columns and count occurrences
grouped = df.groupby(['Consumer app', 'Consumer env', 'Provider app', 'Provider env', 'Port', 'Protocol']).size().reset_index(name='Count')
grouped.to_csv('consolidated_output.csv', index=False)
print(grouped)

# Create a 3D scatter plot with Plotly
png_grouped = df.groupby(['Consumer app', 'Consumer env', 'Provider app', 'Provider env']).size().reset_index(name='Count')

# Create a subplot with a Sunburst chart
fig = make_subplots(rows=1, cols=1)
sunburst_chart = px.sunburst(
    grouped,
    path=['Provider env', 'Provider app', 'Consumer env', 'Consumer app'],
    values='Count',
    color='Count',  # Color segments based on the Count variable
    color_continuous_scale='Viridis',  # Choose a color scale
    hover_name='Consumer app',  # Display Consumer app as hover text
    hover_data=['Count', 'Consumer env', 'Provider env'],  # Additional hover data
    labels={'Consumer app': 'Consumer App', 'Provider app': 'Provider App'},  # Rename labels
    title='Enhanced Sunburst Chart of Provider and Consumer Apps',  # Customize the title
    maxdepth=2,  # Limit the depth of the hierarchy
)

# Add the Sunburst chart to the subplot
fig.add_trace(sunburst_chart.data[0])

# Customize the appearance of the Sunburst chart
fig.update_traces(textinfo='label+percent entry', insidetextorientation='radial')  # Display labels and percentages
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))  # Adjust margin

# Show the interactive chart in a web browser (you can also save it as an HTML file)
fig.show()
