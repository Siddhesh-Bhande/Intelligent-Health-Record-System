# Smart Health Companion Platform

A comprehensive health tracking and management application built with Streamlit. This project showcases a modular design for health data visualization, record management, predictive analytics, and telehealth appointment scheduling.

## Features

- **Health Dashboard**: View real-time health metrics and receive personalized recommendations
- **Health Records Management**: Add, update, and track your health records over time
- **Visual Analytics**: Visualize health trends and identify correlations between metrics
- **Risk Assessment**: ML-powered health risk evaluation based on your health data
- **Doctor Notes Analysis**: Summarize and extract key information from medical notes
- **Telehealth Integration**: Schedule and manage virtual doctor appointments

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/smart-health-companion.git
   cd smart-health-companion
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Project Structure

- `app.py`: Main Streamlit application
- `data_integration.py`: Simulates wearable data and handles file uploads
- `record_management.py`: Manages health records with file-based storage
- `analytics.py`: Generates health trends and visualizations
- `predictive_analytics.py`: Risk prediction model and alerts
- `nlp_summarizer.py`: Analyzes and summarizes doctor notes
- `recommendations.py`: Generates personalized health recommendations
- `blockchain_logging.py`: Secure record change logging with hash-based integrity
- `telehealth.py`: Virtual appointment scheduling and management

## Use Cases

- Personal health tracking and monitoring
- Visualizing health trends over time
- Receiving automated health recommendations
- Analyzing correlations between different health metrics
- Extracting key information from doctor visit notes
- Managing telehealth appointments

## Deployment

This application is ready to be deployed on Streamlit Sharing, a free hosting service for Streamlit apps.

## License

MIT

## Acknowledgements

This project was created as a demonstration of a modern health companion application using Streamlit.
