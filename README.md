🚀 Telemetry Stack Architecture & Deployment Guide
Overview
This project sets up a robust, real-time observability and telemetry pipeline for an SD-WAN simulated network. It utilizes Containerlab to provision network nodes (Hub and Branch), Prometheus for metric scraping, and OpenObserve for centralized log and metric visualization.

Technology Stack
Infrastructure as Code (IaC): Containerlab

Containerization: Docker & Docker Compose

Metrics Collector: Prometheus

Agent/Exporter: Prometheus Node Exporter

Observability Backend: OpenObserve

📂 Configuration Files
1. Network Topology (topology.clab.yml)
Simulates the network nodes and binds their internal metric ports (9100) to the host machine for scraping. We utilize the node-exporter image directly to bypass WSL kernel limitations regarding advanced routing modules.

YAML
name: mpls-sdwan-sim

mgmt:
  network: bridge

topology:
  nodes:
    hub:
      kind: linux
      image: prom/node-exporter:latest
      ports:
        - "9101:9100"
    branch-a:
      kind: linux
      image: prom/node-exporter:latest
      ports:
        - "9102:9100"

  links:
    - endpoints: ["hub:eth1", "branch-a:eth1"]
2. Telemetry Backend (docker-compose.yml)
Provisions the Prometheus server and the OpenObserve dashboard.

YAML
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus-server
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  openobserve:
    image: public.ecr.aws/zinclabs/openobserve:latest
    container_name: openobserve-server
    environment:
      - ZO_ROOT_USER_EMAIL=admin@hackathon.com
      - ZO_ROOT_USER_PASSWORD=Hackathon@2026
    ports:
      - "5080:5080"
3. Scraping Configuration (prometheus.yml)
Instructs Prometheus to scrape the Containerlab nodes and remote-write the data to OpenObserve.

YAML
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'routers'
    static_configs:
      - targets: ['host.docker.internal:9101', 'host.docker.internal:9102']

remote_write:
  - url: "http://openobserve:5080/api/default/prometheus/api/v1/write"
    basic_auth:
      username: "admin@hackathon.com"
      password: "Hackathon@2026"
🛠️ Deployment Instructions
Execute the following commands in the terminal in sequential order to bring up the entire stack:

Step 1: Clean up previous instances (Optional but recommended)

Bash
docker network prune -f
sudo containerlab destroy -t topology.clab.yml --cleanup
docker-compose down
Step 2: Start the Telemetry Backend

Bash
docker-compose up -d
Step 3: Deploy the Network Topology

Bash
sudo containerlab deploy -t topology.clab.yml
Step 4: Verify Deployment

Prometheus Targets: http://localhost:9090/targets (Should show 2/2 UP)

OpenObserve Dashboard: http://localhost:5080 (Check Metrics tab for incoming streams)

📡 API Integration Guide (For Frontend/App Developers)
To consume the live telemetry data in a frontend application (e.g., React, Next.js), poll the Prometheus HTTP API.

Replace <HOST_IP> with the actual local IPv4 address of the machine running the Docker containers (e.g., 10.101.41.32).

Endpoint: GET http://<HOST_IP>:9090/api/v1/query?query=<metric_name>

Useful Metrics for the Dashboard:

CPU Usage: node_cpu_seconds_total

Available Memory: node_memory_MemAvailable_bytes

Network Traffic Received: node_network_receive_bytes_total