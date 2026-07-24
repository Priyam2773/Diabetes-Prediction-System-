import streamlit as st

def show_theme_page():
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
