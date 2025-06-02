import streamlit as st
import openai
import os

st.set_page_config(page_title="UNLV AI Scenario Evaluator", layout="centered")

st.title("🤖 UNLV AI Scenario Evaluator")
st.write("Use this tool to describe a scenario involving AI (e.g., student use, hiring process, faculty workflow). It will return recommendations based on the UNLV AI Framework.")

# Example scenarios
example_scenarios = {
    "Select an example...": "",
    "A student uses ChatGPT to write their weekly reflections": "A student submits weekly journal reflections. You suspect they are using ChatGPT because the tone and structure have changed.",
    "A faculty member uses AI to draft assessment rubrics": "An instructor uses GPT-4 to create draft rubrics for an upper-division writing course.",
    "An administrator wants to use AI to screen job applications": "An HR administrator wants to use AI to rank job candidates based on cover letters and CVs.",
    "A researcher uses AI to summarize article PDFs": "A faculty member uploads PDFs to a tool that summarizes literature and generates citations for grant proposals."
}

# Scenario selection
selected_example = st.selectbox("🔍 Or choose a prewritten scenario to try:", list(example_scenarios.keys()))
scenario_text = example_scenarios[selected_example]

# User input
scenario_input = st.text_area("✏️ Describe your scenario involving AI use:", value=scenario_text, height=200)

# OpenAI API key
api_key = st.text_input("🔑 Enter your OpenAI API key:", type="password")

# GPT call
if st.button("Evaluate Scenario"):
    if not scenario_input.strip():
        st.warning("Please describe a scenario.")
    elif not api_key:
        st.warning("Please enter your OpenAI API key.")
    else:
        try:
            client = openai.OpenAI(api_key=api_key)
            with st.spinner("Evaluating your scenario using the UNLV AI Framework..."):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an AI advisor helping UNLV faculty, staff, or administrators evaluate real-world AI scenarios using the UNLV AI Framework. "
                                "This framework emphasizes four domains: Technical Understanding, Evaluation and Critical Thinking, Practical Integration, and Ethical and Human-Centered Use. "
                                "For each scenario, return a structured analysis with these four sections:\n\n"
                                "### ✅ What the scenario gets right\n"
                                "### ⚠️ Areas to reconsider or clarify\n"
                                "### 📌 Suggestions based on the framework\n"
                                "### 💭 Questions to ask the team or individual"
                            ),
                        },
                        {"role": "user", "content": scenario_input}
                    ],
                    temperature=0.6
                )
                result = response.choices[0].message.content
                st.markdown("### 🧠 Framework-Based Feedback")
                st.markdown("---")

# Add structured formatting around GPT response
formatted_response = result.replace("###", "####").replace("\n\n", "\n\n---\n\n")
st.markdown(formatted_response)


                st.download_button(
                    label="📥 Download Evaluation",
                    data=result,
                    file_name="scenario_evaluation.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Footer and Learn More
st.markdown("---")

st.markdown("""
📚 **Learn more about the UNLV AI Framework**  
[View the full PDF](https://your-link-to-the-framework.pdf)

---

🛠️ *Built by the UNLV Instructional Technology Team*  
Questions? Contact [alethea.inns@unlv.edu](mailto:alethea.inns@unlv.edu)
""")
