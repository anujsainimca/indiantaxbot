import streamlit as st
from groq import Groq

# System prompt (fixed for tax assistant role)
system_prompt = """
You are an Indian Income Tax Assistant with expertise in Indian taxation laws, rules, and compliance.
Provide clear, accurate, and professional information strictly related to income tax matters in India, 
including assessment procedures, exemptions, deductions, TDS, tax filing, advance tax, notices, appeals, 
and compliance under the Income-tax Act, 1961. 
Avoid providing information unrelated to taxation (such as GST, company law, or foreign tax systems) unless explicitly asked within the scope of Indian income tax. 
Ensure that your responses are well-structured, easy to understand, and aligned with the latest provisions of the Indian Income-tax Department.
"""

# Streamlit UI
st.title("💼 Indian Income Tax Assistant")
st.write("Ask me anything about Indian Income Tax (under the Income-tax Act, 1961).")

# API Key input
api_key = st.text_input("🔑 Enter your Groq API Key:", type="password")

# Query input
user_message = st.text_area("Enter your query:", placeholder="E.g. What are the current tax slabs?")

if st.button("Get Answer"):
    if not api_key.strip():
        st.error("Please enter your Groq API key.")
    elif not user_message.strip():
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Fetching tax information..."):
            client = Groq(api_key=api_key)

            chat_completion = client.chat.completions.create(
                model="compound-beta",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.3,
            )
            
            bot_response = chat_completion.choices[0].message.content
            
            # Show response
            st.subheader("📌 Answer")
            st.write(bot_response)

            # Show metadata (optional)
            st.subheader("ℹ️ Metadata")
            st.json({
                "id": chat_completion.id,
                "model": chat_completion.model,
                "created": chat_completion.created,
                "usage": {
                    "prompt_tokens": chat_completion.usage.prompt_tokens,
                    "completion_tokens": chat_completion.usage.completion_tokens,
                    "total_tokens": chat_completion.usage.total_tokens,
                }
            })
