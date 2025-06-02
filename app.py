import streamlit as st
import openai
import os

st.set_page_config(page_title="UNLV AI Scenario Evaluator")

st.title("🤖 UNLV AI Scenario Evaluator")
st.write("Use this tool to describe a scenario involving AI (e.g., student use, hiring process, faculty workflow). It will return recommendations based on the UNLV AI Framework.")

# User input
scenario = st.text_area("🔍 Describe your scenario involving AI use:", height=200)

# OpenAI API key input
openai_api_key = st.text_input("🔑 Enter your OpenAI API key:", type="password")

# Submit button
if st.button("Evaluate Scenario"):
    if not openai_api_key:
        st.warning("Please enter your OpenAI API key.")
    elif not scenario.strip():
        st.warning("Please describe a scenario to evaluate.")
    else:
        with st.spinner("Analyzing using the UNLV AI Framework..."):
            try:
                client = openai.OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an AI advisor helping UNLV faculty, staff, or administrators evaluate real-world AI scenarios "
                                "using the UNLV AI Framework. This framework emphasizes four domains: Technical Understanding, Evaluation "
                                "and Critical Thinking, Practical Integration, and Ethical and Human-Centered Use. When a user shares a scenario, "
                                "analyze it using those domains. Point out strengths, risks, and areas for improvement. Make the tone practical, helpful, and clear."
                            ),
                        },
                        {"role": "user", "content": scenario}
                    ],
                    temperature=0.6
                )
                result = response.choices[0].message.content
                st.markdown("### 🧠 Framework-Based Feedback")
                st.write(result)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
