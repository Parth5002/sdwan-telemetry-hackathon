# Project: Air-Gapped Predictive Copilot for Secure MPLS Operations
# Role: Network Operations & Telemetry Node

**Tech Stack:** 
- Docker, Containerlab, FRRouting (Simulated via node-exporter)
- Prometheus (Port 9090)
- FastAPI (Port 5000)

**Core Logic:**
- We are simulating MPLS/SD-WAN telemetry locally to bypass heavy VM constraints.
- The `live_api.py` reads from Prometheus and injects "Chaos Modes" (1-4) to simulate Hackathon Phase 6 validation scenarios (Congestion, BGP Flap, MPLS Failure, Policy Drift).

**Output Formatting Rule:**
- Never use source code comments for developer identification.
- Always include the developer's exact identification details directly in the active print statements of the program output.