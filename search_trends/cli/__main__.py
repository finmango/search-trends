import click
from search_trends.src.timeline import Timeline
import pandas as pd

@click.command(name='get_trends_for_geo')
@click.option('--terms', '-t', multiple=True, required=True, help='Search terms to query')
@click.option('--start-date', '-s', required=True, help='Start date in YYYY-MM-DD format')
@click.option('--end-date', '-e', required=True, help='End date in YYYY-MM-DD format')
@click.option('--frequency', '-f', type=click.Choice(['DAY', 'WEEK', 'MONTH']), default='DAY', 
              help='Frequency of data points')
@click.option('--geo-restriction', '-g', type=click.Choice(['country', 'dma', 'region']), 
              default='country', help='Type of geographic restriction')
@click.option('--geo-restriction-option', '-o', default='US', 
              help='Geographic area code (e.g., US for country, US-NY for region)')
@click.option('--output-file', '-of', help='Output file path for CSV export (optional)')
def get_trends_for_geo(terms, start_date, end_date, frequency, geo_restriction, geo_restriction_option, output_file):
    """Query Google Trends for search volume data."""
    timeline = Timeline()
    results = timeline.get_search_volumes(
        terms=list(terms),
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        geo_restriction=geo_restriction,
        geo_restriction_option=geo_restriction_option
    )
    
    # Convert results to DataFrame for nice display
    df = pd.DataFrame(results, columns=['Term', 'Date', 'Value'])
    
    # Save to CSV if output file is specified
    if output_file:
        df.to_csv(output_file, index=False)
        click.echo(f"Results saved to {output_file}")
    
    click.echo(df.to_string(index=False))

if __name__ == '__main__':
    get_trends_for_geo()