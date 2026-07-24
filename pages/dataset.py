import pandas as pd
import streamlit as st

def show_dataset_page():
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
