Real Time Resource Dispatch
presentatation script - draft
2019.04.11 (revisions in progress)


## Title / Introduction

[slide: Title]

Hello everyone.  My name is Charles Simchick and I am a Data Engineering Fellow with Insight.  

I built a data pipleline that ingests data from multiple sources, processes these data streams in real-time, and uses the results to make decisions on the optimum utilization of distributed resources represented by that data.  


## Motiviation & Business Value

[slide: Motivation][Energy is a commodity -- costs can be optimized across geographically distributed resources]

I would like to start by providing a little bit of context around the domain space in which I have chosen to implement my project.  I have a background in Energy Engineering, with a lot of experience managing and analyzing the time series data associated with that domain.  One of the most important aspects is the cost of energy.  

Electrical energy is made available through regional markets, each with its own <<cost structure>> related to the available fuel sources and generation infrastructure, and the population density across that region.  At the same time, weather variations have a strong corrleation with the energy required for cooling systems.  Taken together, the result is a continually varying cost for production and delivery of that energy, which is <<made practical>> in the real-time energy commodity pricing.  

Distributed computing resources can be located within any of these geographic regions, and thanks to the different time zones, there can be significant energy commodity price differences.  My project is <<focused>> on capitalizing on these differences to optimize the total cost for dispatching data processing jobs across the available "resource nodes".  

[slide: Sample Data][Time series data for each resource node must be combined to generate the real-time pricing]

A real world application of this pipeline would use actual API data, however I am simulating the data sources for my hypothetical use case to allow more flexibility in <<analyzing>> and demonstrating data ingestion rates.  The siultions are based on representative historical data, and streams are generated for multiple resource nodes.  

[slide: Data Transformations][KSQL provides an accessible abstraction over the Kafka Streams API for real-time stream processing]

The backbone of the data pipeline uses Apache Kafka, and the KSQL API from Confluent provides a very accessible interface to utilize the built-in streaming capabilities.  Intermediate transformations are made to the source data streams in real-time, and results from each resource node are considered against a prioritized job queue to determine the optimium dispatch of these jobs across the nodes.  


## Demonstration

[slide: Demonstration][The application allows me to spawn new nodes, add to the job queue, and tweak the ingestion rate parameters]
[live demo of application]

I am going to switch over now to demonstrate my application.  

This is the main user interface, which shows the job queue on the left side of the display, along with a time-series plot showing the real-time variation in energy pricing <<and capacity>> for each resource node, and stacked bar charts representing how those jobs are dispatched to the resource nodes.  

As data is ingested an processed, the node pricing and capacity values are updated, and the job queue changes to reflect the processing status.  

<<Now I started the app a little bit before this presentation, and configured it to read real-time data from a couple of actual web APIs for a single location near XXX.  Since all of the elements for my hypothetical use case do not exist, I am simulating some of the input streams to generate the necessary data.  As you can see, the "real-time" data interval is relatively slow at about five minutes per record.  
>>

I am going to spawn a few more simulated resource nodes, and generate some new jobs for the queue to demonstrate the result...

Next I will add more jobs to the queue, and increase the ingestion rate for each to speed things up...

...

As you can see, the time series plot indicates the variation in the pricing and capacity at each resource node, and the job queue is updated with current status of each job.  The resource load bar charts react dynamically to illustrate job dispatch.  


## Technology

[slide: Technology Stack]

My pipeline is currently hosted entirely on Amazon AWS.  I have an S3 bucket with the static data used for the simulated data streams.  A single EC2 instance hosts all of my producer code to read records from the S3 bucket and make appropriate transformations for the simulation before publishing to the corresponding Kafka topics.  

My Kafka cluster consists of four EC2 instances, with one master and three workers.  

A separate EC2 instance hosts the Confluent KSQL API, which provides an abstraction over the Kafka KStreams API to perform real-time stream processing using a declarative SQL-like syntax.  The simplicity of this interface, along with the close integration into Kafka, makes this a very fast and attractive option for real-time processing.  

I have another EC2 instance that hosts my consumer code, which reads data from the Kafka topics and performs the job queue dispatch optimization.  

A final EC2 instance hosts my user interface, which uses the Dash package to provide a web interface with dynamic charting appropriate for display of the real-time processing pipeline.  

*** STOPPED EDITING HERE 2019.04.11 ***


In addition to the data streams for each resource, node I am taking advantage of the Kafka architecture to publish both the job queue and dispatch queue into separate topics, which provides a convenient storage for accessing this information.  I am also using a Kafka topic to store "clickstream" data from the user interface input.  

You may have noticed that I do not have a separate database in my pipeline.  I had originally planned to use a Postgres database to store the structured time-series data.  But my use case does not require access to historical data, and the persistent nature of the Kafka topics provides all of the necessary storage for my application.  Eliminating a separate database reduces the overall complexity of the pipeline, and also avoids a potential bottleneck for transactions to and from the database.  

If some future case can be made for permanent storage of the data, it would be relatively trivial to implement the Kafka Connect API to directly transfer the data from the topics into the appropriate database.  This approach would appear to offer the most straightforward and efficient solution.  


## Challenges

[slide: Engineering Challenges]

There were a number of technical challenges in the course of this project, but two are most notable.

[slide: Challenge #1: KSQL Documentation and Operation]

First, KSQL is relatively new and immature technology.  The first release of the API was in December 2017, and the current version stands at 0.XXX.  While the Confluent website appears to have a lot of documentation, I found it to be somewhat obtuse and difficult to search effectively for answers to specific questions.  And discussions on Stack Overflow seem to suggest that this is difficulty is shared, with more questions and speculation than definitive answers.  

Through the course of my research, I was able to offer at least one solution to a shared problem (((deleting a KSQL stream after having first deleted the kafka topic registration))).  After completing my project, I intend to write a blog article discussing some of the difficulties I had, and to offer a straightforward "getting started" tutorial.  

[slide: Challenge #2: Coordination of Topic Streams]

The other major challenge I faced is around the coordination of timing for the different topic streams.  This issue manifests itself both in the separate streams associated with each particular resource node, and in the combination of data streams from different nodes during the dispatch optimization algorithm.  

Energy markets are time-sensitive -- the offered price at any time is only valid until the subsequent offer is made available, after which the previous offer is "expired".  These offers are typically made at regular intervals, but network communications and other factors could lead to more irregular ingestion of the data.  The processing of multiple streams needs to assure that it is using data which is valid with a certain time window.  Within any window, missing or duplicate events on any data stream will render the results incorrect and invalid.  The resource would not actually be available at the expected price.  

To solve this problem, I specified a time interval for each resource node based on the shortest update interval across all of its streams.  I should note that this I am using the "origination" time stamp when the record was actually created at the source, rather than the time of ingestion or processing in my pipeline.  The assigned timestamp for any processed results uses the most recent timestamp within that window.  This was a relatively naive algorithm, and there are probably further improvements that could be made.  


## Future Enhancements

[slide: Future Plans]

This project was conceived and implemented over the course of three weeks of intensive work, during which I was also gaining my first significant exposure to data engineering concepts in general, and to Kafka and its ecosystem more specifically.  so the time constraints required some quick decision-making that was not always fully informed, and there are probably many areas for improvement.  

Putting aside these questions, my roadmap for enhancing this project would include the following steps.  

First, I would like to look into moving most, if not all, of the processing logic into KSQL to take advantage of the efficiencies it offers.  

I would also like to implement the Connect API and an approriate database to provide an option for permanent storage of the data.  

There is also a possibility that the Connect API can be used for the original data ingestion from either the web APIs or the S3 data store, with any pre-processing logic for the simulation incorporated into a real-time KSQL stream.  

Finally, I would like to implement a "monitoring" topic to store data and metrics related to the operation of the data pipeline.  


## About Me

[slide: About Me]

That's the quick and dirty summary of my project, and I would be happy to discuss more of the details if you are interested.  

I would like you to also be interested in me, so I would like to share a little bit more about my interests.  

I will always consider myself first and foremost to be a Mechanical Engineer, and perhaps some of you may understand what I mean by this.  I have a lot of experience with project management and product development, and an affinity for filling the void whenever I find myself in a situation where effective leadership or management is not apparent.  

Outside of my professional interests, I have a dog that makes sure I always have something to do in my "free time".  I enjoy hiking, performing with my Japanese taiko group, and participating as a judge in homebrewing competitions.  

I want to thank you again for your time, and I would be happy to answer any questions you might have.  
