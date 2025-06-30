import streamlit as st
import openai

st.set_page_config(page_title="Syllabus Advisor", layout="centered")

st.title("📝 Syllabus Advisor")

st.write("""
Paste your course syllabus below to receive feedback on how clearly and ethically it addresses AI-related expectations.

The advisor will consider:
- Transparency and clarity
- Academic integrity
- Equity and access
- Ethical alignment with the UNLV AI Framework
""")

# Input
syllabus_text = st.text_area("📄 Paste your syllabus here:", height=300)

# Submit
if st.button("Analyze Syllabus"):
    if not syllabus_text.strip():
        st.warning("Please paste in a syllabus.")
    else:
        try:
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            with st.spinner("Analyzing your syllabus..."):
                prompt = f"""
You are an advisor helping a UNLV instructor review their syllabus based on the UNLV AI Framework. The framework includes four domains:
- Technical Understanding
- Evaluation and Critical Thinking
- Practical Integration
- Ethical and Human-Centered Use

Provide constructive feedback in four sections:
### ✅ Strengths
### ⚠️ Areas for Improvement
### 📌 Suggestions Based on the Framework
### 💭 Questions to Consider

Here is the syllabus text:
{syllabus_text}
"""

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a syllabus advisor using the UNLV AI Framework."},
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
                    label="📥 Download Feedback",
                    data=result,
                    file_name="syllabus_feedback.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Something went wrong: {e}")
