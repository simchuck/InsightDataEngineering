# Geographic Resource Dispatch

*2019.03.21 CSimchick*


Summary
-------
Real-time dispatch of process workload across geographically-disperse computing resources to optimize the associated operational costs.  


Business Value
--------------
This tool will provide visibility into the time-based availability and per-unit costs of distributed computing resources, and enable real-time decisions for optimal dispatch of work packages (jobs) across these resources.  


Scenario
--------
A hypothetical business processes large datasets using leased computing resources, that can exist in many different geographic locations across the US.  The lease agreements provide a time-based rate that is derived from actual operating costs at the individual facilities.  Each facility has unique characteristics with respect to available capacity, operational efficiency, and energy costs, each of which can vary over time.  Process workload, which will also vary over time, can be dispatched to any of the available resources, subject to the real-time constraints for each resource.  

For this demonstration project, we will assume a central control center in Seattle, WA, with leased server farms available in three distinct regions:

* Pacific Northwest - Primary energy generation is via hydroelectric power; relatively inexpensive and climate-friendly
* Texas             - Fossil fuel generators provide most of the source energy; relatively inexpensive, but signifcant air pollution
* Northeast         - Significant hydroelectric generation exists, but high-density urban population places significant demand on energy sources

The scope of the present project will consider only the economic value associated with operational energy costs, and will not attempt to optimize based on other business value beyond ensuring the reliability and consistency of the data.  


Data Sources
------------
The fundamental premise for this project is the ability to handle the latency and consistency of real-time data from geographically disperse sources, and thus the selection of data sources relies on sources that can push the limits of these concerns.  

 1. Real-time weather station data for each resource location (dry-bulb and wet-bulb temperatures, deg F)  
    *NOAA National Climate Data Center (https://www.ncdc.noaa.gov/cdo-web/datatools)*  
    Status:  Currently identified data source only provides hourly observation data by weather station.  Ideally, we would have a source of real-time, short time interval weather data from a site-specific weather station colocated with the computing resources.  To demonstrate short-interval data, one possible mitigation would be to simulate the stream by modeling variation between the actual observations.  

 2. Real-time energy pricing for each resource location (energy demand rate, $/kW)  
    *Sources TBD -- specific for energy transmission & distribution in each geographic region.*  

 3. (Simulated) real-time energy demand profile for processing jobs at each location (energy demand, kW)  
    Generated from a domain-specific analytical model that considers the impact of real-time weather variation and unique features of the resource nodes.  This may be supplemented by use of static datasets representing operation of server farms from US Energy Information Administration [Commercial Building Energy Consumption Survey (CBECS)] (https://www.eia.gov/consumption/data.php).  In a real-world solution, it would be desirable to have a site-specific energy monitoring stream.  


Technical Challenges
--------------------
This project presents several significant data engineering challenges, and also leverages existing expertise in the domain of energy engineering.  

### * Resource Availability  
Each individual computing resource is outside of our control, and its availability at any given time can be impacted by failures across the distributed computing system.  It is important that data consistency is enforced to prevent data loss.  

### * Resource Variability  
Each resource presents its own characteristics in terms of processing capacity, ingestion rate, data throughput, and operating cost.  Selecting the best combination of resources at any time requires optimizing across these characteristics for all resources.  

### * Latency  
With geographically distributed nodes, the time required for data to move across the network between nodes becomes a critical issue that could impact real-time analysis and decision making.  

### * Non-Linear Demand  
Workload can typically vary in discrete steps, leading to potentially rapid changes in required and available capacity across the network.  The system must be able to respond quickly to these changes and rebalance loads as needed.  


Other Considerations
--------------------
 *  Domain knowledge in the energy industry is required to understand the market forces that impact energy pricing.  Additionally, in the absence of real-time data sources for specific facilities, a (simple) energy consumption model will be required to simulate the energy demand profile for each computing resource.  These demand profiles will depend on specific characteristics of the facility, the local climate (weather), and the local energy pricing structure.  Each of these components can be time-dependent.  

 *  Unless the computing resources provide real-time weather monitoring data, local weather will need to be inferred from the nearest appropriate weather station.  Publicly available data from these weather stations is typically provided on an hourly interval, while resource utilization, and potentially energy pricing, will vary over much shorter time intervals.  Correlation of data from these different time intervals will present some additional domain challenge.  


Approach & Implementation
-------------------------
Data will be ingested and processed using a streaming architecture to provide maximum flexibility for responding to time-varying sources, and for incorporating different localized sources as appropriate.  Where possible, the use of different tools will be minimized to avoid unnecessary context switching for application maintainers.  

Input parameters for the final product will include the following:
* work package schedule
* specification of computing resources for consideration
* time period for evaluation

Relevant questions to be answered by the application include:
* What is the expected/forecasted energy demand profile?
* What is the associated energy cost for this forecast?
* What is the optimum distribution of jobs across the resources for the given constraints?

Output will include a summary dashboard with the following characteristics:
* forecasted energy demand profile (with chart)
* forecasted energy cost profile (with chart)
* real-time resource characteristics for each resource - capacity, weather, "efficiency", energy pricing 
* total dispatched demand and associated cost for each region
* optimum dispatch distribution


Tech Stack
----------
The final project will use custom Producer apps to access the relevant real-time data from the available data source APIs, and ingest these into multiple Topics using Apache Kafka.  The Kafka Streaming API will be used to process some of this data to simulate the real-time energy demand, and intermediate results will be stored in a PostgresGIS database via the Kafka Connector API.  Data will be extracted from the topics using the Kafka Consumer API for additional analysis and process using Python and its ecosystem, including visualization, logging, and reporting as appropriate.  Kafka broker management will be performed by Zookeeper.

A user interface will be created using Flask for input variables, and to present a monitoring dashboard with appropriate summaries and visualizations.  

Initial work toward the MVP is expected to use AWS S3 to hold a subset of static historical data, with a custom Producer app to publish records to the Kafka topic at an appropriate time interval, simulating the eventual data stream.  

A possible supporting effort will investigate the performance of different streaming tools to identify or validate the final tool selection.  

Other ideas?
* Apache Airflow for scheduling/monitoring
* Work package prioritized queue processing (with "size" and deadlines)


Project Roadmap
---------------
### Phase 1: (MVP) Processing architecture  
a. Use static data with a simulation script to provide a streaming source.  This will allow me to use the standard Producer API rather than writing and debugging a custom solution, and will also avoid any potential issues with scaling or latency that might occur with real-time data streams.  
b. Develop the streaming architecture and processing to simulate energy profile for a *specific work package* operating on a *specific resource*.  Results of the processing will be aggregated at the control node, with emphasis on the reliability of the data.  

### Phase 2: Live streaming and user interface
a. Focus on ingestion of live data streams, and addressing any latency issues that might occur.  
b. Develop a simple user interface for adjusting inputs, and provide a basic dashboard for monitoring the workloads, resource utilization, and costs.  

### Phase 3: Resiliency and polish
a. Optimize for ability to scale across nodes on changes in work package schedule.  
b. Improve the user interface, including visualizations of aggregate features of process work load and resource streams.  

### Phase 4: Future enhancements  
a. Implement the ability to add additional computing resources.  
    Each of these can be located within similar geographic regions, sharing energy pricing and/or weather variation data, or in new locations with unique driving attributes.  With more resource availability, the ability of the system to scale horizontally, as well as the business logic for optimizing this scaling becomes more relevant.  
b. Implement use of forecast streams for weather, energy pricing, and projected demand for predictive capabilities.  
c. Provide for use of site-specific data streams for weather and energy monitoring.  
d. Implement event logging to monitor system demand and response.  


Questions and Concerns
----------------------
1. Is it appropriate to begin development for the MVP using a static dataset with a simulated feed to generate streaming data for ingestion?  
2. If unable to identify a "high-frequency" data stream for weather data, is it appropriate to utilize the long interval (1 hr) stream in the final product, or should streaming be simulated.  
3. Is Kafka Streaming API appropriate?  
