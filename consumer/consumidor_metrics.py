# TODO: Implement Kafka Consumer

import os
import json
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
from kafka import KafkaConsumer
from pymongo import MongoClient

load_dotenv()

# Configuración
MONGO_URI = os.getenv("MONGO_URI")
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
TOPIC = os.getenv("TOPIC_NAME")
WINDOW_SIZE = 20 # 

def run_consumer():
    # Conexión a MongoDB Atlas
    client = MongoClient(MONGO_URI)
    db = client['monitoring_db']
    col_raw = db['system_metrics_raw']
    col_kpis = db['system_metrics_kpis']

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        group_id='monitor_group_01',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest'
    )

    buffer = []
    start_time = time.time()

    print(f"📥 Consumidor conectado a {TOPIC}. Esperando datos...")

    try:
        for message in consumer:
            data = message.value
            
            # 1. Almacenar en RAW inmediatamente
            col_raw.insert_one(data)
            buffer.append(data)
            print(f"📝 Mensaje guardado en RAW ({len(buffer)}/{WINDOW_SIZE})")

            # 2. Lógica de KPIs (Ventana Tumbling)
            if len(buffer) >= WINDOW_SIZE:
                end_time = time.time()
                duration = end_time - start_time
                
                # Cálculos de promedios
                kpis = {
                    "avg_cpu": sum(m['metrics']['cpu_percent'] for m in buffer) / WINDOW_SIZE,
                    "avg_mem": sum(m['metrics']['memory_percent'] for m in buffer) / WINDOW_SIZE,
                    "avg_disk": sum(m['metrics']['disk_io_mbps'] for m in buffer) / WINDOW_SIZE,
                    "avg_net": sum(m['metrics']['network_mbps'] for m in buffer) / WINDOW_SIZE,
                    "total_errors": sum(m['metrics']['error_count'] for m in buffer),
                    "throughput": WINDOW_SIZE / duration
                }

                # Documento final de KPI
                kpi_document = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "window_duration_sec": round(duration, 2),
                    "message_count": WINDOW_SIZE,
                    "kpis": {k: round(v, 2) for k, v in kpis.items()}
                }

                col_kpis.insert_one(kpi_document)
                print(f"📊 [KPI] Ventana completada e insertada en MongoDB.")
                
                # Reiniciar ventana
                buffer = []
                start_time = time.time()

    except Exception as e:
        print(f"❌ Error en el consumidor: {e}")
    finally:
        consumer.close()
        client.close()

if __name__ == "__main__":
    run_consumer()