
import streamlit as st
import openai
import time

st.set_page_config(page_title="AI Story Builder", layout="wide")
st.title("📖 AI Story Builder with Structure")

# --- API Key ---
openai_api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# --- Story Prompt and Structure ---
prompt = st.text_area("🧠 Enter your story theme or premise", height=100, value="A poor man inherits an empire from his ex-wife's will.")
num_sections = st.number_input("📋 Number of Sections", min_value=1, max_value=20, value=5)

structure = []
st.subheader("✏️ Story Structure")
for i in range(num_sections):
    col1, col2 = st.columns([2, 1])
    with col1:
        title = st.text_input(f"Section {i+1} Title", key=f"title_{i}")
    with col2:
        word_count = st.number_input(f"Words", min_value=100, max_value=3000, value=500, step=100, key=f"word_{i}")
    structure.append({"title": title, "words": word_count})

# --- Function to Call OpenAI ---
def generate_section(title, words, theme):
    prompt_template = f"""You are a professional storyteller. Write a dramatic and emotionally engaging story section titled "{title}" based on the following theme:

    {theme}

    The section should be approximately {words} words long and written in a compelling narrative style."""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional fiction writer."},
            {"role": "user", "content": prompt_template}
        ],
        temperature=0.8,
        max_tokens=int(words * 1.4),
    )
    return response.choices[0].message.content.strip()

# --- Generate Story ---
if st.button("🚀 Generate Story"):
    if not openai_api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        openai.api_key = openai_api_key
        full_story = ""
        for sec in structure:
            with st.spinner(f"Generating: {sec['title']}..."):
                try:
                    section_text = generate_section(sec["title"], sec["words"], prompt)
                    st.markdown(f"### {sec['title']}")
                    st.write(section_text)
                    full_story += f"{sec['title']}\n{section_text}\n\n"
                    time.sleep(1)
                except Exception as e:
                    st.error(f"Error generating section '{sec['title']}': {str(e)}")

        st.download_button("📥 Download Full Story", full_story, file_name="generated_story.txt")
