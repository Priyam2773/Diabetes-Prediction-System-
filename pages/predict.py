import time
import datetime
import pandas as pd
import streamlit as st
from utils.pdf_generator import generate_pdf_report

def show_predict_page(model):
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
