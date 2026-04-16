# Kafka Monitoring Lab# Kafka Monitoring Lab

Este proyecto implementa un sistema de monitorización de métricas de servidores en tiempo real utilizando una arquitectura de streaming de datos con **Apache Kafka** y almacenamiento persistente en **MongoDB Atlas**.

## 1. Arquitectura del Sistema

El sistema se compone de tres capas principales:
1.  **Productor (Python):** Simula la generación de métricas (CPU, Memoria, Disco) de 5 servidores diferentes y las envía a un tópico de Kafka cada 10 segundos.
2.  **Broker (Kafka):** Actúa como el motor de mensajería distribuida, gestionando el flujo de datos entre el productor y el consumidor.
3.  **Consumidor (Python):** Escucha el tópico de Kafka, almacena cada métrica individual en una colección "RAW" y calcula promedios (KPIs) cada ventana de 20 mensajes para almacenarlos en una colección "KPIs".

## 2. Tecnologías Utilizadas

* **Lenguaje:** Python 3.12+
* **Mensajería:** Apache Kafka (vía Docker)
* **Base de Datos:** MongoDB Atlas (Cloud)
* **Contenedores:** Docker & Docker Compose
* **Librerías Python:** `kafka-python`, `pymongo`, `python-dotenv`

## 3. Configuración del Entorno

### Requisitos Previos
* Docker Desktop instalado y en ejecución.
* Cuenta en MongoDB Atlas con un clúster activo.
* Python instalado.

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto con el siguiente formato:
```env
# Kafka
KAFKA_BOOTSTRAP_SERVER=localhost:29092
TOPIC_NAME=system-metrics-topic

# MongoDB Atlas
MONGO_URI=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/?appName=Cluster0
DB_NAME=monitoring_db