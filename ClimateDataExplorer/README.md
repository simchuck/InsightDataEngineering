# Climate Data Explorer

*2019.03.20 CSimchick*


Summary
-------
Climate change is a critical and topical issue, and there are many diverse sources of data that characterize its causes and effects via both quantitative and qualitative means.  The goal of this project is to bring this data together into a common tool that can provide various reporting and visualization tools to help the data engineer develop intuition about the datasets, and to identify potential correlations that could be further explored.  

The project will ingest data from multiple, divers climate-related sources and provide basic reporting and visualization functionality to allow data scientist users to explore the datasets in context, and to develop some basic intuition about correlations that can help to select data for further exploration and analysis.  


Business Value
--------------
This tool will reduce the time required for a data scientist to identify appropriate data sets for analysis for questions related to climatological concerns.  It could be used in climatological research, reporting, and projections/forecasts of future interactions and impacts.  


Data Sources
------------
1. NOAA National Climate Data Center (https://www.ncdc.noaa.gov/cdo-web/datatools)
   Diverse collection of historical climatological data, including terrestrial and marine conditions, weather data and events.  This source will provide structured data representing the actual measured climatoligical observations which indirectly drives data for other sources.  
2. US Energy Information Administration (https://www.eia.gov/consumption/data.php)
   Energy consumption survey data for residential (RBECS), commercial (CBECS), and manufacturing (MECS) facilities.  Represents end-user energy consumption based on fuel/energy type and usage categories within each sector.  This can also serve as a proxy for real-time smart meter data streams.  
3. Common Crawl (https://commoncrawl.org)
   Extensive web crawl data providing a rich corpus for assessing the prevalence of climate-driven business activity.  Will extract and filter based on representative climate specific keywords to produce timestamped profile.  
4. Global Database of Events Language and Tone (https://gdeltproject.org)
   A global aggregation of broadcast, print, and web news media.  Use will extract and filter stories based on representative climate-specific keywords to produce a timestamped profile that can serve as a proxy for public interest in climate related data and events.  


Engineering Challenge
---------------------
The proposed datasets comprise a broad array of structured and unstructured data, including numerical and textual based, that can be mapped to a common timeline.  Using a streaming architecture will provide maximum flexibility for incorporating new data sets.  The ability to present appropriate summary information in a side-by-side format, as well as interactive visualization, presents an interesting challenge to present this data with low latency that allows for unhindered exploration by the end user.  


Tech Stack
----------
I want to use streaming architecture (even though most processing can be done in batch mode) to allow flexibility for extending to real-time data processing for future use cases.  
(Looking for ideas here...)

1. Transfer data from original sources to AWS S3
2. Kafka Connector API to ingest into pub-sub topics
3. Kafka Streaming API to process data (map-reduce and filtering as approriate to index and aggregate data)
4. Kafka Consumer API 
5. Use ??? database to store indexed data for user exploration
6. Kafka Producer API to provide access via topic
7. Python for back end aggregation reports and interactive visualization engine (Bokeh?)
8. Flask for web interface


Project Roadmap
---------------
Initial MVP will ingest a limited subset of available data (historical climatological and energy consumption), index by time to correlate the data sets, and provide some basic summary statistics on the aggregated data via a Flask web application.

Future enhancements:
- UI to select a subset of data based on source
- UI to select a subset of data based on time period
- UI to provide interactive visualizations
- Incorporate other data sets, including unstructured text-based sources (GDELT, CommonCrawl)
- Provide mechanism to produce indexed dataset aggregations (joins ?) with from selected datasets and time periods)
- Simulation of real-time data streams using period data queries from historical datasets.  


    NOTES
    -----
    2019.03.20  16:10
    Based on feedback from project check-in, Curtis suggested an approach which 
    puts more focus on collecting real-time data for weather, energy pricing, and
    energy requirements, and incorporates a geographic/regional element to provide
    the challenge of latency and data consistency.  
    Pivoting this project to *"Geographic Resourcee Dispatch"*
