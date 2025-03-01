import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
import base64
import demo_data

# Import our modules
from data_integration import fetch_wearable_data, upload_health_data
from record_management import add_health_record, update_health_record, get_health_record, get_all_records, delete_health_record
from analytics import generate_health_trends, plot_metric, get_plot_as_base64
from predictive_analytics import train_risk_model, predict_risk, send_alert, generate_sample_training_data
from nlp_summarizer import simple_summarize, extract_key_info
from recommendations import generate_health_recommendations
from blockchain_logging import log_record_update, verify_ledger_integrity
from telehealth import schedule_telehealth_consultation, get_upcoming_consultations, cancel_consultation

# Set page configuration
st.set_page_config(
    page_title="Smart Health Companion", 
    page_icon="❤️", 
    layout="wide", 
    initial_sidebar_state="collapsed"  # Start with collapsed sidebar for mobile feel
)

# CSS customization
st.markdown("""
<style>
    /* Global styles */
    [data-testid="stSidebar"] {
        background-color: #f9f9f9;
        border-right: 1px solid #eee;
    }
    
    /* Header styles */
    .main-header {
        font-size: 2rem;
        color: #3366ff;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .section-header {
        font-size: 1.3rem;
        color: #3366ff;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid #f0f0f0;
    }
    
    /* Card styles */
    .metric-card {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
        border: 1px solid #f0f0f0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Status indicators */
    .status-healthy {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-caution {
        color: #ffc107;
        font-weight: bold;
    }
    
    .status-alert {
        color: #dc3545;
        font-weight: bold;
    }
    
    /* User profile */
    .user-profile {
        background: linear-gradient(135deg, #3366ff 0%, #00ccff 100%);
        color: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Mobile friendly buttons */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        font-weight: 500;
        padding: 0.5rem 1rem;
        background-color: #3366ff;
        color: white;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #2952cc;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        background-color: #f0f2f6;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3366ff !important;
        color: white !important;
    }
    
    /* Make dataframes more mobile-friendly */
    [data-testid="stDataFrame"] {
        overflow-x: auto;
    }
    
    /* Sidebar navigation */
    .sidebar-nav {
        padding: 0.5rem;
    }
    
    .sidebar-nav button {
        width: 100%;
        text-align: left;
        margin-bottom: 0.5rem;
        padding: 10px;
        border-radius: 8px;
        background-color: transparent;
        border: 1px solid #f0f0f0;
        transition: all 0.2s ease;
    }
    
    .sidebar-nav button:hover {
        background-color: #f0f2f6;
    }
    
    .active-nav {
        background-color: #e6f0ff !important;
        border-left: 4px solid #3366ff !important;
        font-weight: 600;
    }
    
    /* Icon styling */
    .icon {
        margin-right: 8px;
        vertical-align: middle;
    }
    
    /* Custom container */
    .custom-container {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Responsive tweaks */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.5rem;
        }
        
        .section-header {
            font-size: 1.1rem;
        }
        
        .metric-card {
            padding: 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize demo data
    demo_data.initialize_demo_data()
    
    # Initialize session state variables if they don't exist
    if 'risk_model' not in st.session_state:
        training_data = generate_sample_training_data()
        st.session_state.risk_model = train_risk_model(training_data)
    
    if 'demo_user' not in st.session_state:
        st.session_state.demo_user = demo_data.get_demo_user()
    
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"
    
    # Sidebar navigation with icons
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/heart-health.png", width=80)
        st.markdown("<h2 style='text-align: center;'>Health Companion</h2>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-nav'>", unsafe_allow_html=True)
        
        # Navigation buttons with icons
        if st.button("📊 Dashboard", key="nav_dashboard", 
                    help="View your health dashboard",
                    use_container_width=True):
            st.session_state.page = "Dashboard"
            
        if st.button("📝 Health Records", key="nav_records",
                    help="Manage your health records",
                    use_container_width=True):
            st.session_state.page = "Health Records"
            
        if st.button("📈 Analytics", key="nav_analytics",
                    help="View health trends and analytics",
                    use_container_width=True):
            st.session_state.page = "Analytics"
            
        if st.button("⚠️ Risk Assessment", key="nav_risk",
                    help="Check your health risk assessment",
                    use_container_width=True):
            st.session_state.page = "Risk Assessment"
            
        if st.button("📋 Doctor Notes", key="nav_notes",
                    help="Analyze doctor notes",
                    use_container_width=True):
            st.session_state.page = "Doctor Notes"
            
        if st.button("🩺 Telehealth", key="nav_telehealth",
                    help="Manage telehealth appointments",
                    use_container_width=True):
            st.session_state.page = "Telehealth"
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # User info at bottom of sidebar
        st.markdown("<hr>", unsafe_allow_html=True)
        user = st.session_state.demo_user
        st.markdown(f"<div style='text-align: center; padding: 10px;'><p>Logged in as<br><b>{user['name']}</b></p></div>", unsafe_allow_html=True)
    
    # Add a top navigation bar for mobile view
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<h1 class='main-header'>Smart Health Companion</h1>", unsafe_allow_html=True)
    
    # Display selected page based on session state
    if st.session_state.page == "Dashboard":
        show_dashboard()
    elif st.session_state.page == "Health Records":
        show_health_records()
    elif st.session_state.page == "Analytics":
        show_analytics()
    elif st.session_state.page == "Risk Assessment":
        show_risk_assessment()
    elif st.session_state.page == "Doctor Notes":
        show_doctor_notes()
    elif st.session_state.page == "Telehealth":
        show_telehealth()

def show_dashboard():
    # User profile section
    user = st.session_state.demo_user
    
    st.markdown(
        f"""
        <div class="user-profile">
            <h2>Welcome, {user['name']}!</h2>
            <p>Age: {user['age']} | Height: {user['height']} cm | Weight: {user['weight']} kg</p>
            <p style="font-size: 0.9rem;margin-top:10px;">Last checkup: {(datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Get current wearable data
    wearable_data = demo_data.get_latest_wearable_data()
    
    # Today's Health Summary section
    st.markdown("<h2 class='section-header'>Today's Health Summary</h2>", unsafe_allow_html=True)
    
    # Health metrics in a grid of cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        heart_rate = wearable_data['heart_rate']
        status = "Normal" if 60 <= heart_rate <= 100 else "Abnormal"
        status_class = "status-healthy" if status == "Normal" else "status-alert"
        
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin-top:0;font-size:1rem;color:#666;">Heart Rate</h3>
            <p style="font-size:1.8rem;font-weight:bold;margin:0;">{heart_rate} <span style="font-size:1rem;font-weight:normal;">bpm</span></p>
            <p class="{status_class}" style="margin-bottom:0;">{status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        bp = wearable_data['blood_pressure']
        systolic, diastolic = map(int, bp.split('/'))
        
        if systolic < 120 and diastolic < 80:
            status = "Normal"
            status_class = "status-healthy"
        elif (120 <= systolic <= 129) and diastolic < 80:
            status = "Elevated"
            status_class = "status-caution"
        else:
            status = "High"
            status_class = "status-alert"
            
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin-top:0;font-size:1rem;color:#666;">Blood Pressure</h3>
            <p style="font-size:1.8rem;font-weight:bold;margin:0;">{bp} <span style="font-size:1rem;font-weight:normal;">mmHg</span></p>
            <p class="{status_class}" style="margin-bottom:0;">{status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        steps = wearable_data['steps']
        status = "Active" if steps >= 7500 else "Needs Improvement"
        status_class = "status-healthy" if status == "Active" else "status-caution"
        
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin-top:0;font-size:1rem;color:#666;">Steps Today</h3>
            <p style="font-size:1.8rem;font-weight:bold;margin:0;">{steps}</p>
            <p class="{status_class}" style="margin-bottom:0;">{status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row of metrics
    col1, col2 = st.columns(2)
    
    with col1:
        calories = wearable_data['calories_burned']
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin-top:0;font-size:1rem;color:#666;">Calories Burned</h3>
            <p style="font-size:1.8rem;font-weight:bold;margin:0;">{calories} <span style="font-size:1rem;font-weight:normal;">cal</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        sleep = wearable_data['sleep_hours']
        status = "Sufficient" if sleep >= 7 else "Insufficient"
        status_class = "status-healthy" if status == "Sufficient" else "status-caution"
        
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin-top:0;font-size:1rem;color:#666;">Sleep Duration</h3>
            <p style="font-size:1.8rem;font-weight:bold;margin:0;">{sleep} <span style="font-size:1rem;font-weight:normal;">hours</span></p>
            <p class="{status_class}" style="margin-bottom:0;">{status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Health Recommendations
    st.markdown("<h2 class='section-header'>Personalized Recommendations</h2>", unsafe_allow_html=True)
    recommendations = generate_health_recommendations(wearable_data)
    
    for i, rec in enumerate(recommendations[:3]):  # Limit to 3 recommendations
        st.markdown(f"""
        <div style="background-color:white;padding:15px;border-radius:10px;margin-bottom:10px;border-left:4px solid #3366ff;box-shadow:0 2px 5px rgba(0,0,0,0.05);">
            <p style="margin:0;">{rec}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if len(recommendations) > 3:
        with st.expander("Show more recommendations"):
            for rec in recommendations[3:]:
                st.info(rec)
    
    # Recent Health Records
    st.markdown("<h2 class='section-header'>Recent Health Records</h2>", unsafe_allow_html=True)
    
    records = get_all_records()
    
    if records:
        # Convert to DataFrame for better display
        df = pd.DataFrame(records)
        # Sort by timestamp if available
        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp', ascending=False)
        
        # Select only the most recent 5 records
        recent_records = df.head(5)
        
        # Create a more mobile-friendly view of records
        for i, record in recent_records.iterrows():
            date = record.get('date', '')
            bp = record.get('blood_pressure', '')
            hr = record.get('heart_rate', '')
            notes = record.get('notes', '')
            
            st.markdown(f"""
            <div style="background-color:white;padding:15px;border-radius:10px;margin-bottom:10px;box-shadow:0 2px 5px rgba(0,0,0,0.05);">
                <div style="display:flex;justify-content:space-between;">
                    <h3 style="margin:0;font-size:1.1rem;">{date}</h3>
                    <span style="color:#666;">#{record.get('record_id', '')}</span>
                </div>
                <div style="display:flex;gap:15px;margin-top:10px;flex-wrap:wrap;">
                    <div>
                        <span style="color:#666;font-size:0.9rem;">BP:</span> 
                        <span style="font-weight:bold;">{bp}</span>
                    </div>
                    <div>
                        <span style="color:#666;font-size:0.9rem;">HR:</span> 
                        <span style="font-weight:bold;">{hr} bpm</span>
                    </div>
                </div>
                {f'<p style="margin-top:10px;margin-bottom:0;font-style:italic;">{notes}</p>' if notes else ''}
            </div>
            """, unsafe_allow_html=True)
        
        if len(df) > 5:
            st.markdown(f'<div style="text-align:center;"><a href="#" style="color:#3366ff;">View all {len(df)} records</a></div>', unsafe_allow_html=True)
    else:
        st.info("No health records found. Add some in the Health Records section.")
    
    # File Upload Section
    show_file_upload_section()

def show_health_records():
    st.markdown("<h1 class='main-header'>Health Records Management</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Add Record", "View Records", "Update Record"])
    
    with tab1:
        st.markdown("<h2 class='section-header'>Add New Health Record</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            record_date = st.date_input("Record Date", datetime.now())
            blood_pressure_systolic = st.number_input("Systolic Blood Pressure", min_value=70, max_value=200, value=120)
            blood_pressure_diastolic = st.number_input("Diastolic Blood Pressure", min_value=40, max_value=120, value=80)
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=72)
        
        with col2:
            blood_sugar = st.number_input("Blood Sugar (mg/dL)", min_value=70, max_value=300, value=100)
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
            temperature = st.number_input("Body Temperature (°C)", min_value=35.0, max_value=42.0, value=36.6, step=0.1)
        
        notes = st.text_area("Medical Notes", height=100)
        
        # Prepare the record data
        record_data = {
            "date": record_date.strftime("%Y-%m-%d"),
            "blood_pressure": f"{blood_pressure_systolic}/{blood_pressure_diastolic}",
            "blood_pressure_systolic": blood_pressure_systolic,
            "blood_pressure_diastolic": blood_pressure_diastolic,
            "heart_rate": heart_rate,
            "blood_sugar": blood_sugar,
            "weight": weight,
            "temperature": temperature,
            "notes": notes
        }
        
        if st.button("Add Health Record"):
            response = add_health_record(record_data)
            st.success(response)
            
            # Log the addition to our blockchain
            log_entry = log_record_update(len(get_all_records()), {"action": "add", "data": record_data})
            st.info(f"Record logged with hash: {log_entry['hash'][:10]}...")
    
    with tab2:
        st.markdown("<h2 class='section-header'>View Health Records</h2>", unsafe_allow_html=True)
        
        records = get_all_records()
        
        if records:
            # Convert to DataFrame
            df = pd.DataFrame(records)
            
            # Handle case where some columns might not exist in all records
            for col in ['blood_pressure', 'heart_rate', 'blood_sugar', 'weight', 'temperature', 'notes']:
                if col not in df.columns:
                    df[col] = None
            
            # Select columns to display
            display_cols = ['record_id', 'date', 'blood_pressure', 'heart_rate', 
                          'blood_sugar', 'weight', 'temperature']
            
            # Filter to columns that actually exist
            display_cols = [col for col in display_cols if col in df.columns]
            
            # Display the records
            st.dataframe(df[display_cols])
            
            # Allow deletion
            record_to_delete = st.number_input("Record ID to delete", min_value=1, 
                                            max_value=max(df['record_id']) if not df.empty else 1, 
                                            step=1)
            
            if st.button("Delete Record"):
                result = delete_health_record(record_to_delete)
                st.info(result)
        else:
            st.info("No health records found.")
    
    with tab3:
        st.markdown("<h2 class='section-header'>Update Health Record</h2>", unsafe_allow_html=True)
        
        records = get_all_records()
        
        if records:
            record_ids = [r.get('record_id') for r in records]
            record_to_update = st.selectbox("Select Record to Update", record_ids)
            
            if record_to_update:
                record = get_health_record(record_to_update)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    blood_pressure_systolic = st.number_input("New Systolic BP", 
                                                           min_value=70, max_value=200, 
                                                           value=record.get('blood_pressure_systolic', 120))
                    blood_pressure_diastolic = st.number_input("New Diastolic BP", 
                                                            min_value=40, max_value=120, 
                                                            value=record.get('blood_pressure_diastolic', 80))
                
                with col2:
                    heart_rate = st.number_input("New Heart Rate", 
                                              min_value=40, max_value=200, 
                                              value=record.get('heart_rate', 72))
                    blood_sugar = st.number_input("New Blood Sugar", 
                                               min_value=70, max_value=300, 
                                               value=record.get('blood_sugar', 100))
                
                notes = st.text_area("Update Notes", value=record.get('notes', ''), height=100)
                
                # Prepare updated data
                updated_data = {
                    "blood_pressure": f"{blood_pressure_systolic}/{blood_pressure_diastolic}",
                    "blood_pressure_systolic": blood_pressure_systolic,
                    "blood_pressure_diastolic": blood_pressure_diastolic,
                    "heart_rate": heart_rate,
                    "blood_sugar": blood_sugar,
                    "notes": notes
                }
                
                if st.button("Update Record"):
                    result = update_health_record(record_to_update, updated_data)
                    st.success(result)
                    
                    # Log the update
                    log_entry = log_record_update(record_to_update, {"action": "update", "data": updated_data})
                    st.info(f"Update logged with hash: {log_entry['hash'][:10]}...")
        else:
            st.info("No health records found. Please add some records first.")

def show_analytics():
    st.markdown("<h1 class='main-header'>Health Analytics</h1>", unsafe_allow_html=True)
    
    # Generate simulated health trends data
    trends = generate_health_trends()
    
    # Display different metrics based on user selection
    metric_option = st.selectbox(
        "Select Health Metric to Visualize",
        ["Blood Pressure (Systolic)", "Blood Pressure (Diastolic)", "Heart Rate", "Blood Sugar", "Steps"]
    )
    
    if metric_option == "Blood Pressure (Systolic)":
        plot_metric(trends["dates"], trends["blood_pressure_systolic"], "Systolic Blood Pressure Trend", "mmHg")
        st.pyplot()
        
        avg_systolic = np.mean(trends["blood_pressure_systolic"])
        st.info(f"Average Systolic Blood Pressure: {avg_systolic:.1f} mmHg")
        
        if avg_systolic > 130:
            st.warning("Your average systolic blood pressure is above the normal range.")
        elif avg_systolic < 90:
            st.warning("Your average systolic blood pressure is below the normal range.")
        else:
            st.success("Your average systolic blood pressure is within the normal range.")
            
    elif metric_option == "Blood Pressure (Diastolic)":
        plot_metric(trends["dates"], trends["blood_pressure_diastolic"], "Diastolic Blood Pressure Trend", "mmHg")
        st.pyplot()
        
        avg_diastolic = np.mean(trends["blood_pressure_diastolic"])
        st.info(f"Average Diastolic Blood Pressure: {avg_diastolic:.1f} mmHg")
        
        if avg_diastolic > 80:
            st.warning("Your average diastolic blood pressure is above the normal range.")
        elif avg_diastolic < 60:
            st.warning("Your average diastolic blood pressure is below the normal range.")
        else:
            st.success("Your average diastolic blood pressure is within the normal range.")
            
    elif metric_option == "Heart Rate":
        plot_metric(trends["dates"], trends["heart_rate"], "Heart Rate Trend", "bpm")
        st.pyplot()
        
        avg_hr = np.mean(trends["heart_rate"])
        st.info(f"Average Heart Rate: {avg_hr:.1f} bpm")
        
        if avg_hr > 100:
            st.warning("Your average heart rate is elevated.")
        elif avg_hr < 60:
            st.warning("Your average heart rate is lower than normal. If you're not an athlete, this might be a concern.")
        else:
            st.success("Your average heart rate is within the normal range.")
            
    elif metric_option == "Blood Sugar":
        plot_metric(trends["dates"], trends["blood_sugar"], "Blood Sugar Trend", "mg/dL")
        st.pyplot()
        
        avg_bs = np.mean(trends["blood_sugar"])
        st.info(f"Average Blood Sugar: {avg_bs:.1f} mg/dL")
        
        if avg_bs > 140:
            st.warning("Your average blood sugar is higher than the optimal range.")
            if avg_bs > 180:
                st.error("Your average blood sugar is significantly elevated. Please consult your healthcare provider.")
        else:
            st.success("Your average blood sugar is within the normal range.")
            
    elif metric_option == "Steps":
        plot_metric(trends["dates"], trends["steps"], "Daily Steps Trend", "steps")
        st.pyplot()
        
        avg_steps = np.mean(trends["steps"])
        st.info(f"Average Daily Steps: {avg_steps:.0f}")
        
        if avg_steps < 5000:
            st.warning("Your average daily steps are below the recommended minimum of 7,500 steps.")
        elif avg_steps > 10000:
            st.success("Great job! You're exceeding the recommended 10,000 steps per day.")
        else:
            st.info("You're meeting the basic activity requirements, but try to aim for 10,000 steps daily.")
    
    # Correlation Analysis
    st.markdown("<h2 class='section-header'>Correlation Analysis</h2>", unsafe_allow_html=True)
    
    st.write("Let's explore relationships between different health metrics:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_metric = st.selectbox(
            "X-axis Metric",
            ["Blood Pressure (Systolic)", "Heart Rate", "Steps", "Blood Sugar"],
        )
    
    with col2:
        y_metric = st.selectbox(
            "Y-axis Metric",
            ["Heart Rate", "Blood Sugar", "Blood Pressure (Systolic)", "Steps"],
            index=1
        )
    
    # Map selection to data
    x_data_map = {
        "Blood Pressure (Systolic)": trends["blood_pressure_systolic"],
        "Heart Rate": trends["heart_rate"],
        "Steps": trends["steps"],
        "Blood Sugar": trends["blood_sugar"]
    }
    
    y_data_map = {
        "Blood Pressure (Systolic)": trends["blood_pressure_systolic"],
        "Heart Rate": trends["heart_rate"],
        "Steps": trends["steps"],
        "Blood Sugar": trends["blood_sugar"]
    }
    
    x_data = x_data_map[x_metric]
    y_data = y_data_map[y_metric]
    
    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(x_data, y_data, alpha=0.7, s=100)
    
    # Add trend line
    z = np.polyfit(x_data, y_data, 1)
    p = np.poly1d(z)
    plt.plot(x_data, p(x_data), "r--", alpha=0.7)
    
    plt.title(f"{x_metric} vs {y_metric}", fontsize=16)
    plt.xlabel(x_metric, fontsize=12)
    plt.ylabel(y_metric, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    st.pyplot()
    
    # Calculate correlation
    correlation = np.corrcoef(x_data, y_data)[0, 1]
    st.info(f"Correlation coefficient: {correlation:.2f}")
    
    if abs(correlation) > 0.7:
        st.write("There appears to be a strong correlation between these metrics.")
    elif abs(correlation) > 0.4:
        st.write("There appears to be a moderate correlation between these metrics.")
    else:
        st.write("There appears to be a weak correlation between these metrics.")

def show_risk_assessment():
    st.markdown("<h1 class='main-header'>Health Risk Assessment</h1>", unsafe_allow_html=True)
    
    st.write("""
    This tool uses a machine learning model to assess potential health risks based on your data.
    Please enter your information below for an assessment.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=45)
        systolic_bp = st.number_input("Systolic Blood Pressure (mmHg)", min_value=80, max_value=200, value=120)
        diastolic_bp = st.number_input("Diastolic Blood Pressure (mmHg)", min_value=40, max_value=120, value=80)
    
    with col2:
        heart_rate = st.number_input("Resting Heart Rate (bpm)", min_value=40, max_value=200, value=72)
        blood_sugar = st.number_input("Blood Sugar (mg/dL)", min_value=70, max_value=300, value=100)
    
    if st.button("Calculate Risk"):
        # Prepare user data for prediction
        user_data = [age, systolic_bp, diastolic_bp, heart_rate, blood_sugar]
        
        # Get prediction from the model
        prediction = predict_risk(st.session_state.risk_model, user_data)
        
        # Display result
        risk_probability = prediction["probability"]
        risk_level = prediction["risk_level"]
        
        # Create a nice visual indicator
        if risk_level == "High":
            st.error(f"Risk Assessment: {risk_level} ({risk_probability}% probability)")
            
            # Send alert if risk is high
            alert_message = "High health risk detected based on your recent data."
            alert_result = send_alert(alert_message, "High")
            st.warning(alert_result)
            
            st.markdown("""
            ### Recommendations:
            1. Schedule an appointment with your healthcare provider soon.
            2. Monitor your blood pressure and blood sugar regularly.
            3. Consider lifestyle modifications such as reducing sodium intake, increasing physical activity, and improving diet.
            """)
        else:
            st.success(f"Risk Assessment: {risk_level} ({risk_probability}% probability)")
            st.markdown("""
            ### Keep up the good work!
            - Continue regular health check-ups
            - Maintain a healthy lifestyle with regular exercise and balanced diet
            - Monitor your vitals periodically
            """)
        
        # Display risk factors
        st.subheader("Key Risk Factors:")
        
        # Create a DataFrame for the risk factors
        risk_data = {
            "Metric": ["Blood Pressure", "Blood Sugar", "Heart Rate", "Age"],
            "Value": [f"{systolic_bp}/{diastolic_bp} mmHg", f"{blood_sugar} mg/dL", f"{heart_rate} bpm", f"{age} years"],
            "Status": ["", "", "", ""]
        }
        
        # Determine status for each metric
        if systolic_bp > 140 or diastolic_bp > 90:
            risk_data["Status"][0] = "⚠️ High"
        elif systolic_bp > 120 or diastolic_bp > 80:
            risk_data["Status"][0] = "⚠️ Elevated"
        else:
            risk_data["Status"][0] = "✅ Normal"
            
        if blood_sugar > 180:
            risk_data["Status"][1] = "⚠️ High"
        elif blood_sugar > 140:
            risk_data["Status"][1] = "⚠️ Elevated"
        else:
            risk_data["Status"][1] = "✅ Normal"
            
        if heart_rate > 100:
            risk_data["Status"][2] = "⚠️ Elevated"
        elif heart_rate < 60:
            risk_data["Status"][2] = "⚠️ Low"
        else:
            risk_data["Status"][2] = "✅ Normal"
            
        if age > 65:
            risk_data["Status"][3] = "⚠️ Increased risk with age"
        else:
            risk_data["Status"][3] = "✅ Not a major factor"
        
        # Display risk factors table
        st.table(pd.DataFrame(risk_data))

def show_doctor_notes():
    st.markdown("<h1 class='main-header'>Doctor Notes Analysis</h1>", unsafe_allow_html=True)
    
    st.write("""
    Use this tool to analyze and summarize doctor notes. You can enter notes from your medical appointments
    and get a concise summary of the key information.
    """)
    
    # Sample doctor notes for quick testing
    sample_notes = """
    Patient presents with complaints of persistent headache for the past 2 weeks. The pain is described as throbbing and primarily located in the frontal region. Patient reports that pain is worse in the morning and improves somewhat during the day. No nausea or vomiting, but patient reports mild sensitivity to bright lights. Patient has been self-medicating with over-the-counter ibuprofen with partial relief. Vital signs are within normal range with BP of 128/84. No focal neurological deficits observed during examination. Patient has a history of occasional migraine headaches but describes current symptoms as different from usual migraine pattern. Diagnosed with tension headache potentially triggered by recent work-related stress. Prescribed acetaminophen 500mg PRN for pain and recommended stress reduction techniques including regular breaks during work. Advised to maintain regular sleep schedule and increase water intake. Follow up in 2 weeks if symptoms persist or worsen. Referral to neurology will be considered if no improvement with current treatment plan.
    """
    
    option = st.radio("Choose an option:", ["Enter My Own Notes", "Use Sample Notes"])
    
    if option == "Enter My Own Notes":
        doctor_notes = st.text_area("Enter doctor notes here:", height=200)
    else:
        doctor_notes = st.text_area("Sample doctor notes:", sample_notes, height=200)
    
    if st.button("Analyze Notes"):
        if doctor_notes:
            # Get summary
            summary = simple_summarize(doctor_notes)
            
            # Extract key information
            key_info = extract_key_info(doctor_notes)
            
            # Display summary
            st.markdown("<h2 class='section-header'>Summary</h2>", unsafe_allow_html=True)
            st.info(summary)
            
            # Display key information
            st.markdown("<h2 class='section-header'>Key Information</h2>", unsafe_allow_html=True)
            
            # Diagnosis
            st.subheader("Diagnosis")
            if key_info["diagnosis"]:
                for item in key_info["diagnosis"]:
                    st.write("• " + item)
            else:
                st.write("No clear diagnosis information found.")
            
            # Medication
            st.subheader("Medication")
            if key_info["medication"]:
                for item in key_info["medication"]:
                    st.write("• " + item)
            else:
                st.write("No medication information found.")
            
            # Follow-up
            st.subheader("Follow-up Instructions")
            if key_info["follow_up"]:
                for item in key_info["follow_up"]:
                    st.write("• " + item)
            else:
                st.write("No follow-up information found.")
            
            # Recommendations based on the notes
            st.markdown("<h2 class='section-header'>Recommendations</h2>", unsafe_allow_html=True)
            
            # Simple logic to generate recommendations
            if any("headache" in item.lower() for item in key_info["diagnosis"]):
                st.info("• Consider tracking headache patterns with a journal to identify triggers.")
                st.info("• Ensure you're staying hydrated and getting adequate rest.")
            
            if any("stress" in note.lower() for note in doctor_notes.split()):
                st.info("• Look into stress management techniques such as meditation or deep breathing exercises.")
                st.info("• Consider regular physical activity to help reduce stress levels.")
            
            if any("sleep" in note.lower() for note in doctor_notes.split()):
                st.info("• Maintain a consistent sleep schedule, even on weekends.")
                st.info("• Create a relaxing bedtime routine to improve sleep quality.")
        else:
            st.error("Please enter some notes to analyze.")

def show_telehealth():
    st.markdown("<h1 class='main-header'>Telehealth Appointments</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Schedule Appointment", "View Appointments"])
    
    with tab1:
        st.markdown("<h2 class='section-header'>Schedule New Telehealth Consultation</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name", "")
            appointment_date = st.date_input("Appointment Date", datetime.now() + timedelta(days=1))
        
        with col2:
            doctor_options = [
                "Dr. Smith (Cardiology)",
                "Dr. Johnson (Internal Medicine)",
                "Dr. Williams (Endocrinology)",
                "Dr. Davis (Neurology)"
            ]
            doctor_name = st.selectbox("Select Doctor", doctor_options)
            appointment_time = st.time_input("Appointment Time", datetime.now().time().replace(hour=9, minute=0, second=0))
        
        reason = st.text_area("Reason for Consultation", height=100)
        
        if st.button("Schedule Appointment"):
            if patient_name and doctor_name:
                # Combine date and time into a datetime object
                consultation_datetime = datetime.combine(appointment_date, appointment_time)
                
                # Schedule the appointment
                appointment = schedule_telehealth_consultation(
                    patient_name, 
                    doctor_name, 
                    consultation_datetime
                )
                
                st.success(f"Appointment scheduled successfully! Appointment ID: {appointment['appointment_id']}")
                st.json(appointment)
            else:
                st.error("Please fill out all required fields.")
    
    with tab2:
        st.markdown("<h2 class='section-header'>Upcoming Appointments</h2>", unsafe_allow_html=True)
        
        # Get upcoming consultations
        appointments = get_upcoming_consultations()
        
        if appointments:
            # Convert to DataFrame for better display
            df = pd.DataFrame(appointments)
            
            # Format date/time for display
            try:
                df['consultation_time'] = pd.to_datetime(df['consultation_time']).dt.strftime('%Y-%m-%d %H:%M')
            except:
                pass  # Handle if format conversion fails
            
            # Display the appointments
            st.dataframe(df)
            
            # Allow cancelling appointments
            st.markdown("<h3>Cancel Appointment</h3>", unsafe_allow_html=True)
            
            appointment_to_cancel = st.selectbox(
                "Select appointment to cancel",
                [(f"ID: {appt['appointment_id']} - {appt['doctor']} - {appt['consultation_time']}") for appt in appointments]
            )
            
            if st.button("Cancel Selected Appointment"):
                # Extract appointment ID from the selection
                appt_id = int(appointment_to_cancel.split(" - ")[0].replace("ID: ", ""))
                
                # Cancel the appointment
                result = cancel_consultation(appt_id)
                st.success(result)
                
                # Refresh the list
                st.experimental_rerun()
        else:
            st.info("No upcoming appointments found.")
            
        # Add a section for creating a mock meeting link (simulation)
        st.markdown("<h2 class='section-header'>Join Telehealth Meeting</h2>", unsafe_allow_html=True)
        
        if appointments:
            meeting_id = st.selectbox(
                "Select appointment to join",
                [(f"ID: {appt['appointment_id']} - {appt['doctor']} - {appt['consultation_time']}") for appt in appointments]
            )
            
            if st.button("Generate Meeting Link"):
                # This is a simulation - in a real app, this would generate an actual meeting link
                st.success("Meeting link generated successfully!")
                meeting_link = f"https://telehealth.example.com/meeting/{meeting_id.split(' - ')[0].replace('ID: ', '')}"
                st.code(meeting_link)
                
                st.info("Note: This is a simulated meeting link. In a real application, this would connect to a video conferencing service.")
        else:
            st.info("No upcoming appointments available for telehealth meetings.")

def show_file_upload_section():
    st.markdown("<h2 class='section-header'>Upload Health Document</h2>", unsafe_allow_html=True)
    
    # Add tab for template downloads
    upload_tab, template_tab = st.tabs(["Upload Files", "Download Templates"])
    
    with upload_tab:
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg", "csv", "txt"])
        
        if uploaded_file:
            message = upload_health_data(uploaded_file)
            st.success(message)
        
        # Show existing uploads
        if os.path.exists("uploads"):
            files = os.listdir("uploads")
            if files:
                st.markdown("### Your Documents")
                file_df = pd.DataFrame({
                    "Filename": files,
                    "Type": [f.split('.')[-1].upper() for f in files],
                    "Uploaded Date": [datetime.fromtimestamp(os.path.getctime(os.path.join("uploads", f))).strftime("%Y-%m-%d") for f in files]
                })
                st.dataframe(file_df)
    
    with template_tab:
        st.markdown("### Available Templates")
        st.markdown("""
        Download these templates to help you format your health data correctly:
        * **Blood Test Results Template** - For organizing lab test results
        * **Health Tracking Template** - For daily health metrics tracking
        """)
        
        if os.path.exists("templates/blood_test_template.csv"):
            blood_test_df = pd.read_csv("templates/blood_test_template.csv")
            st.download_button(
                label="Download Blood Test Template",
                data=blood_test_df.to_csv(index=False),
                file_name="blood_test_template.csv",
                mime="text/csv"
            )
        
        if os.path.exists("templates/health_tracking_template.csv"):
            health_tracking_df = pd.read_csv("templates/health_tracking_template.csv")
            st.download_button(
                label="Download Health Tracking Template",
                data=health_tracking_df.to_csv(index=False),
                file_name="health_tracking_template.csv",
                mime="text/csv"
            )
        
        st.info("Tip: Fill the templates with your data and upload them to keep track of your health information.")

if __name__ == "__main__":
    main() 