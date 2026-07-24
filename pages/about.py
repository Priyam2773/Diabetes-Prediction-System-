import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

def show_about_page(model):
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
