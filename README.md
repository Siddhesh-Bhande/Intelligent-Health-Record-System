# Intelligent Health Record System & Clinical Companion

A modular clinical health record and personal analytics platform built with Streamlit and Python. Features predictive health risk modeling, NLP-assisted clinical note summarization, immutable blockchain-style audit logging, and telehealth scheduling.

## Overview

Modern digital health applications require clear data integration across wearable telemetry, clinical documentation, and predictive risk indicators. This platform demonstrates an end-to-end architecture unifying disparate health metrics into real-time visual dashboards and actionable patient insights.

## Core Modules

### 1. Longitudinal Health Records and Telemetry
- **Record Management**: Centralized patient health record CRUD with schema validation (`record_management.py`).
- **Telemetry Ingestion**: Simulated continuous biometric feeds (heart rate, glucose, blood pressure, sleep cycles) (`data_integration.py`).

### 2. Predictive Analytics and Clinical Intelligence
- **Risk Assessment Model**: Machine learning classifier calculating cardiovascular and metabolic risk scores (`predictive_analytics.py`).
- **Clinical NLP Summarizer**: Keyword and semantic summarizer extracting diagnoses, medication regimens, and follow-ups from raw clinician notes (`nlp_summarizer.py`).
- **Personalized Recommendations**: Rule-based engine generating preventive care alerts based on biometric thresholds (`recommendations.py`).

### 3. Security, Auditing and Telehealth
- **Immutable Ledger Logging**: SHA-256 cryptographic chain verifying record integrity and detecting unauthorized modifications (`blockchain_logging.py`).
- **Telehealth Scheduler**: Interactive appointment manager with status tracking and calendar slot reservations (`telehealth.py`).

## Architecture and Project Structure

```
Intelligent-Health-Record-System/
├── docs/
│   └── requirements.md            # Detailed product requirements and system specifications
├── analytics.py                   # Health trend calculations and Matplotlib/Base64 visual pipelines
├── app.py                         # Streamlit multi-tab dashboard interface
├── blockchain_logging.py          # Cryptographic audit hash chain
├── data_integration.py            # Telemetry ingestion and simulated wearable integration
├── demo_data.py                   # Seed datasets for clinical evaluation
├── health_records.json            # Local record store
├── nlp_summarizer.py              # Clinical text extraction and extractive summarization
├── predictive_analytics.py        # Machine learning risk classification
├── recommendations.py             # Rule-based patient health advisory engine
├── record_management.py           # Core patient record persistence layer
├── requirements.txt               # Pinned Python package dependencies
├── telehealth.py                  # Virtual consultation scheduler
├── telehealth_appointments.json   # Telehealth appointment state store
├── .gitignore                     # Python, Streamlit, and OS ignore specifications
├── LICENSE                        # MIT License
└── README.md                      # Architecture and setup guide
```

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Siddhesh-Bhande/Intelligent-Health-Record-System.git
   cd Intelligent-Health-Record-System
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the application:
   ```bash
   streamlit run app.py
   ```

## Specifications

Detailed functional requirements and technical domain considerations are documented in [docs/requirements.md](docs/requirements.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
