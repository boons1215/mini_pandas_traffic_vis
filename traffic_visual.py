import pandas as pd
import plotly.express as px
import sys
import argparse
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

    consumer_hostname_grouped.to_csv('consumer_hostname_without_applabel_output.csv', index=False)
    provider_hostname_grouped.to_csv('provider_hostname_without_applabel_output.csv', index=False)

def generate_sunburst_chart(df, maxdepth=2):
    # Group a DataFrame by the "Port" and "Protocol" columns and count the occurrences in total flows
    grouped = df.groupby(['Consumer app', 'Consumer env', 'Provider app', 'Provider env', 'Port', 'Protocol']).size().reset_index(name='Count')
    grouped.to_csv('consolidated_output.csv', index=False)
    print(grouped)

    # To count the total appearance of each port using the "grouped" DataFrame
    merge_grouped = grouped.groupby(['Consumer app', 'Consumer env', 'Provider app', 'Provider env']).size().reset_index(name='Count')
    merge_grouped.to_csv('222consolidated_output.csv', index=False)
    print(merge_grouped)

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
        #title=f'Sunburst Chart: {maxdepth} Layers - Inner Layer: Provider env, 2nd Layer: Provider app, 3rd Layer: Consumer env, 4th Layer: Consumer app',
        maxdepth=maxdepth,  
    )

    fig.add_trace(sunburst_chart.data[0])
    fig.update_layout(
        legend_title_text="Legend",
        legend_traceorder="normal",  # Change trace order in the legend
    )
    fig.update_traces(textinfo='label+percent entry', insidetextorientation='radial') 
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))  

    html_title = f'<div style="font-family: Rubik, sans-serif; font-size: 16px;">' \
                 f'<h2 style="text-align: left;">Sunburst Chart</h2>' \
                 f'<p style="text-align: left;">This Sunburst chart displays a hierarchical representation of data.</p>' \
                 f'<p style="text-align: left; font-size: 12px;">' \
                 f'Layer 1: Provider environment<br>' \
                 f'Layer 2: Provider application within Provider environment<br>' \
                 f'Layer 3: Consumer environment outbound to the Provider Application<br>' \
                 f'Layer 4: Consumer application within Consumer environment' \
                 f'</p>' \
                 f'</div>'
    
    chart_with_title_and_legend = f'<div>{html_title}{fig.to_html()}</div>'

    with open('sunburst_chart_with_legend.html', 'w') as f:
        f.write(chart_with_title_and_legend)

    fig.show()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate Sunburst chart from CSV data")
    parser.add_argument("csv_file_path", help="Path to the CSV file")
    parser.add_argument("--maxdepth", type=int, choices=[2, 3, 4], default=2, help="Maximum depth of the hierarchy (2, 3, or 4)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    df = read_csv_file(args.csv_file_path)
    df = preprocess_data(df)
    generate_consumer_and_provider_hostname_csv(df)
    generate_sunburst_chart(df, maxdepth=args.maxdepth)

if __name__ == "__main__":
    main()
