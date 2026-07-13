from fastapi import FastAPI
import requests
import random

app = FastAPI()

# Global variable to simulate progressive buildup over time for Scenario 1
congestion_counter = 0

@app.get("/live-metrics")
def get_live_data():
    global congestion_counter
    # Fetching from local Prometheus container
    prometheus_url = "http://localhost:9090/api/v1/query"
    
    params = {
        'query': 'rate(node_network_receive_bytes_total{device="eth0"}[1m])'
    }
    
    try:
        response = requests.get(prometheus_url, params=params)
        response.raise_for_status()
        raw_data = response.json()
        
        results = raw_data.get('data', {}).get('result', [])
        
        if not results:
            print("API Pinged. Error: No data from Prometheus - Developer: Parth Gohil (Enrollment: 240413116004)")
            return {"error": "No data found from Prometheus."}
        
        metric = results[0].get('metric', {})
        device = metric.get('device', 'eth0')
        instance = metric.get('instance', '172.20.20.3')
        
        val = results[0].get('value', [])
        raw_bandwidth = float(val[1])
        
        # --- NATURAL VARIANCE (Makes the graph wiggle) ---
        bandwidth = raw_bandwidth * random.uniform(0.9, 1.1)
        latency = round(random.uniform(15.0, 25.0), 1)
        jitter = round(random.uniform(1.0, 3.0), 1)
        packet_loss = 0.0
        bgp_status = 1
        
        chaos_mode = 0  
        
        if chaos_mode == 1:
            # Scenario 1: Progressive Congestion Buildup
            congestion_counter += 50000
            bandwidth = 300000 + congestion_counter
            latency = 20.0 + (congestion_counter / 5000)
            if bandwidth > 800000:
                packet_loss = random.uniform(5.0, 10.0)
                
        elif chaos_mode == 2:
            # Scenario 2: BGP Route Flap
            bgp_status = random.choice([0, 1, 0, 0]) # High chance of dropping
            if bgp_status == 0:
                packet_loss = 100.0
                bandwidth = 0.0
            else:
                latency = random.uniform(200.0, 300.0) # Downstream reroute latency
                
        elif chaos_mode == 3:
            # Scenario 3: Intermittent MPLS Underlay Failure
            jitter = random.uniform(40.0, 80.0)
            packet_loss = random.uniform(10.0, 20.0)
            latency = random.uniform(150.0, 200.0)
            
        elif chaos_mode == 4:
            # Scenario 4: Controller Misconfiguration (Policy Drift)
            # Bandwidth is normal, but latency and jitter spike due to bad policy
            latency = random.uniform(100.0, 500.0)
            jitter = random.uniform(10.0, 20.0)

        # Reset congestion counter if we switch out of mode 1
        if chaos_mode != 1:
            congestion_counter = 0
            
        print(f"API Pinged successfully. Mode: {chaos_mode}, Serving: {round(bandwidth, 1)} bps - Developer: Parth Gohil (Enrollment: 240413116004)")
            
        return {
            "timestamp": val[0],
            "device": device,
            "instance": instance,
            "bandwidth_bps": round(bandwidth, 1),
            "latency_ms": round(latency, 1),
            "jitter_ms": round(jitter, 1),
            "packet_loss_percent": round(packet_loss, 1),
            "bgp_status": bgp_status
        }
        
    except Exception as e:
        print(f"API Error Encountered: {str(e)} - Developer: Parth Gohil (Enrollment: 240413116004)")
        return {"error": str(e)}