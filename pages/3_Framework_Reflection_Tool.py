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
               # Build dynamic reflection input based on what's answered
reflections = []

if q1.strip():
    reflections.append(f"Q1 - AI in current/future work:\n{q1}")
if q2.strip():
    reflections.append(f"Q2 - What feels promising:\n{q2}")
if q3.strip():
    reflections.append(f"Q3 - Concerns or tensions:\n{q3}")
if q4.strip():
    reflections.append(f"Q4 - Values and priorities:\n{q4}")

user_input = "\n\n".join(reflections)

prompt = f"""
You are a supportive reflection coach helping a {role.lower()} at UNLV think about their use of AI.

Use the UNLV AI Framework as your guide. The framework includes four domains:
- Technical Understanding
- Evaluation and Critical Thinking
- Practical Integration
- Ethical and Human-Centered Use

Read their reflections and respond using only the framework domains that are relevant to what they shared. Do not mention or reflect on questions they left blank. You may skip a domain entirely if it is not relevant.

Reference the framework where appropriate, and use phrases like “this connects well to the UNLV AI Framework’s emphasis on…”

Keep your tone thoughtful, encouraging, and reflective—not evaluative.

Here are their reflections:
{user_input}
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
