# 02_System_Design: Air-Gapped Predictive NOC Copilot

## 1. High-Level Architecture
The system follows a distributed microservices pattern, segregated by task-specific hardware to optimize local resource utilization:
- **Telemetry Layer (Node):** Containerlab nodes (FRR-based) exporting metrics via `node-exporter` over a local bridge network.
- **Processing Layer:** Python-based `watchdog` engine executing Isolation Forest ML models for anomaly forecasting.
- **Intelligence Layer:** Ollama (Llama-3) RAG pipeline backed by a Qdrant Vector Database containing ISRO-specific troubleshooting runbooks.
- **Visualization Layer:** Grafana dashboarding service querying Prometheus (metrics) and SQLite (AI-generated alerts).



## 2. Component Interaction
1. **Scrape:** Prometheus continuously pulls metrics from the containerized network topology.
2. **Analyze:** The Python-based watchdog polls Prometheus, detecting precursor anomaly patterns.
3. **Reason:** Anomaly alerts trigger the RAG pipeline; the Copilot queries the local Vector DB to synthesize context.
4. **Respond:** The AI generates structured CLI mitigation steps, which are persisted to SQLite.
5. **Visualize:** Grafana provides a unified view of telemetry spikes alongside AI-generated incident summaries.

## 3. Data Flow & Air-Gap Integrity
All data flows occur exclusively over a local IPv4 WLAN subnet. The system environment is hardened via local-only hostnames (e.g., `host.docker.internal`) and strict firewall rules. No external network traffic is required, satisfying the air-gapped security mandate.