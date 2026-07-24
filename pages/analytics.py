import pandas as pd
import streamlit as st
import plotly.express as px

def show_analytics_page():
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
