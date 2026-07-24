import streamlit as st
import pandas as pd
from utils.theme_manager import medical_illustration_svg

def show_home_page():
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
