import datetime
from fpdf import FPDF

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
    
    # Bottom details (Diagnosis Card Block)
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
