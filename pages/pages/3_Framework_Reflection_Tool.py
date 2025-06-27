import streamlit as st
import openai

st.set_page_config(page_title="Framework Reflection Tool", layout="centered")

st.title("🧭 Framework Reflection Tool")
st.write("Use this tool to reflect on how your current or planned use of AI aligns with the UNLV AI Framework.")

# Role selector
role = st.selectbox("👤 What is your role?", ["Select...", "Instructor", "Administrator", "Researcher"])

# Input prompts based on role
if role != "Select...":
    st.subheader("💬 Reflection Prompts")

    use_case = st.text_area("1. Describe how you're currently using or planning to use AI in your work:", height=150)
    goals = st.text_area("2. What are your goals or motivations for using AI?", height=100)
    concerns = st.text_area("3. What concerns do you have (e.g., ethics, effectiveness, bias, equity)?", height=100)

    api_key = st.text_input("🔑 Enter your OpenAI API key:", type="password")

    if st.button("Generate Reflection Summary"):
        if not (use_case.strip() and goals.strip() and concerns.strip()):
            st.warning("Please complete all three reflection prompts.")
        elif not api_key:
            st.warning("Please enter your OpenAI API key.")
        else:
            try:
                client = openai.OpenAI(api_key=api_key)
                with st.spinner("Generating your framework-aligned reflection..."):
                    prompt = f"""
You are an advisor helping a UNLV {role.lower()} reflect on their use of AI using the UNLV AI Framework. 
The framework includes these domains: Technical Understanding, Evaluation and Critical Thinking, Practical Integration, and Ethical and Human-Centered Use.

Here is their input:
Use case: {use_case}
Goals: {goals}
Concerns: {concerns}

Summarize their reflections across the four domains, pointing out strengths, risks, and opportunities to improve alignment. Be supportive and constructive.
"""

                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a reflection coach using the UNLV AI Framework."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.6
                    )
                    result = response.choices[0].message.content

                    st.markdown("### 🧠 Framework-Based Reflection Summary")
                    st.markdown(result)

                    st.download_button(
                        label="📥 Download Summary",
                        data=result,
                        file_name="framework_reflection.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"Something went wrong: {e}")
