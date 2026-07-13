# 03_Execution_Plan: Project Roadmap

| Phase | Objective | Team Lead | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Network Simulation (SD-WAN/MPLS) | Parth Gohil | Completed |
| **Phase 2** | Telemetry Pipeline & Scrape Config | Parth Gohil | Completed |
| **Phase 3** | Predictive Modeling (Anomaly Detection) | Nisarg Bavaskar | In-Progress |
| **Phase 4** | Offline LLM & RAG Deployment | Devang Bavaskar | Completed |
| **Phase 5** | Copilot Logic & Automation | Devang/Preet | In-Progress |
| **Phase 6** | Scenario Validation (Chaos Testing) | Parth/Team | Pending |

## Pending Work Overview
- **Prediction Lead Time:** Currently, our model triggers *upon* anomaly; we must refine the `watchdog.py` to identify *precursor trends* (e.g., latency drift) to meet the "preventive intervention" objective.
- **Chaos Scenarios:** Implementation of the 4 mandatory fault scenarios into the live API.
- **Runbook Mapping:** Preet needs to map the 4 scenarios to concrete CLI-based remediation runbooks for the Vector DB.