import streamlit as st

# Custom styling definitions
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
    }

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

# Custom SVG logo / illustration
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
