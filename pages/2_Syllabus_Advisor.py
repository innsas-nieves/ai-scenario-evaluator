import streamlit as st
import openai

st.set_page_config(page_title="Syllabus Advisor", layout="centered")

st.title("📝 Syllabus Advisor")
st.write("Paste in a course syllabus below to get AI-generated feedback based on the UNLV AI Framework.")

# Syllabus input
syllabus_text = st.text_area("📄 Paste your syllabus here:", height=300)

# API key
api_key = st.text_input("🔑 Enter your OpenAI API key:", type="password")

# Submit
if st.button("Analyze Syllabus"):
    if not syllabus_text.strip():
        st.warning("Please paste in a syllabus.")
    elif not api_key:
        st.warning("Please enter your OpenAI API key.")
    else:
        try:
            client = openai.OpenAI(api_key=api_key)
            with st.spinner("Analyzing your syllabus..."):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an AI assistant helping UNLV instructors review their syllabi based on the UNLV AI Framework. "
                                "The framework emphasizes four domains: Technical Understanding, Evaluation and Critical Thinking, Practical Integration, and Ethical and Human-Centered Use. "
                                "For each syllabus, return feedback in this structure:\n\n"
                                "### ✅ Strengths\n"
                                "### ⚠️ Areas for Improvement\n"
                                "### 📌 Suggestions Based on the Framework\n"
                                "### 💭 Questions to Consider"
                            ),
                        },
                        {"role": "user", "content": syllabus_text}
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
