# BReOLAP: Your Fintech Realtime-OLAP Solution 🚀

Fintech organizations require an OLAP solution that can resolve complex analytical queries in milliseconds, enabling them to make informed, split-second decisions. Choosing the right Realtime-OLAP is crucial, and **BReOLAP** is here to guide you through selecting the best option for your specific needs!

----
## 🎯 Purpose

Our goal at BReOLAP is multi-fold:
- **Model Definition:** We define a model where specific requirements dictate the choice of database.
- **Benchmarking Insights:** Demonstrate our methodology for benchmark comparisons.
- **System Replication:** Provide insights into replicating contemporary systems for your use.

## 🏅 Candidate Realtime-OLAP

We've rigorously tested the following Realtime-OLAPs to ensure you get reliable, actionable insights:

| <img src="https://cdn.brandfetch.io/idnezyZEJm/w/400/h/400/theme/dark/icon.jpeg?c=1bx1741846904095id64Mup7acT2007dvU&t=1684474240695" width="100"> <br> **ClickHouse** | <img src="https://cdn.prod.website-files.com/62ccab534b634e946221774e/632ca26c3a7f081704214125_pinot_team.jpeg" width="100"> <br> **Pinot** |
|---------------------------------------------|------------------------------------------|
| <img src="https://pbs.twimg.com/profile_images/491968662899658752/F65UpOhT_400x400.png" width="100"> <br> **Druid** | <img src="https://avatars.githubusercontent.com/u/78232517?s=200&v=4" width="100"> <br> **StarRocks** |



### 🚧 In Progress
We are also in the process of evaluating these promising databases:
* **Doris**
* **Kylin**

# Flow of data

```mermaid
graph TD;
    
    subgraph ClickHouse & StarRocks
        A[data-source] -->|Kafka| B[sink-connector]
        subgraph DB1[Database]
            F[node] <--> C[controller] <--> D[node] 
        end
        B --> DB1
        DB1 -->|Processed Data| E[Query Engine & Ingestion Verifier]
    end

    subgraph Druid & Pinot
        G[data-source] -->|Kafka| H[internal-stream-ingestor]
        subgraph DB2[Database]
            I[controller] <--> J[node] <--> Q[historical-nodes] 
        end
        H --> DB2
        DB2 -->|Processed Data| K[Query Engine & Ingestion Lag Tracer]
    end
```
---

## 🛠️ Deep Dive into Our Technology

We're ready to answer your questions immediately! For those interested in a deeper understanding, here's how we equip you with the best tools:

- **Distributed Systems Setup:** Learn how we configure each candidate database to function efficiently in a distributed environment.
- **Table Definitions:** Discover how we define tables to run benchmark tests effectively.
- **Data Stream Integration:** See how we set up input streams to simulate real-time data flow.
- **Query Execution:** Understand our configurations for running queries and retrieving results smoothly.
- **Monitoring and Metrics:** Explore our setup with Prometheus and Grafana for real-time metrics collection.

Feel free to explore our [Documentation](#) for detailed guides and setups.

## 📢 Stay Tuned

For updates, further details, and live results, keep an eye on this space! We're constantly working to expand our insights and tools to help you stay ahead in the fast-paced world of Fintech.

---

We're excited to help you navigate the complex landscape of Realtime-OLAP solutions. With BReOLAP, you're not just choosing a tool; you're setting the stage for future-proof financial analytics!

