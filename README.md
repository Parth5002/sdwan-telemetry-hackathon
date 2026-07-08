# Telemetry Pipeline and Chaos Engineering for SD-WAN Simulation

**Developer:** Parth Gohil (Enrollment: 240413116004)  
**Team Members:** Nisarg, Devang Bavaskar  

---

## 1. Project Overview
The objective of this module was to design, deploy, and monitor a virtualized SD-WAN network topology (Hub and Branch architecture) to facilitate the training of an AI/ML-based threat detection model. The project involved setting up a robust telemetry stack to monitor network health in real-time, deliberately injecting network anomalies (Chaos Engineering), and extracting the resulting datasets for machine learning applications.

## 2. Architecture and Technology Stack
* **Infrastructure Simulation:** Docker & Containerlab (Simulating Hub and Branch-A routers).
* **Data Collection (Agent):** Prometheus Node Exporter (Extracting hardware and network metrics).
* **Telemetry & Time-Series Database:** Prometheus (Scraping and storing real-time metrics).
* **Data Visualization:** OpenObserve (Providing an enterprise-grade UI for real-time traffic monitoring).
* **Chaos Engineering:** `iperf3` (Generating high-bandwidth simulated network attacks).

## 3. Implementation Methodology
### Phase 1: Telemetry Integration
Node Exporter binaries were successfully deployed into the virtualized routers. Prometheus was configured to scrape these endpoints at regular intervals to monitor standard operational metrics.

### Phase 2: Resolving Infrastructure Bottlenecks
* Addressed dynamic IP allocation issues ("IP Roulette") within the Docker network by inspecting live container IPs and dynamically updating the Prometheus YAML configurations. 
* Fixed DNS resolution errors inside Alpine containers by overriding the `resolv.conf` to utilize Google's public DNS (`8.8.8.8`).

### Phase 3: Chaos Engineering & Anomaly Generation
To provide actionable data for the ML model, a controlled network flood was executed. Using `iperf3`, approximately 136 GB of traffic was transmitted from Branch-A to the Hub over a 60-second window, peaking at 19.4 Gbits/sec.

### Phase 4: Dashboarding & Extraction
The generated anomaly (bandwidth spike) was successfully visualized in OpenObserve via the `remote_write` configuration in Prometheus. A custom Python script was then executed to query the Prometheus API (`/api/v1/query_range`) using PromQL, extracting the exact anomaly dataset into an `anomaly_data.json` file for the AI/ML pipeline.

## 4. Conclusion
The backend telemetry and observability pipeline is fully functional and battle-tested. It accurately captures baseline network behavior and successfully records synthetic anomalies, providing a reliable data foundation for downstream machine learning tasks.

