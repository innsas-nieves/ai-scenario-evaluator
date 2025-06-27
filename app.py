st.set_page_config(
    page_title="UNLV AI Framework Tools",
    layout="centered",
    page_icon="🎓"
)
import streamlit as st

st.title("🎓 UNLV AI Framework Interactive Tools")
st.write("""
Welcome to the UNLV AI Framework app. This toolset helps UNLV instructors, administrators, and researchers explore and evaluate their use of AI using institutional guidance.

Choose a tool to get started:
""")

st.markdown("### 🧠 AI Scenario Evaluator")
st.markdown("_Describe an AI use case and get feedback based on the framework’s four domains._")

st.markdown("### 📝 Syllabus Advisor _(coming soon)_")
st.markdown("_Paste a syllabus to check for transparency, equity, and academic integrity in AI expectations._")

st.markdown("### 🧭 Framework Reflection Tool _(coming soon)_")
st.markdown("_Answer guided prompts to reflect on your AI-related practices._")

st.markdown("---")

st.markdown("""
📚 [View the full UNLV AI Framework PDF](https://your-link-to-the-framework.pdf)  
🛠️ Questions? Contact [alethea.inns@unlv.edu](mailto:alethea.inns@unlv.edu)
""")
