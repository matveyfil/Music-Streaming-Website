# Music Streaming Project – Logging & Monitoring

This part of the project focuses on setting up **centralized logging and monitoring** for all microservices.

## Work Done
- Configured **Fluent Bit** to collect logs from all Docker containers.  
- Integrated logs with **Elasticsearch** for indexing and storage.  
- Connected **Kibana** for log visualization and dashboard creation.  
- Created filters to separate logs per microservice.  
- Ensured logs are persisted with **Elasticsearch volumes** (data survives container restarts).  
- Verified dashboards and log search functionality inside Kibana.  

## Outcome
- All services now send logs into a single system.  
- Developers can search, filter, and analyze logs in **Kibana**.  
- Project is ready for **dashboards, alerts, and observability improvements**.  
