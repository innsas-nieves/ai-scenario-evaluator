import streamlit as st
import openai

st.set_page_config(page_title="Framework Reflection Tool", layout="centered")

st.title("🧭 Framework Reflection Tool")
st.write("Reflect on how your use of AI aligns with UNLV's values and priorities. You can answer any or all of the questions below.")

# Role selection
role = st.selectbox("👤 What is your role?", ["Select...", "Instructor", "Administrator", "Researcher"])

# Questions (any can be answered)
q1 = st.text_area("1. What is one way AI is already showing up in your work, or could be in the future?", height=100)
q2 = st.text_area("2. What feels promising or exciting about that possibility?", height=100)
q3 = st.text_area("3. What concerns, questions, or tensions are on your mind?", height=100)
q4 = st.text_area("4. What values or priorities do you want to keep in focus as you use AI?", height=100)

# OpenAI API key
api_key = st.text_input("🔑 Enter your OpenAI API key:", type="password")

# Submit
if st.button("Generate Reflection Summary"):
    if not any([q1.strip(), q2.strip(), q3.strip(), q4.strip()]):
        st.warning("You can answer as many or as few questions as you'd like, but at least one response is required.")
    elif not api_key:
        st.warning("Please enter your OpenAI API key.")
    else:
        try:
            client = openai.OpenAI(api_key=api_key)
            with st.spinner("Generating your framework-aligned reflection..."):
                prompt = f"""
You are a supportive reflection coach helping a {role.lower()} at UNLV think about their use of AI.

Use the UNLV AI Framework to guide your response. The framework includes four domains:
1. Technical Understanding
2. Evaluation and Critical Thinking
3. Practical Integration
4. Ethical and Human-Centered Use

Summarize the user’s reflections across these domains using a warm, conversational tone. If they skipped a question, you can skip that area or respond briefly. Offer encouragement and thoughtful questions they might explore further.

Here are their responses:
Q1: {q1}
Q2: {q2}
Q3: {q3}
Q4: {q4}
"""

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a reflective coach using the UNLV AI Framework."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.6
                )
                result = response.choices[0].message.content

                st.markdown("### 🧠 Framework-Based Reflection Summary")
                st.markdown("---")
                formatted_result = result.replace("###", "####").replace("\n\n", "\n\n---\n\n")
                st.markdown(formatted_result)

                st.download_button(
                    label="📥 Download Summary",
                    data=result,
                    file_name="framework_reflection.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Something went wrong: {e}")
