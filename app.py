import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns
import time
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix
import datetime
from fpdf import FPDF

# -------------------------------
# PDF Diagnostic Report Exporter
def generate_pdf_report(patient_name, prediction, confidence, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age):
    pdf = FPDF()
    pdf.add_page()
    
    # Header styling
    pdf.set_fill_color(14, 165, 233)  # Sky blue banner
    pdf.rect(0, 0, 210, 20, "F")
    
    pdf.ln(18)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(12, 74, 110)  # Dark teal
    pdf.cell(0, 10, "DIABETES HEALTH SCREENING REPORT", ln=True, align="C")
    pdf.ln(5)
    
    # Session Details
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 116, 139)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 5, f"Report Date: {current_time}", ln=True, align="R")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 5, f"Patient Name / Identifier: {patient_name}", ln=True, align="L")
    pdf.ln(4)
    
    # Divider line
    pdf.set_draw_color(226, 232, 240)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Diagnosis Card Block
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Diagnostic Assessment Summary", ln=True)
    pdf.ln(2)
    
    if prediction == 1:
        status_text = "HIGH RISK (Positive Diabetic Screening)"
        bg_r, bg_g, bg_b = 254, 242, 242
        text_r, text_g, text_b = 239, 68, 68
    else:
        status_text = "LOW RISK (Negative/Normal Diabetic Screening)"
        bg_r, bg_g, bg_b = 240, 253, 244
        text_r, text_g, text_b = 16, 185, 129
        
    pdf.set_fill_color(bg_r, bg_g, bg_b)
    pdf.set_text_color(text_r, text_g, text_b)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 10, f"  Status: {status_text}", ln=True, fill=True)
    pdf.ln(2)
    
    pdf.set_text_color(30, 41, 59)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Logistic Model Prediction Confidence: {confidence:.2f}%", ln=True)
    pdf.ln(5)
    
    # Grid of metabolic markers
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Patient Metabolic Profile Metrics", ln=True)
    pdf.ln(2)
    
    # Table header
    pdf.set_fill_color(241, 245, 249)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(95, 7, "  Metabolic Parameter", border=1, fill=True)
    pdf.cell(95, 7, "  Value", border=1, ln=True, fill=True)
    
    pdf.set_font("Helvetica", "", 10)
    metrics = [
        ("Pregnancies (Count)", f"{pregnancies}"),
        ("Plasma Glucose Concentration (mg/dL)", f"{glucose} mg/dL"),
        ("Diastolic Blood Pressure (mmHg)", f"{blood_pressure} mmHg"),
        ("Triceps Skin Fold Thickness (mm)", f"{skin_thickness if skin_thickness is not None else 'N/A'}"),
        ("Serum Insulin 2-Hour (mu U/ml)", f"{insulin if insulin is not None else 'N/A'}"),
        ("Body Mass Index (BMI)", f"{bmi:.1f}"),
        ("Diabetes Pedigree Function (DPF)", f"{diabetes_pedigree_function if diabetes_pedigree_function is not None else 'N/A'}"),
        ("Patient Age (Years)", f"{age} yrs")
    ]
    
    for label, val in metrics:
        pdf.cell(95, 7, f"  {label}", border=1)
        pdf.cell(95, 7, f"  {val}", border=1, ln=True)
        
    pdf.ln(6)
    
    # Recommendations
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Recommended Preventive Actions / Guidelines:", ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    
    if prediction == 1:
        recs = [
            "- Schedule diagnostic clinical verification & oral glucose tests.",
            "- Self-monitor blood sugar levels (pre & post-prandial glycemic logbooks).",
            "- Shift to a high-fiber, low glycemic index whole-food diet.",
            "- Conduct 150 minutes of weekly moderate cardiovascular exercise mapping."
        ]
    else:
        recs = [
            "- Maintain clean whole-food meals, targeting low refined sugar/carbs.",
            "- Structure 7-8 hours of circadian sleep cycles.",
            "- Ensure 2.5L-3.0L oral water hydration daily.",
            "- Stay active with daily step milestones and physical movements."
        ]
        
    for rec in recs:
        pdf.cell(0, 5, rec, ln=True)
        
    pdf.ln(12)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 5, "CONFIDENTIALITY NOTICE: This screening serves as a decision support aid, and is not a clinical replacement.", ln=True, align="C")
    
    return bytes(pdf.output())

# -------------------------------
# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme selection
# Initialize session states for user preferences and history
if "theme" not in st.session_state:
    st.session_state.theme = "Clean Medical Blue"

# Determine theme mode dynamically based on the active theme
if st.session_state.theme == "Cyber Clinic (Dark)":
    st.session_state.theme_mode = "🌙 Dark Mode"
else:
    st.session_state.theme_mode = "☀️ Light Mode"

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# Dynamic theme styling injection
def inject_theme_styles():
    preset = st.session_state.theme
    mode = st.session_state.theme_mode
    
    # 1. Base Variables based on MODE (Light / Dark)
    if mode == "🌙 Dark Mode":
        mode_css = f"""
        :root {{
            --bg-primary: #080c14;
            --bg-secondary: #0c111e;
            --bg-tertiary: #121826;
            --text-color: #94a3b8;
            --heading-color: #f8fafc;
            --border-color: rgba(255, 255, 255, 0.08);
            --sidebar-bg-color: #05070c;
            --sidebar-btn-bg: rgba(255, 255, 255, 0.03);
            --sidebar-btn-hover: rgba(255, 255, 255, 0.08);
            --body-bg-gradient: radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.12) 0%, #05070c 80%), radial-gradient(circle at 90% 80%, rgba(37, 99, 235, 0.1) 0%, #05070c 85%);
            --card-bg: rgba(13, 20, 36, 0.55);
            --card-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
            --input-bg-color: rgba(13, 20, 36, 0.7);
            --input-border-color: rgba(255, 255, 255, 0.08);
            --input-text-color: #f1f5f9;
            --divider-color: rgba(255, 255, 255, 0.08);
            --metric-bg: rgba(255, 255, 255, 0.02);
            --glow-color: rgba(14, 165, 233, 0.15);
        }}
        .stApp {{
            color: var(--text-color) !important;
        }}
        h1, h2, h3, h4, h5, h6, label {{
            color: var(--heading-color) !important;
        }}
        .stNumberInput input {{
            background-color: var(--input-bg-color) !important;
            border: 1px solid var(--input-border-color) !important;
            color: var(--input-text-color) !important;
        }}
        .footer {{
            border-top: 1px solid var(--divider-color) !important;
            color: #64748b !important;
        }}
        """
    else:  # Light Mode
        mode_css = f"""
        :root {{
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-tertiary: #f1f5f9;
            --text-color: #475569;
            --heading-color: #0f172a;
            --border-color: rgba(15, 23, 42, 0.06);
            --sidebar-bg-color: {"rgba(240, 253, 244, 0.65)" if preset == "Emerald Health" else "rgba(255, 245, 245, 0.65)" if preset == "Crimson Alert" else "rgba(240, 247, 255, 0.65)"};
            --sidebar-btn-bg: rgba(255, 255, 255, 0.65);
            --sidebar-btn-hover: #ffffff;
            --body-bg-gradient: {
                "radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.05) 0%, #f8fafc 90%)" if preset == "Emerald Health"
                else "radial-gradient(circle at 10% 20%, rgba(244, 63, 94, 0.05) 0%, #f8fafc 90%)" if preset == "Crimson Alert"
                else "radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.05) 0%, #f8fafc 90%)"
            };
            --card-bg: rgba(255, 255, 255, 0.7);
            --card-shadow: 0 20px 40px rgba(15, 23, 42, 0.03);
            --input-bg-color: rgba(255, 255, 255, 0.8);
            --input-border-color: rgba(15, 23, 42, 0.08);
            --input-text-color: #0f172a;
            --divider-color: rgba(15, 23, 42, 0.06);
            --metric-bg: rgba(255, 255, 255, 0.5);
            --glow-color: rgba(37, 99, 235, 0.05);
        }}
        """

    # 2. Preset Accents overrides
    if preset == "Emerald Health":
        accent_css = """
        :root {
            --primary-color: #10b981;
            --secondary-color: #059669;
            --nav-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
            --nav-gradient-hover: linear-gradient(135deg, #34d399 0%, #10b981 100%);
            --nav-glow: rgba(16, 185, 129, 0.15);
        }
        """
    elif preset == "Crimson Alert":
        accent_css = """
        :root {
            --primary-color: #f43f5e;
            --secondary-color: #dc2626;
            --nav-gradient: linear-gradient(135deg, #f43f5e 0%, #dc2626 100%);
            --nav-gradient-hover: linear-gradient(135deg, #fb7185 0%, #f43f5e 100%);
            --nav-glow: rgba(244, 63, 94, 0.15);
        }
        """
    else:  # Clean Medical Blue (default)
        accent_css = """
        :root {
            --primary-color: #0ea5e9;
            --secondary-color: #2563eb;
            --nav-gradient: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
            --nav-gradient-hover: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
            --nav-glow: rgba(37, 99, 235, 0.15);
        }
        """
    st.markdown(f"<style>{mode_css}\n{accent_css}</style>", unsafe_allow_html=True)

# Run style injection
inject_theme_styles()

custom_styles = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

    /* Page Fade-in Animation */
    @keyframes fadeInPage {
        from {
            opacity: 0;
            filter: blur(8px);
        }
        to {
            opacity: 1;
            filter: blur(0);
        }
    }

    .stApp {
        background: var(--body-bg-gradient) !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--text-color) !important;
        animation: fadeInPage 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Webkit Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.05);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(14, 165, 233, 0.2);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(14, 165, 233, 0.4);
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1050px !important;
    }

    h1 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        color: var(--heading-color) !important;
        text-align: center !important;
        margin-bottom: 0.3rem !important;
        font-size: 2.75rem !important;
        border: none !important;
        padding: 0 !important;
        letter-spacing: -0.5px !important;
    }

    .subtitle {
        text-align: center;
        color: var(--primary-color) !important;
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 2.2rem;
        letter-spacing: 0.5px;
    }

    /* Input card container (custom key) with smooth hover and scale transitions */
    div[class*="st-key-input_card"] {
        background: var(--card-bg) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 20px !important;
        padding: 2.2rem !important;
        box-shadow: var(--card-shadow) !important;
        margin-bottom: 2rem !important;
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease, border-color 0.4s ease !important;
    }

    div[class*="st-key-input_card"]:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(14, 165, 233, 0.25) !important;
        box-shadow: var(--card-shadow), 0 20px 40px var(--glow-color) !important;
    }

    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg-color) !important;
        border-right: 1px solid var(--border-color) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
    }

    /* Target headers in sidebar */
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h1 {
        font-family: 'Outfit', sans-serif !important;
        color: var(--heading-color) !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }

    .stNumberInput label, .stSlider label {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        color: var(--text-color) !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.4rem !important;
    }

    .stNumberInput input {
        border-radius: 12px !important;
        border: 1px solid var(--input-border-color) !important;
        background-color: var(--input-bg-color) !important;
        padding: 0.5rem 0.75rem !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--input-text-color) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .stNumberInput input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px var(--glow-color) !important;
        outline: none !important;
    }

    /* Slider styling custom with hover animations */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: var(--primary-color) !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
        transition: transform 0.2s ease, background-color 0.2s ease !important;
    }
    
    div[data-testid="stSlider"] div[role="slider"]:hover {
        transform: scale(1.2) !important;
    }
    
    div[data-testid="stSlider"] div[data-testid="stSliderTrack"] > div {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)) !important;
    }

    /* Button Animations and Transitions */
    .stButton > button {
        background: var(--nav-gradient) !important;
        color: white !important;
        border: none !important;
        padding: 0.9rem 2.2rem !important;
        border-radius: 30px !important;
        font-weight: 650 !important;
        font-family: 'Outfit', sans-serif !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        width: 100% !important;
        margin-top: 1rem !important;
        letter-spacing: 0.5px !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.35), 0 0 0 3px var(--glow-color) !important;
        background: var(--nav-gradient-hover) !important;
    }

    .stButton > button:active {
        transform: translateY(1px) scale(0.99) !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2) !important;
    }

    /* Tab controls overrides */
    div[data-testid="stTabBar"] {
        background: transparent !important;
        border-bottom: 2px solid var(--border-color) !important;
        gap: 8px !important;
    }

    div[data-testid="stTabBar"] button {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        color: var(--text-color) !important;
        background: transparent !important;
        border: none !important;
        padding: 0.6rem 1.25rem !important;
        border-radius: 8px 8px 0 0 !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stTabBar"] button:hover {
        color: var(--primary-color) !important;
        background: rgba(14, 165, 233, 0.05) !important;
    }

    div[data-testid="stTabBar"] button[aria-selected="true"] {
        color: var(--primary-color) !important;
        border-bottom: 2px solid var(--primary-color) !important;
        font-weight: 700 !important;
        background: var(--glow-color) !important;
    }

    /* Expander overrides */
    div[data-testid="stExpander"] {
        background: var(--card-bg) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        box-shadow: var(--card-shadow) !important;
        margin-bottom: 1.2rem !important;
        overflow: hidden !important;
    }
    
    div[data-testid="stExpander"] details summary {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 650 !important;
        color: var(--heading-color) !important;
        padding: 1rem 1.2rem !important;
        font-size: 1.05rem !important;
        transition: background 0.3s ease !important;
    }

    div[data-testid="stExpander"] details summary:hover {
        background: rgba(14, 165, 233, 0.05) !important;
    }

    /* Metric overrides */
    div[data-testid="metric-container"] {
        background: var(--card-bg) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        box-shadow: var(--card-shadow) !important;
        transition: all 0.35s ease !important;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px) !important;
        border-color: rgba(14, 165, 233, 0.2) !important;
        box-shadow: var(--card-shadow), 0 10px 20px var(--glow-color) !important;
    }

    div[data-testid="stMetricVal"] {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.85rem !important;
        font-weight: 750 !important;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }

    .footer {
        text-align: center;
        padding: 2.2rem 0;
        margin-top: 3.5rem;
        border-top: 1px solid var(--divider-color);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        opacity: 0.8;
    }

    .footer strong {
        color: var(--primary-color);
    }
    
    /* Responsive overrides */
    @media (max-width: 600px) {
        .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 1rem !important;
        }
        div[class*="st-key-input_card"] {
            padding: 1.25rem !important;
            border-radius: 14px !important;
        }
        .medical-grid {
            grid-template-columns: 1fr !important;
            gap: 12px !important;
        }
        .medical-card-header {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 10px !important;
        }
        h1 {
            font-size: 2rem !important;
        }
        .subtitle {
            font-size: 0.95rem !important;
            margin-bottom: 1.5rem !important;
        }
        .medical-card {
            padding: 1.25rem !important;
            border-radius: 14px !important;
        }
    }

    /* Success / Error Card Spring Pop and Pulse Animations */
    @keyframes springPop {
        0% {
            transform: scale(0.92) translateY(15px);
            opacity: 0;
        }
        70% {
            transform: scale(1.02) translateY(-2px);
            opacity: 0.9;
        }
        100% {
            transform: scale(1) translateY(0);
            opacity: 1;
        }
    }

    @keyframes pulseBorderSuccess {
        0% { border-color: rgba(16, 185, 129, 0.4); box-shadow: 0 10px 25px rgba(16, 185, 129, 0.04); }
        50% { border-color: rgba(16, 185, 129, 0.8); box-shadow: 0 12px 30px rgba(16, 185, 129, 0.12); transform: translateY(-1px); }
        100% { border-color: rgba(16, 185, 129, 0.4); box-shadow: 0 10px 25px rgba(16, 185, 129, 0.04); }
    }

    @keyframes pulseBorderError {
        0% { border-color: rgba(239, 68, 68, 0.4); box-shadow: 0 10px 25px rgba(239, 68, 68, 0.04); }
        50% { border-color: rgba(239, 68, 68, 0.8); box-shadow: 0 12px 30px rgba(239, 68, 68, 0.12); transform: translateY(-1px); }
        100% { border-color: rgba(239, 68, 68, 0.4); box-shadow: 0 10px 25px rgba(239, 68, 68, 0.04); }
    }

    .result-card {
        border-radius: 16px;
        padding: 1.75rem;
        margin-top: 1.5rem;
        text-align: center;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .diabetic-card {
        background: rgba(254, 242, 242, 0.92) !important;
        border: 2px solid #fee2e2 !important;
        border-left: 6px solid #ef4444 !important;
        animation: springPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards, pulseBorderError 3.5s infinite ease-in-out !important;
    }

    .healthy-card {
        background: rgba(240, 253, 250, 0.92) !important;
        border: 2px solid #ccfbf1 !important;
        border-left: 6px solid #14b8a6 !important;
        animation: springPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards, pulseBorderSuccess 3.5s infinite ease-in-out !important;
    }

    .result-header {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.4rem !important;
    }

    .diabetic-header {
        color: #b91c1c !important;
    }

    .healthy-header {
        color: #0f766e !important;
    }

    .result-probability {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
        margin-bottom: 0.75rem !important;
    }

    /* Styled indicators with transitions */
    .indicator-box {
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 8px;
        display: inline-block;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    .indicator-green {
        background-color: rgba(209, 250, 229, 0.4) !important;
        color: #047857 !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-left: 4px solid #10b981 !important;
    }
    .indicator-orange {
        background-color: rgba(254, 237, 222, 0.4) !important;
        color: #c2410c !important;
        border: 1px solid rgba(249, 115, 22, 0.2) !important;
        border-left: 4px solid #f97316 !important;
    }
    .indicator-red {
        background-color: rgba(254, 226, 226, 0.4) !important;
        color: #b91c1c !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
        border-left: 4px solid #ef4444 !important;
    }
    .indicator-blue {
        background-color: rgba(240, 249, 255, 0.4) !important;
        color: #0369a1 !important;
        border: 1px solid rgba(14, 165, 233, 0.2) !important;
        border-left: 4px solid #0ea5e9 !important;

    /* Professional Medical Report Card Styling */
    .medical-card {
        border-radius: 24px;
        padding: 2.2rem;
        margin: 2rem auto;
        max-width: 650px;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        font-family: 'Inter', sans-serif;
        text-align: left !important;
        animation: springPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    
    .medical-card-diabetic {
        background: rgba(239, 68, 68, 0.05) !important;
        border: 1px solid rgba(239, 68, 68, 0.25) !important;
        border-top: 8px solid #ef4444 !important;
        box-shadow: var(--card-shadow), 0 10px 30px rgba(239, 68, 68, 0.08) !important;
    }
    
    .medical-card-healthy {
        background: rgba(16, 185, 129, 0.05) !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-top: 8px solid #10b981 !important;
        box-shadow: var(--card-shadow), 0 10px 30px rgba(16, 185, 129, 0.08) !important;
    }

    .medical-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
        gap: 10px;
    }

    .medical-card-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.55rem;
        font-weight: 800;
        color: var(--heading-color) !important;
        margin: 0 !important;
        letter-spacing: -0.5px !important;
    }

    .medical-badge {
        padding: 8px 18px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 750;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 6px;
        line-height: 1 !important;
        letter-spacing: 0.5px;
    }

    .medical-badge-high {
        background-color: rgba(239, 68, 68, 0.15) !important;
        color: #ef4444 !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
    }

    .medical-badge-low {
        background-color: rgba(16, 185, 129, 0.15) !important;
        color: #10b981 !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
    }

    .confidence-container {
        background: var(--input-bg-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 14px;
        padding: 1.1rem;
        margin-bottom: 1.5rem;
    }

    .confidence-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }

    .confidence-percentage {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.2rem;
        font-weight: 850;
    }
    
    .confidence-percentage-high {
        color: #ef4444;
    }

    .confidence-percentage-low {
        color: #10b981;
    }

    .confidence-bar-bg {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        height: 10px;
        width: 100%;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }

    .confidence-bar-fill {
        height: 100%;
        border-radius: 10px;
    }

    .confidence-bar-fill-high {
        background: linear-gradient(90deg, #f87171, #ef4444);
    }

    .confidence-bar-fill-low {
        background: linear-gradient(90deg, #34d399, #10b981);
    }

    .medical-card-divider {
        height: 1px;
        background-color: var(--border-color);
        margin: 1.5rem 0;
    }

    .medical-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 12px;
        margin-bottom: 1.5rem;
    }

    .medical-grid-item {
        background: var(--input-bg-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 14px;
        padding: 0.85rem;
        text-align: center;
        transition: transform 0.3s ease !important;
    }

    .medical-grid-item:hover {
        transform: translateY(-2px);
    }

    .medical-grid-label {
        font-size: 0.75rem;
        color: var(--text-color);
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 4px;
        letter-spacing: 0.5px;
        opacity: 0.8;
    }

    .medical-grid-value {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.05rem;
        font-weight: 750;
        color: var(--heading-color) !important;
    }

    .medical-tips-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.2rem;
        font-weight: 750;
        color: var(--heading-color) !important;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .medical-tips-list {
        list-style: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .medical-tips-item {
        font-size: 0.92rem;
        line-height: 1.6;
        color: var(--text-color) !important;
        margin-bottom: 10px;
        padding-left: 26px;
        position: relative;
    }

    .medical-tips-item::before {
        content: "■";
        position: absolute;
        left: 8px;
        top: 2px;
        font-size: 0.75rem;
    }

    .medical-tips-item-high::before {
        color: #ef4444;
    }

    .medical-tips-item-low::before {
        color: #10b981;
    }

    /* Sidebar CUSTOM radio navigation button cards styling */
    [data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 12px !important;
        padding: 15px 0 !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: var(--sidebar-btn-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 14px !important;
        padding: 0.8rem 1.2rem !important;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        cursor: pointer !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        color: var(--text-color) !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02) !important;
        display: flex !important;
        align-items: center !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background: var(--nav-gradient) !important;
        color: #ffffff !important;
        border-color: transparent !important;
        box-shadow: 0 8px 20px var(--nav-glow) !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] h1,
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] h2,
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] span,
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] div {
        color: #ffffff !important;
    }

    /* Hide the radio checkmark indicator elements */
    [data-testid="stSidebar"] div[role="radiogroup"] label [data-testid="stValueError"] {
        display: none !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarker"] {
        display: none !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label span[data-testid="stText"] {
        margin-left: 0px !important;
        font-size: 1.05rem !important;
    }
    
    /* Hover effects */
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        transform: translateY(-2px) !important;
        border-color: var(--primary-color) !important;
        background-color: var(--sidebar-btn-hover) !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.04) !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"]:hover {
        transform: translateY(-2px) !important;
        background: var(--nav-gradient-hover) !important;
        color: #ffffff !important;
    }
</style>
"""

st.markdown(custom_styles, unsafe_allow_html=True)
# Custom medical illustration SVG
medical_illustration_svg = """
<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 1rem; width: 100%;">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="100%" style="max-width: 600px; height: auto;">
        <defs>
            <linearGradient id="blueCyanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#0ea5e9" stop-opacity="0.85" />
                <stop offset="100%" stop-color="#2563eb" stop-opacity="0.85" />
            </linearGradient>
            <linearGradient id="pulseGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#2563eb" />
                <stop offset="50%" stop-color="#0ea5e9" />
                <stop offset="100%" stop-color="#2563eb" />
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="5" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <circle cx="400" cy="100" r="90" fill="url(#blueCyanGrad)" opacity="0.03" />
        <circle cx="400" cy="100" r="60" fill="url(#blueCyanGrad)" opacity="0.05" />
        <line x1="80" y1="100" x2="720" y2="100" stroke="#0ea5e9" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.15" />
        <path d="M 80,100 L 220,100 L 230,85 L 240,115 L 250,100 L 340,100 L 352,50 L 365,160 L 378,100 L 430,100 L 438,70 L 446,110 L 454,90 L 462,100 L 580,100 L 590,85 L 600,115 L 610,100 L 720,100" 
              fill="none" stroke="url(#pulseGrad)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)" />
        <g transform="translate(378, 77) scale(0.9)">
            <path d="M 24.5,4 C 18,1 4,1 0,16 C 0,32 15,42 24.5,49 C 34,42 49,32 49,16 C 45,1 31,1 24.5,4 Z" fill="#ffffff" stroke="#e0f2fe" stroke-width="2" />
            <path d="M 24.5,7 C 19,4 7,4 3.5,16 C 3.5,29 16,38 24.5,44.5 C 33,38 45.5,29 45.5,16 C 42,4 30,4 24.5,7 Z" fill="url(#blueCyanGrad)" />
            <path d="M 21.5,17 H 27.5 V 23 H 33.5 V 29 H 27.5 V 35 H 21.5 V 29 H 15.5 V 23 H 21.5 Z" fill="#ffffff" />
        </g>
        <circle cx="280" cy="70" r="3" fill="#0ea5e9" opacity="0.6" />
        <circle cx="510" cy="130" r="4.5" fill="#2563eb" opacity="0.4" />
        <circle cx="210" cy="120" r="2" fill="#06b6d4" opacity="0.6" />
        <circle cx="590" cy="60" r="2.5" fill="#0ea5e9" opacity="0.5" />
    </svg>
</div>
"""

# Beautiful Title with Subtitle
st.markdown("""
<h1>🔬 Diabetes Screening Dashboard</h1>
<p class="subtitle">AI-Assisted Diagnostic Screening & Clinical Decision Support</p>
""", unsafe_allow_html=True)

# -------------------------------
# Helper functions
@st.cache_resource
def load_or_train_model():
    """Load pre-trained model or train & save if not exists."""
    model_path = "models/logistic_reg.sav"
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model
    else:
        # Load dataset
        df = pd.read_csv("Diabetes.csv")
        # Handle zero values in clinical settings by placing standard median placeholders
        # split inputs
        X = df.drop("Outcome", axis=1)
        y = df["Outcome"]
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Create pipeline with scaling and logistic regression
        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42))
        ])
        pipeline.fit(X_train, y_train)
        # Evaluate
        y_pred = pipeline.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        st.success(f"✅ Model trained on the fly. Test accuracy: {acc:.2f}")
        # Save model
        os.makedirs("models", exist_ok=True)
        with open(model_path, "wb") as f:
            pickle.dump(pipeline, f)
        return pipeline

# -------------------------------
# Sidebar navigation
st.sidebar.title("🩺 Navigation Options")
option = st.sidebar.radio(
    "Navigation Options", 
    ["🏠 Home", "🩺 Predict", "📊 Analytics", "📄 Dataset", "ℹ About", "🎨 Theme"],
    label_visibility="collapsed"
)

# Load model (cached)
model = load_or_train_model()
# -------------------------------
# Home Page
if option == "🏠 Home":
    st.markdown(medical_illustration_svg, unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-bottom: 0.5rem;'>🏠 Home</h3>", unsafe_allow_html=True)
    st.markdown("""
    Welcome to the **Diabetes Prediction Dashboard**, an AI-assisted clinical screening and decision support system. 
    This application utilizes machine learning models trained on the PIMA Indian Diabetes Dataset to evaluate patient parameters and predict diabetic risk.
    
    ### 🔬 System Features:
    *   **🩺 Diagnostics Predictor**: Fill in patient diagnostic numbers to render a detailed **Medical Report Card** with custom risk status (🔴 High Risk / 🟢 Low Risk), confidence metrics, and personalized clinical recommendations. Supports single entry and file upload (CSV).
    *   **📊 Dataset Explorer & Analytics**: Filter the dataset dynamically by age and outcome groups, visualize data via **Plotly plots**, and view population statistics.
    *   **📄 Dataset Details**: Check the features dictionary and view tabular raw data records.
    *   **🎨 Custom Accent Themes**: Choose between visual theme presets on-the-fly to customize the background and design.
    """, unsafe_allow_html=True)
    
    # Load and display quick summary stats of the dataset
    df_full = pd.read_csv("Diabetes.csv")
    st.write("")
    st.markdown("<h5 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-bottom: 1rem;'>📊 Population Quick Stats</h5>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Population Size", len(df_full))
    with col2:
        diabetic_cases = df_full["Outcome"].sum()
        st.metric("Diabetic Records", diabetic_cases)
    with col3:
        diabetic_ratio = (df_full["Outcome"] == 1).mean() * 100
        st.metric("Diabetic Ratio", f"{diabetic_ratio:.1f}%")

# -------------------------------
# Predict Page (Tabs for Single / Batch)
elif option == "🩺 Predict":
    st.markdown("<h3 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-bottom: 0.5rem;'>🩺 Diabetes Predictor Workspace</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 0.95rem; margin-bottom: 1.5rem;'>Perform diabetes risk analysis below. Choose between manual entry or batch file upload:</p>", unsafe_allow_html=True)
    
    tab_single, tab_batch = st.tabs(["🔍 Single Patient Entry", "📂 Batch Upload (CSV)"])
    
    with tab_single:
        st.markdown("<h5 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-bottom: 1rem;'>🔍 Single Patient Diagnostic Entry</h5>", unsafe_allow_html=True)
        # Wrap inputs inside a glassmorphism card styled container (not using st.form to enable live validation alerts)
        with st.container(key="input_card"):
            # Set up defaults for all prediction sliders/inputs to support clinical resetting if not initialized
            default_inputs = {
                "s_patient_name": "Patient Alpha",
                "s_pregnancies": 1,
                "s_glucose": 120,
                "s_blood_pressure": 70,
                "s_skin_thickness": 20,
                "s_insulin": None,
                "s_bmi": 25.0,
                "s_dpf": None,
                "s_age": 30
            }
            for k, v in default_inputs.items():
                if k not in st.session_state:
                    st.session_state[k] = v

            patient_name = st.text_input("👤 Patient Name / Identifier", key="s_patient_name", help="Enter patient name or clinical case number")
            st.write("")

            col1, col2 = st.columns(2)
            
            with col1:
                pregnancies = st.slider("🤰 Pregnancies", min_value=0, max_value=20, key="s_pregnancies", help="Number of times pregnant")
                if pregnancies > 10:
                    st.markdown('<div class="indicator-box indicator-orange">⚠️ High parity (>10) elevates gestational risks</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="indicator-box indicator-green">🟢 Standard range</div>', unsafe_allow_html=True)
                
                st.write("") # Spacer

                glucose = st.slider("🩸 Glucose Level (mg/dL)", min_value=0, max_value=200, key="s_glucose", help="2-hour plasma glucose concentration in oral glucose tolerance test")
                if glucose < 70:
                    st.markdown('<div class="indicator-box indicator-blue">🔵 Hypoglycemia (<70 mg/dL)</div>', unsafe_allow_html=True)
                elif glucose < 100:
                    st.markdown('<div class="indicator-box indicator-green">🟢 Normal Fasting (<100 mg/dL)</div>', unsafe_allow_html=True)
                elif glucose <= 125:
                    st.markdown('<div class="indicator-box indicator-orange">🟡 Impaired Gluc / Prediabetes (100-125 mg/dL)</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="indicator-box indicator-red">🔴 Critical Diabetic Level (≥126 mg/dL)</div>', unsafe_allow_html=True)

                st.write("") # Spacer

                blood_pressure = st.slider("🩺 Diastolic Blood Pressure (mm Hg)", min_value=0, max_value=150, key="s_blood_pressure", help="Diastolic blood pressure (mm Hg)")
                if blood_pressure < 60:
                    st.markdown('<div class="indicator-box indicator-blue">🔵 Hypotension (<60 mm Hg)</div>', unsafe_allow_html=True)
                elif blood_pressure <= 80:
                    st.markdown('<div class="indicator-box indicator-green">🟢 Normal (60-80 mm Hg)</div>', unsafe_allow_html=True)
                elif blood_pressure <= 89:
                    st.markdown('<div class="indicator-box indicator-orange">🟡 Prehypertension (81-89 mm Hg)</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="indicator-box indicator-red">🔴 Hypertension (≥90 mm Hg)</div>', unsafe_allow_html=True)

                st.write("") # Spacer

                skin_thickness = st.slider("📏 Skin Thickness (mm)", min_value=0, max_value=100, key="s_skin_thickness", help="Triceps skin fold thickness (mm)")
                if 10 <= skin_thickness <= 50:
                    st.markdown('<div class="indicator-box indicator-green">🟢 Healthy Range (10-50 mm)</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="indicator-box indicator-orange">⚠️ Atypical skin folds thickness</div>', unsafe_allow_html=True)

            with col2:
                insulin = st.number_input("💉 Insulin Level (mu U/ml)", min_value=0, max_value=900, key="s_insulin", placeholder="e.g. 80", help="2-Hour serum insulin (mu U/ml). Leave empty for clinical default.")
                if insulin is None:
                    st.markdown('<div class="indicator-box indicator-blue">ℹ️ Running with clinical median default: 80 mu U/ml</div>', unsafe_allow_html=True)
                    insulin_val = 80
                else:
                    insulin_val = insulin
                    if insulin < 16:
                        st.markdown('<div class="indicator-box indicator-orange">⚠️ Low fasting insulin level (<16)</div>', unsafe_allow_html=True)
                    elif insulin <= 166:
                        st.markdown('<div class="indicator-box indicator-green">🟢 Healthy insulin range (16-166)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="indicator-box indicator-red">🔴 Hyperinsulinemia / Resistance (>166)</div>', unsafe_allow_html=True)

                st.write("") # Spacer

                bmi = st.slider("⚖️ Body Mass Index (BMI)", min_value=0.0, max_value=70.0, step=0.1, key="s_bmi", help="Body Mass Index (weight in kg / (height in m)²)")
                if bmi < 18.5:
                    st.markdown('<div class="indicator-box indicator-orange">🟡 Underweight (<18.5)</div>', unsafe_allow_html=True)
                elif bmi < 25.0:
                    st.markdown('<div class="indicator-box indicator-green">🟢 Normal / Healthy BMI (18.5-24.9)</div>', unsafe_allow_html=True)
                elif bmi < 30.0:
                    st.markdown('<div class="indicator-box indicator-orange">🟡 Overweight (25.0-29.9)</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="indicator-box indicator-red">🔴 Obese (≥30.0)</div>', unsafe_allow_html=True)

                st.write("") # Spacer

                dpf = st.number_input("🧬 Diabetes Pedigree Function", min_value=0.0, max_value=2.5, key="s_dpf", placeholder="e.g. 0.47", step=0.01, help="Diabetes pedigree function scoring family history. Leave empty for average default.")
                if dpf is None:
                    st.markdown('<div class="indicator-box indicator-blue">ℹ️ Running with hereditary default: 0.47</div>', unsafe_allow_html=True)
                    dpf_val = 0.47
                else:
                    dpf_val = dpf
                    if dpf < 0.50:
                        st.markdown('<div class="indicator-box indicator-green">🟢 Low hereditary risk index (<0.50)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="indicator-box indicator-red">🔴 High hereditary risk index (≥0.50)</div>', unsafe_allow_html=True)

                st.write("") # Spacer

                age = st.slider("📅 Age (years)", min_value=0, max_value=120, key="s_age", help="Patient age in years")
                if age >= 45:
                    st.markdown('<div class="indicator-box indicator-orange">⚠️ Aged 45+: Elevates metabolic risks</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="indicator-box indicator-green">🟢 Standard age group risk</div>', unsafe_allow_html=True)
            
            st.write("")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                predict_button = st.button("🔮 Predict Diabetes Status", type="primary", use_container_width=True)
            with col_btn2:
                reset_button = st.button("🔄 Reset Diagnostic Metrics", type="secondary", use_container_width=True)
                if reset_button:
                    for k, v in default_inputs.items():
                        st.session_state[k] = v
                    st.rerun()

            if predict_button:
                # Better Error Handling - input boundary validation
                val_errors = []
                if glucose == 0:
                    val_errors.append("Plasma Glucose level cannot be 0 mg/dL for active screening assessment.")
                if bmi == 0.0:
                    val_errors.append("Body Mass Index (BMI) cannot be 0.0.")
                if blood_pressure == 0:
                    val_errors.append("BP cannot be 0 mmHg. Patient requires immediate triage.")
                
                if val_errors:
                    for err in val_errors:
                        st.error(f"🚨 **Clinical Validation Alert:** {err}")
                else:
                    # Input data as DataFrame
                    input_data = pd.DataFrame([[pregnancies, glucose, blood_pressure, skin_thickness,
                                                insulin_val, bmi, dpf_val, age]],
                                              columns=["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                                                       "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"])
                    
                    # Loader with a smooth dynamic step-by-step progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    for percent_complete in range(100):
                        progress_bar.progress(percent_complete + 1)
                        if percent_complete < 33:
                            status_text.markdown("<p style='text-align:center; color:var(--primary-color); font-weight:600;'>⚡ Normalizing and scaling metabolic metrics...</p>", unsafe_allow_html=True)
                        elif percent_complete < 66:
                            status_text.markdown("<p style='text-align:center; color:var(--primary-color); font-weight:600;'>🧠 Querying Logistic Classifier boundaries...</p>", unsafe_allow_html=True)
                        else:
                            status_text.markdown("<p style='text-align:center; color:var(--primary-color); font-weight:600;'>📊 Computing diagnostic decision boundaries...</p>", unsafe_allow_html=True)
                        time.sleep(0.01)
                    
                    progress_bar.empty()
                    status_text.empty()
    
                    # Predict
                    prediction = model.predict(input_data)[0]
                    proba = model.predict_proba(input_data)[0][1]  # Probability of class 1
    
                    if prediction == 1:
                        confidence = proba * 100
                        st.markdown(f"""
                        <div class="medical-card medical-card-diabetic">
                            <div class="medical-card-header">
                                <span class="medical-card-title">📋 Clinical Assessment Report</span>
                                <span class="medical-badge medical-badge-high">🔴 High Risk</span>
                            </div>
                            <div style="font-size: 0.95rem; color: #64748b; margin-bottom: 1.5rem;">
                                Patient diagnostic markers exceed normal metabolic boundaries. Logistic classification indicates high likelihood of diabetic indicators.
                            </div>
                            <div class="confidence-container">
                                <div class="confidence-header">
                                    <span>Prediction Confidence Score</span>
                                    <span class="confidence-percentage confidence-percentage-high">{confidence:.1f}%</span>
                                </div>
                                <div class="confidence-bar-bg">
                                    <div class="confidence-bar-fill confidence-bar-fill-high" style="width: {confidence:.2f}%;"></div>
                                </div>
                            </div>
                            <div class="medical-card-divider"></div>
                            <div class="medical-grid">
                                <div class="medical-grid-item">
                                    <div class="medical-grid-label">Glucose</div>
                                    <div class="medical-grid-value" style="color: #ef4444;">{glucose} mg/dL</div>
                                </div>
                                <div class="medical-grid-item">
                                    <div class="medical-grid-label">BMI</div>
                                    <div class="medical-grid-value" style="color: #ef4444;">{bmi:.1f}</div>
                                </div>
                                <div class="medical-grid-item">
                                    <div class="medical-grid-label">Age</div>
                                    <div class="medical-grid-value">{age} yrs</div>
                                </div>
                                <div class="medical-grid-item">
                                    <div class="medical-grid-label">Blood Press.</div>
                                    <div class="medical-grid-value">{blood_pressure} mmHg</div>
                                </div>
                            </div>
                            <div class="medical-card-divider"></div>
                            <div class="medical-tips-title">📋 Clinical Recommendations:</div>
                            <ul class="medical-tips-list">
                                <li class="medical-tips-item medical-tips-item-high"><strong>Consult Endocrinology Specialists:</strong> We recommend booking a comprehensive diagnostic review and HbA1c screening tests.</li>
                                <li class="medical-tips-item medical-tips-item-high"><strong>Self-Monitoring:</strong> Maintain regular pre & post-prandial glycemic logbooks.</li>
                                <li class="medical-tips-item medical-tips-item-high"><strong>Nutrition Protocols:</strong> Prioritize low glycemic index, high-fiber dietary intakes.</li>
                                <li class="medical-tips-item medical-tips-item-high"><strong>Aerobic Exercise:</strong> Introduce 150 minutes of weekly moderate fitness mapping.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        confidence = (1 - proba) * 100
                        st.markdown(f"""
                        <div class="medical-card medical-card-healthy">
                            <div class="medical-card-header">
                                <span class="medical-card-title">📋 Clinical Assessment Report</span>
                                <span class="medical-badge medical-badge-low">🟢 Low Risk</span>
                            </div>
                            <div style="font-size: 0.95rem; color: #64748b; margin-bottom: 1.5rem;">
                                Patient markers reside within standard metabolic thresholds. Logistic classification predicts low risk of diabetic indicators.
                            </div>
                            <div class="confidence-container">
                                <div class="confidence-header">
                                    <span>Prediction Confidence Score</span>
                                    <span class="confidence-percentage confidence-percentage-low">{confidence:.1f}%</span>
                                </div>
                                <div class="confidence-bar-bg">
                                    <div class="confidence-bar-fill confidence-bar-fill-low" style="width: {confidence:.2f}%;"></div>
                                </div>
                            </div>
                            <div class="medical-card-divider"></div>
                            <div class="medical-grid">
                                <div class="medical-grid-item">
                                    <div class="medical-grid-label">Glucose</div>
                                    <div class="medical-grid-value" style="color: #22c55e;">{glucose} mg/dL</div>
                                </div>
                                <div class="medical-grid-item">
                                    <div class="medical-grid-label">BMI</div>
                                    <div class="medical-grid-value" style="color: #22c55e;">{bmi:.1f}</div>
                                </div>
                                <div class="medical-grid-item">
                                    <div class="medical-grid-label">Age</div>
                                    <div class="medical-grid-value">{age} yrs</div>
                                </div>
                                <div class="medical-grid-item">
                                    <div class="medical-grid-label">Blood Press.</div>
                                    <div class="medical-grid-value">{blood_pressure} mmHg</div>
                                </div>
                            </div>
                            <div class="medical-card-divider"></div>
                            <div class="medical-tips-title">🌱 Preventive Lifestyle Metrics:</div>
                            <ul class="medical-tips-list">
                                <li class="medical-tips-item medical-tips-item-low"><strong>Balanced Diet:</strong> Focus on whole-food carbs, lean proteins, healthy fats.</li>
                                <li class="medical-tips-item medical-tips-item-low"><strong>Active Movement:</strong> Ensure brief walks after carbohydrate meals.</li>
                                <li class="medical-tips-item medical-tips-item-low"><strong>Hydration Status:</strong> Maximize water intake while limiting sugary beverages.</li>
                                <li class="medical-tips-item medical-tips-item-low"><strong>Routine Screening:</strong> Track metabolic metrics annually for comprehensive health maintenance.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Store in Session Log History
                    history_entry = {
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Patient Name": patient_name if patient_name.strip() != "" else "Unnamed Patient",
                        "Pregnancies": pregnancies,
                        "Glucose": glucose,
                        "Blood Pressure": blood_pressure,
                        "Skin Thickness": skin_thickness,
                        "Insulin": insulin_val,
                        "BMI": bmi,
                        "DPF": dpf_val,
                        "Age": age,
                        "Outcome": "🔴 High Risk" if prediction == 1 else "🟢 Low Risk",
                        "Confidence": f"{confidence:.1f}%"
                    }
                    st.session_state.prediction_history.append(history_entry)
                    
                    # Generate and place PDF download button
                    pdf_bytes = generate_pdf_report(
                        patient_name=patient_name if patient_name.strip() != "" else "Unnamed Patient",
                        prediction=prediction,
                        confidence=confidence,
                        pregnancies=pregnancies,
                        glucose=glucose,
                        blood_pressure=blood_pressure,
                        skin_thickness=skin_thickness,
                        insulin=insulin_val,
                        bmi=bmi,
                        diabetes_pedigree_function=dpf_val,
                        age=age
                    )
                    
                    st.download_button(
                        label="📄 Download Diagnostic PDF Report",
                        data=pdf_bytes,
                        file_name=f"clinical_report_{patient_name.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

        # Show prediction history logbook below inputs
        st.markdown("<div class='medical-card-divider'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-top: 1.5rem; margin-bottom: 0.8rem;'>📋 Clinical Screening Logbook (Prediction History)</h4>", unsafe_allow_html=True)
        if len(st.session_state.prediction_history) > 0:
            df_history = pd.DataFrame(st.session_state.prediction_history)
            st.dataframe(df_history, use_container_width=True)
            
            col_dh1, col_dh2 = st.columns(2)
            with col_dh1:
                csv_bytes = df_history.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Export Logbook (CSV)",
                    data=csv_bytes,
                    file_name="diabetes_screening_logbook.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col_dh2:
                if st.button("🗑️ Clear Screening Logbook", use_container_width=True):
                    st.session_state.prediction_history = []
                    st.rerun()
        else:
            st.info("No screenings logged in this session yet. Run predictions above to log data.")

    with tab_batch:
        uploaded_file = st.file_uploader("📂 Choose a CSV file for diagnosis", type="csv")
        if uploaded_file is not None:
            df_upload = pd.read_csv(uploaded_file)
            
            st.markdown("<h5 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-top: 1rem;'>Uploaded Data Preview</h5>", unsafe_allow_html=True)
            st.dataframe(df_upload.head(5), use_container_width=True)

            # Check required columns
            required_cols = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                             "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
            if all(col in df_upload.columns for col in required_cols):
                # Dynamic loader progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                for percent_complete in range(100):
                    progress_bar.progress(percent_complete + 1)
                    status_text.markdown(f"<p style='text-align:center; color:var(--primary-color); font-weight:600;'>⏳ Running batch diagnostics... {percent_complete+1}%</p>", unsafe_allow_html=True)
                    time.sleep(0.015)
                progress_bar.empty()
                status_text.empty()
                
                # Make predictions
                predictions = model.predict(df_upload[required_cols])
                probabilities = model.predict_proba(df_upload[required_cols])[:, 1]

                # Scroll results
                df_upload["Prediction"] = predictions
                df_upload["Probability (Diabetic)"] = probabilities
                df_upload["Result"] = df_upload["Prediction"].apply(lambda x: "Diabetic" if x == 1 else "Not Diabetic")

                st.markdown("<h5 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-top: 1.5rem;'>📊 Prediction Output Batch</h5>", unsafe_allow_html=True)
                st.dataframe(df_upload, use_container_width=True)

                # Columns for actions and metrics
                action_col, summary_col = st.columns([1, 1])
                with action_col:
                    st.markdown("<h5 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-top: 1rem;'>Actions</h5>", unsafe_allow_html=True)
                    csv_output = df_upload.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Download Predictions as CSV", csv_output, "predictions.csv", "text/csv")
                
                with summary_col:
                    st.markdown("<h5 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-top: 1rem;'>Statistics</h5>", unsafe_allow_html=True)
                    diabetic_count = df_upload["Prediction"].sum()
                    total = len(df_upload)
                    
                    col_met1, col_met2 = st.columns(2)
                    with col_met1:
                        st.metric("Total Patients", total)
                    with col_met2:
                        st.metric("Predicted Diabetic Cases", diabetic_count, delta=f"{diabetic_count/total*100:.1f}%")
            else:
                st.error(f"CSV must contain columns: {required_cols}")
# -------------------------------
# Dataset Explorer & Analytics Page
elif option == "📊 Analytics":
    st.markdown("<h3 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-bottom: 0.5rem;'>📊 Dataset Explorer & Visual Analytics</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 0.95rem; margin-bottom: 1.5rem;'>Filter the patient population parameters and visualize critical metabolic metrics dynamically using interactive data charts.</p>", unsafe_allow_html=True)

    df_full = pd.read_csv("Diabetes.csv")
    
    # Selection/filtering sidebar-like widgets within columns
    st.markdown("<h5 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-top: 1rem;'>🔍 Populate and Filter Dataset</h5>", unsafe_allow_html=True)
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        age_range = st.slider("Filter by Age Range", int(df_full["Age"].min()), int(df_full["Age"].max()), (int(df_full["Age"].min()), int(df_full["Age"].max())), help="Filter metrics based on age segments")
    with filter_col2:
        outcome_filter = st.multiselect("Outcome Profile Filter", ["Healthy", "Diabetic"], default=["Healthy", "Diabetic"], help="Select diabetic diagnostic groups")
    
    # Map outcome filter to values
    filter_vals = []
    if "Healthy" in outcome_filter:
        filter_vals.append(0)
    if "Diabetic" in outcome_filter:
        filter_vals.append(1)
        
    df_filtered = df_full[(df_full["Age"] >= age_range[0]) & (df_full["Age"] <= age_range[1])]
    df_filtered = df_filtered[df_filtered["Outcome"].isin(filter_vals)]
    
    if len(df_filtered) == 0:
        st.warning("⚠️ No records match the set filters. Please adjust sliders or selection filters.")
    else:
        # Create map label for Plotly plots
        df_filtered["Diabetic Status"] = df_filtered["Outcome"].map({0: "Healthy", 1: "Diabetic"})
        
        # Summary metrics
        met_col1, met_col2, met_col3, met_col4 = st.columns(4)
        with met_col1:
            st.metric("Filtered Records Count", len(df_filtered))
        with met_col2:
            st.metric("Avg Glucose Level", f"{df_filtered['Glucose'].mean():.1f} mg/dL")
        with met_col3:
            st.metric("Avg BMI Rate", f"{df_filtered['BMI'].mean():.1f}")
        with met_col4:
            diabetic_ratio = (df_filtered["Outcome"] == 1).mean() * 100
            st.metric("Diabetic Cases Ratio", f"{diabetic_ratio:.1f}%")
            
        st.markdown("<div class='medical-card-divider'></div>", unsafe_allow_html=True)
        st.markdown("<h5 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-bottom: 1.5rem;'>📈 Population Distributions (Segmented by Outcome)</h5>", unsafe_allow_html=True)
        
        chart_col1, chart_col2 = st.columns(2)
        color_maps = {"Healthy": "#10b981", "Diabetic": "#ef4444"}
        
        with chart_col1:
            # 1. Age Distribution
            fig_age = px.histogram(df_filtered, x="Age", color="Diabetic Status", barmode="overlay",
                                   color_discrete_map=color_maps, title="Age Distribution Profile",
                                   template="plotly_white")
            fig_age.update_layout(bargap=0.08, margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig_age, use_container_width=True)
            
            # 2. Glucose Distribution
            fig_glucose = px.histogram(df_filtered, x="Glucose", color="Diabetic Status", barmode="overlay",
                                       color_discrete_map=color_maps, title="Glucose Levels Distribution",
                                       template="plotly_white")
            fig_glucose.update_layout(bargap=0.08, margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig_glucose, use_container_width=True)
            
            # 3. BMI Box Plot
            fig_bmi = px.box(df_filtered, x="Diabetic Status", y="BMI", color="Diabetic Status",
                             color_discrete_map=color_maps, title="Body Mass Index (BMI) Range",
                             template="plotly_white")
            fig_bmi.update_layout(margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig_bmi, use_container_width=True)
            
        with chart_col2:
            # 4. Blood Pressure Distribution
            fig_bp = px.histogram(df_filtered, x="BloodPressure", color="Diabetic Status", barmode="overlay",
                                  color_discrete_map=color_maps, title="Diastolic Blood Pressure Distribution",
                                  template="plotly_white")
            fig_bp.update_layout(bargap=0.08, margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig_bp, use_container_width=True)
            
            # 5. Pregnancies Count Comparison
            fig_preg = px.histogram(df_filtered, x="Pregnancies", color="Diabetic Status", barmode="group",
                                    color_discrete_map=color_maps, title="Pregnancies Group Comparison",
                                    template="plotly_white")
            fig_preg.update_layout(bargap=0.08, margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig_preg, use_container_width=True)
            
            # 6. Insulin Box Plot
            fig_insulin = px.box(df_filtered, x="Diabetic Status", y="Insulin", color="Diabetic Status",
                                 color_discrete_map=color_maps, title="Insulin Distribution Profile",
                                 template="plotly_white")
            fig_insulin.update_layout(margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig_insulin, use_container_width=True)
            
        st.markdown("<div class='medical-card-divider'></div>", unsafe_allow_html=True)
        with st.expander("📋 View Filtered Dataset Records Table"):
            st.dataframe(df_filtered, use_container_width=True)

# -------------------------------
# Dataset details Page
elif option == "📄 Dataset":
    st.markdown("<h3 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-bottom: 0.5rem;'>📄 Dataset & Variables</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 0.95rem; margin-bottom: 1.5rem;'>View details about the variables used in the screening or explore raw dataset records.</p>", unsafe_allow_html=True)
    
    tab_vars, tab_raw = st.tabs(["📋 Variables Dictionary", "🔍 Raw Dataset Records"])
    
    with tab_vars:
        st.markdown("""
        ### **Dataset Variables**
        The dataset is from the **PIMA Indian Diabetes Database** from the National Institute of Diabetes and Digestive and Kidney Diseases:
        
        *   **🤰 Pregnancies:** Number of times pregnant.
        *   **🩸 Glucose:** 2-hour plasma glucose concentration in oral glucose tolerance test.
        *   **🩺 Blood Pressure:** Diastolic blood pressure (mmHg).
        *   **📏 Skin Thickness:** Triceps skin fold thickness (mm) representation.
        *   **💉 Insulin:** 2-hour serum insulin level (mu U/ml).
        *   **⚖️ BMI:** Body Mass Index (weight in kg / (height in m)²).
        *   **🧬 Diabetes Pedigree Function:** Diabetes pedigree function scoring family history.
        *   **📅 Age:** Patient age in years.
        """)
        
    with tab_raw:
        df_full = pd.read_csv("Diabetes.csv")
        st.markdown("##### View Raw Records")
        row_limit = st.slider("Select number of records to display", 5, 200, 50)
        st.dataframe(df_full.head(row_limit), use_container_width=True)

# -------------------------------
# About Page
elif option == "ℹ About":
    st.markdown("<h3 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-bottom: 0.5rem;'>📖 About & Model Evaluation</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 0.95rem; margin-bottom: 1.5rem;'>Understand the underpinning machine learning pipelines, dataset features, and developer info.</p>", unsafe_allow_html=True)

    tab_overview, tab_model, tab_tech, tab_dev = st.tabs([
        "📋 Project Overview & Dataset", 
        "🧠 Machine Learning Model", 
        "🛠️ Technologies Used", 
        "👤 Developer & Credits"
    ])
    
    with tab_overview:
        st.markdown("### **📋 Project Overview**")
        st.markdown(
            "This **Diabetes Prediction Dashboard** is an AI-assisted diagnostic screening and decision support platform. "
            "It utilizes standard logistic regression classification trained on historical patient records to evaluate and rank "
            "diabetic risk parameters. This tool is designed to support clinical workflows, identify risk boundaries, "
            "and suggest preventive lifestyle protocols."
        )
        st.write("")
        st.markdown("### **📊 Dataset Information**")
        st.markdown(
            "The model is trained on the **PIMA Indian Diabetes Dataset**, originally from the *National Institute of "
            "Diabetes and Digestive and Kidney Diseases* (NIDDK). The database contains clinical indicators from female "
            "patients of Pima Indian heritage. Key attributes include:"
        )
        st.markdown(
            "- **Pregnancies**: Number of previous pregnancies.\n"
            "- **Glucose**: 2-hour plasma glucose concentration from oral tolerance tests.\n"
            "- **Blood Pressure**: Diastolic blood pressure (mmHg).\n"
            "- **Skin Thickness**: Triceps skin fold thickness (mm).\n"
            "- **Insulin**: 2-hour serum insulin levels (mu U/ml).\n"
            "- **BMI**: Body Mass Index (weight in kg / (height in m)²).\n"
            "- **Diabetes Pedigree Function**: Scoring factor representing hereditary/familial lineage diabetes history.\n"
            "- **Age**: Patient age in years."
        )

    with tab_model:
        df_full = pd.read_csv("Diabetes.csv")
        X_full = df_full.drop("Outcome", axis=1)
        y_full = df_full["Outcome"]
        _, X_test, _, y_test = train_test_split(X_full, y_full, test_size=0.2, random_state=42)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)

        st.markdown("### **🧠 Machine Learning Pipeline Specifications**")
        st.markdown(
            "- **Model Classifier**: Logistic Regression (`max_iter=1000`, `random_state=42`)\n"
            "- **Preprocessors**: `StandardScaler` pipeline for scaling metabolic properties.\n"
            "- **Diagnostic Target**: Predict binary diabetic marker (`1` for Risk / `0` for Low Risk)."
        )
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Classifier Validation Accuracy", f"{acc:.2%}")
        
        st.write("")
        st.markdown("#### **Confusion Matrix Heatmap**")
        
        # Confusion matrix heatmap styled to match
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#f0f7ff')
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                    annot_kws={"size": 13, "weight": "bold", "color": "#0f172a"})
        ax.set_xlabel("Predicted Label", fontsize=11, fontweight='bold', color='#1e293b')
        ax.set_ylabel("Actual Label", fontsize=11, fontweight='bold', color='#1e293b')
        ax.set_title("Confusion Matrix Classifier Performance", fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        ax.tick_params(colors='#1e293b', labelsize=10)
        for spine in ax.spines.values():
            spine.set_edgecolor('#cbd5e1')
        st.pyplot(fig)

    with tab_tech:
        st.markdown("### **🛠️ Platform Technologies Stack**")
        st.markdown("The platform leverages standard scientific and GUI packages to ensure high portability, response speed, and diagnostic accuracy:")
        
        st.markdown("""
        <div class="tech-stack-container" style="display: flex; flex-direction: column; gap: 0.8rem; margin-top: 1rem;">
            <div style="background: rgba(14, 165, 233, 0.08); border-left: 4px solid #0ea5e9; padding: 0.8rem; border-radius: 4px;">
                <strong>🐍 Python:</strong> Core programming language wrapping all ML and dataset manipulation libraries.
            </div>
            <div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; padding: 0.8rem; border-radius: 4px;">
                <strong>🎈 Streamlit:</strong> Modern visual layout routing widget and interactive form engine.
            </div>
            <div style="background: rgba(245, 158, 11, 0.08); border-left: 4px solid #f59e0b; padding: 0.8rem; border-radius: 4px;">
                <strong>🧠 Scikit-Learn:</strong> Powers the ML preprocessing pipeline, scaler standardizer, and logistic classifier.
            </div>
            <div style="background: rgba(37, 99, 235, 0.08); border-left: 4px solid #2563eb; padding: 0.8rem; border-radius: 4px;">
                <strong>🔢 NumPy:</strong> High-performance vector representation logic for model input values.
            </div>
            <div style="background: rgba(99, 102, 241, 0.08); border-left: 4px solid #6366f1; padding: 0.8rem; border-radius: 4px;">
                <strong>🐼 Pandas:</strong> Clean ingestion dataframes for viewing and downloading cohort results.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_dev:
        st.markdown("### **👤 Developer & Contact Info**")
        st.markdown(
            "This decision support platform is designed and maintained by **Priyam Rai**. "
            "Please check the links below to connect, view source code, or explore other projects."
        )
        
        st.write("")
        col_g, col_l = st.columns(2)
        with col_g:
            st.link_button(
                "🐱 Visit GitHub Profile", 
                "https://github.com/priyam-rai", 
                use_container_width=True,
                help="Explore repositories and system source code"
            )
        with col_l:
            st.link_button(
                "🔗 Connect on LinkedIn", 
                "https://linkedin.com/in/priyam-rai", 
                use_container_width=True,
                help="Connect and message on LinkedIn"
            )
        st.write("")
        st.info("ℹ️ Clinical decision support models are meant to aid screening workflows; they do not replace formal custom medical evaluations.")

# -------------------------------
# Theme Page
elif option == "🎨 Theme":
    st.markdown("<h3 style='font-family: \"Outfit\", sans-serif; color: var(--heading-color); margin-bottom: 0.5rem;'>🎨 App Accent Theme Selector</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 0.95rem; margin-bottom: 1.5rem;'>Select visual presets to customize theme colors and accent indicators throughout the platform in real-time.</p>", unsafe_allow_html=True)
    
    theme_choice = st.radio(
        "Choose Theme Accent Preset", 
        ["Clean Medical Blue", "Emerald Health", "Crimson Alert", "Cyber Clinic (Dark)"],
        index=["Clean Medical Blue", "Emerald Health", "Crimson Alert", "Cyber Clinic (Dark)"].index(st.session_state.theme)
    )
    
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

# -------------------------------
# Footer
st.markdown("""
<div class="footer">
    <p>Developed with 💙 by <strong>Priyam Rai</strong> | AI Healthcare Decision Support System</p>
</div>
""", unsafe_allow_html=True)
