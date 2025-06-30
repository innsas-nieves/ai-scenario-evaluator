import streamlit as st
import openai

st.set_page_config(page_title="AI Scenario Evaluator", layout="centered")

st.title("🧠 AI Scenario Evaluator")

st.write("""
Use this tool to describe a real or hypothetical AI-related scenario. The evaluator will return GPT-powered feedback based on the UNLV AI Framework, highlighting strengths, risks, and areas to strengthen alignment.

You can describe situations like:
- A student using ChatGPT to generate a paper
- An administrator considering AI for hiring or communication
- A researcher summarizing literature with AI tools
""")

# Example scenarios
example_scenarios = {
    "Select an example...": "",
    "A student uses ChatGPT to write their weekly reflections": "A student submits weekly journal reflections. You suspect they are using ChatGPT because the tone and structure have changed.",
    "A faculty member uses AI to draft assessment rubrics": "An instructor uses GPT-4 to create draft rubrics for an upper-division writing course.",
    "An administrator wants to use AI to screen job applications": "An HR administrator wants to use AI to rank job candidates based on cover letters and CVs.",
    "A researcher uses AI to summarize article PDFs": "A faculty member uploads PDFs to a tool that summarizes literature and generates citations for grant proposals."
}

selected_example = st.selectbox("🔍 Or choose a prewritten scenario to try:", list(example_scenarios.keys()))
scenario_text = example_scenarios[selected_example]

scenario_input = st.text_area("✏️ Describe your scenario involving AI use:", value=scenario_text, height=200)

# Submit
if st.button("Evaluate Scenario"):
    if not scenario_input.strip():
        st.warning("Please describe a scenario.")
    else:
        try:
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            with st.spinner("Analyzing your scenario using the UNLV AI Framework..."):
                prompt = f"""
You are an AI advisor helping a member of the UNLV community evaluate their use of AI. Use the UNLV AI Framework as your guide, which includes these domains:
- Technical Understanding
- Evaluation and Critical Thinking
- Practical Integration
- Ethical and Human-Centered Use

Read the scenario and offer feedback using any domains that apply. Do not include domains that are not relevant. Your response should be structured with:
### ✅ What the scenario gets right
### ⚠️ Areas to reconsider or clarify
### 📌 Suggestions based on the framework
### 💭 Questions to ask the team or individual

Here is the scenario:
{scenario_input}
"""

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a university AI advisor using the UNLV AI Framework."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.6
                )

                result = response.choices[0].message.content

                st.markdown("### 🧠 Framework-Based Feedback")
                st.markdown("---")

                formatted_result = result.replace("###", "####").replace("\n\n", "\n\n---\n\n")
                st.markdown(formatted_result)

                st.download_button(
                    label="📥 Download Evaluation",
                    data=result,
                    file_name="scenario_evaluation.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Something went wrong: {e}")
