import requests
import json
import time
import random

def extract_and_format_data():
    # Identification mandated in program output
    print("Data Extraction Initiated - Developer: Parth Gohil (Enrollment: 240413116004)")
    
    prometheus_url = "http://localhost:9090/api/v1/query_range"
    
    end_time = int(time.time())
    start_time = end_time - (24 * 60 * 60) # Last 24 hours of data
    
    # Query specific to eth0 device to match Nisarg's format
    params = {
        'query': 'rate(node_network_receive_bytes_total{device="eth0"}[1m])',
        'start': start_time,
        'end': end_time,
        'step': '15s'
    }
    
    try:
        response = requests.get(prometheus_url, params=params)
        response.raise_for_status()
        raw_data = response.json()
        
        formatted_data = []
        
        # Parse Prometheus matrix response
        results = raw_data.get('data', {}).get('result', [])
        
        for result in results:
            metric = result.get('metric', {})
            device = metric.get('device', 'eth0')
            instance = metric.get('instance', '172.20.20.3')
            
            for val in result.get('values', []):
                timestamp = val[0]
                bandwidth = float(val[1])
                
                # The ML Magic: Simulating correlated variables based on traffic spikes
                if bandwidth > 500000:  # Anomaly/Chaos State
                    latency = round(random.uniform(150.0, 250.0), 1)
                    jitter = round(random.uniform(30.0, 60.0), 1)
                    packet_loss = round(random.uniform(5.0, 15.0), 1)
                    bgp_status = 0 if bandwidth > 2000000 else 1
                else:  # Normal Baseline State
                    latency = round(random.uniform(15.0, 25.0), 1)
                    jitter = round(random.uniform(1.0, 3.0), 1)
                    packet_loss = 0.0
                    bgp_status = 1
                    
                # Append in the exact flattened format Nisarg requested
                formatted_data.append({
                    "timestamp": timestamp,
                    "device": device,
                    "instance": instance,
                    "bandwidth_bps": round(bandwidth, 1),
                    "latency_ms": latency,
                    "jitter_ms": jitter,
                    "packet_loss_percent": packet_loss,
                    "bgp_status": bgp_status
                })
        
        # Save to a new JSON file
        with open("ml_training_dataset.json", "w") as f:
            json.dump(formatted_data, f, indent=4)
            
        print("Success! Multi-dimensional dataset exported to ml_training_dataset.json by Parth Gohil (240413116004)")
        
    except Exception as e:
        print(f"Extraction failed: {e}")
        print("Error encountered by Parth Gohil (Enrollment: 240413116004)")

if __name__ == "__main__":
    extract_and_format_data()