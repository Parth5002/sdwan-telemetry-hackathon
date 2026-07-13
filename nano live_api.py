from fastapi import FastAPI
import requests
import random

app = FastAPI()

@app.get("/live-metrics")
def get_live_data():
    prometheus_url = "http://localhost:9090/api/v1/query"
    
    # Querying the exact live bandwidth
    params = {
        'query': 'rate(node_network_receive_bytes_total{device="eth0"}[1m])'
    }
    
    try:
        response = requests.get(prometheus_url, params=params)
        response.raise_for_status()
        raw_data = response.json()
        
        results = raw_data.get('data', {}).get('result', [])
        
        if not results:
            return {"error": "No data found from Prometheus right now."}
        
        # Extracting the single latest value
        metric = results[0].get('metric', {})
        device = metric.get('device', 'eth0')
        instance = metric.get('instance', '172.20.20.3')
        
        val = results[0].get('value', [])
        timestamp = val[0]
        bandwidth = float(val[1])
        
        # Simulating multivariate data based on live bandwidth
        if bandwidth > 500000:  # Chaos Attack Live
            latency = round(random.uniform(150.0, 250.0), 1)
            jitter = round(random.uniform(30.0, 60.0), 1)
            packet_loss = round(random.uniform(5.0, 15.0), 1)
            bgp_status = 0 if bandwidth > 2000000 else 1
        else:  # Normal Network Live
            latency = round(random.uniform(15.0, 25.0), 1)
            jitter = round(random.uniform(1.0, 3.0), 1)
            packet_loss = 0.0
            bgp_status = 1
            
        print("API Pinged successfully. Live Data Served - Developer: Parth Gohil (Enrollment: 240413116004)")
            
        return {
            "timestamp": timestamp,
            "device": device,
            "instance": instance,
            "bandwidth_bps": round(bandwidth, 1),
            "latency_ms": latency,
            "jitter_ms": jitter,
            "packet_loss_percent": packet_loss,
            "bgp_status": bgp_status
        }
        
    except Exception as e:
        print("API Error Encountered - Developer: Parth Gohil (Enrollment: 240413116004)")
        return {"error": str(e)}