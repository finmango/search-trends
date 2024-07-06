# WORK IN PROGRESS

Code used for FinMango [FinTrends](https://www.finmango.org/trends)

Example usage: 
```
# Make sure to have the API key in your environment variables

from src.timeline import Timeline
search = Timeline()

df = search.get_search_volumes(
    terms=['anxiety','depression']
    start_date='2024-01-01',
    end_date='2024-03-03',
    frequency='D',
    geo_restriction='country',
    geo_restriction_option='US'
)

```