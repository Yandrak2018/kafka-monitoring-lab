# TODO: Implement Kafka Producer

import os
import json
import time
import random
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
from kafka import KafkaProducer

# Cargar configuración desde la raíz
load_dotenv()

# Configuración de Kafka
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "localhost:29092")
TOPIC = os.getenv("TOPIC_NAME", "system-metrics-topic")
SERVER_IDS = ["web01", "web02", "db01", "app01", "cache01"]

def generate_metrics(server_id):
    """Genera el diccionario de métricas según el formato del PDF"""
    return {
        "server_id": server_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "cpu_percent": round(random.uniform(5.0, 80.0), 2),
            "memory_percent": round(random.uniform(20.0, 90.0), 2),
            "disk_io_mbps": round(random.uniform(0.1, 100.0), 2),
            "network_mbps": round(random.uniform(1.0, 500.0), 2),
            "error_count": random.randint(0, 3) if random.random() < 0.1 else 0
        },
        "message_uuid": str(uuid.uuid4())
    }

def run_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all' # Asegura que el mensaje llegue
        )
        print(f"🚀 Productor iniciado. Enviando a {TOPIC}...")

        while True:
            for server in SERVER_IDS:
                msg = generate_metrics(server)
                producer.send(TOPIC, value=msg)
                print(f"✅ [Sent] Server: {server} | UUID: {msg['message_uuid']}")
            
            time.sleep(10)

    except Exception as e:
        print(f"❌ Error en el productor: {e}")
    finally:
        producer.close()

if __name__ == "__main__":
    run_producer()