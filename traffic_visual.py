import pandas as pd
import plotly.express as px
import sys
from plotly.subplots import make_subplots
import plotly.graph_objs as go

def read_csv_file(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

def preprocess_data(df):
    # Replace empty values with "NO LABEL" in all columns
    df = df.fillna('NO LABEL').replace('', 'NO LABEL')
    return df

def generate_consumer_and_provider_hostname_csv(df):
    # Create DataFrames for Consumer and Provider Hostnames when 'Consumer app' or 'Provider app' is empty
    consumer_hostname_df = df[df['Consumer app'] == 'NO LABEL']
    provider_hostname_df = df[df['Provider app'] == 'NO LABEL']

    # Group and save DataFrames to CSV
    consumer_hostname_grouped = consumer_hostname_df.groupby(['Consumer Hostname', 'Consumer app']).size().reset_index(name='Count')
    provider_hostname_grouped = provider_hostname_df.groupby(['Provider Hostname', 'Provider app']).size().reset_index(name='Count')

    consumer_hostname_grouped.to_csv('consumer_hostname_output.csv', index=False)
    provider_hostname_grouped.to_csv('provider_hostname_output.csv', index=False)

def generate_sunburst_chart(df):
    # Group the DataFrame by the specified columns and count occurrences
    grouped = df.groupby(['Consumer app', 'Consumer env', 'Provider app', 'Provider env', 'Port', 'Protocol']).size().reset_index(name='Count')
    grouped.to_csv('consolidated_output.csv', index=False)
    print(grouped)

    merge_grouped = df.groupby(['Consumer app', 'Consumer env', 'Provider app', 'Provider env']).size().reset_index(name='Count')
    merge_grouped.to_csv('test.csv', index=False)

    # Create a subplot with a Sunburst chart
    fig = make_subplots(rows=1, cols=1)
    sunburst_chart = px.sunburst(
        merge_grouped,
        path=['Provider env', 'Provider app', 'Consumer env', 'Consumer app'],
        values='Count',
        color='Count',  
        color_continuous_scale='Viridis', 
        hover_name='Consumer app',  # Display Consumer app as hover text
        hover_data=['Count', 'Consumer app', 'Consumer env', 'Provider app', 'Provider env'],  
        labels={'Consumer app': 'Consumer App', 'Provider app': 'Provider App'},  
        title='Sunburst Chart as Provider App Centric', 
        maxdepth=2,  
    )

    # Add the Sunburst chart to the subplot
    fig.add_trace(sunburst_chart.data[0])

    # Customize the appearance of the Sunburst chart
    fig.update_traces(textinfo='label+percent entry', insidetextorientation='radial')  # Display labels and percentages
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))  # Adjust margin

    # Save the chart as an HTML file
    fig.write_html('sunburst_chart.html')
    fig.show()

def main():
    # Check if the user provided a CSV file path as a command-line argument
    if len(sys.argv) < 2:
        print("Please provide the path to the CSV file as a command-line argument.")
        sys.exit(1)

    csv_file_path = sys.argv[1]

    # Read and preprocess the CSV file
    df = read_csv_file(csv_file_path)
    df = preprocess_data(df)

    # Generate CSV files and Sunburst chart
    generate_consumer_and_provider_hostname_csv(df)
    generate_sunburst_chart(df)

if __name__ == "__main__":
    main()
