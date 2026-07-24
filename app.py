import streamlit as st

# Import modular components
from utils.theme_manager import inject_theme_styles, custom_styles
from utils.model_loader import load_or_train_model
from pages.home import show_home_page
from pages.predict import show_predict_page
from pages.analytics import show_analytics_page
from pages.dataset import show_dataset_page
from pages.about import show_about_page
from pages.theme import show_theme_page

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme selection
if "theme" not in st.session_state:
    st.session_state.theme = "Clean Medical Blue"

# Determine theme mode dynamically based on the active theme
if st.session_state.theme == "Cyber Clinic (Dark)":
    st.session_state.theme_mode = "🌙 Dark Mode"
else:
    st.session_state.theme_mode = "☀️ Light Mode"

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# Inject custom styles & presets
inject_theme_styles()
st.markdown(custom_styles, unsafe_allow_html=True)

# Beautiful Title with Subtitle
st.markdown("""
<h1>🔬 Diabetes Screening Dashboard</h1>
<p class="subtitle">AI-Assisted Diagnostic Screening & Clinical Decision Support</p>
""", unsafe_allow_html=True)

# Load cached / trained model
model = load_or_train_model()

# Sidebar navigation
st.sidebar.title("🩺 Navigation Options")
option = st.sidebar.radio(
    "Navigation Options", 
    ["🏠 Home", "🩺 Predict", "📊 Analytics", "📄 Dataset", "ℹ About", "🎨 Theme"],
    label_visibility="collapsed"
)

# Page Routing
if option == "🏠 Home":
    show_home_page()
elif option == "🩺 Predict":
    show_predict_page(model)
elif option == "📊 Analytics":
    show_analytics_page()
elif option == "📄 Dataset":
    show_dataset_page()
elif option == "ℹ About":
    show_about_page(model)
elif option == "🎨 Theme":
    show_theme_page()

# Footer
st.markdown("""
<div class="footer">
    <p>Developed with 💙 by <strong>Priyam Rai</strong> | AI Healthcare Decision Support System</p>
</div>
""", unsafe_allow_html=True)
