import streamlit as st
from openai import OpenAI
import base64

# ===========================
# Page Setup
# ===========================
st.set_page_config(
    page_title="🎭 Role-based Creative Chatbot + Image Studio",
    page_icon="🎨",
    layout="wide"
)

st.title("🎭 Role-based Creative Chatbot + Image Studio")
st.markdown("Enter your own OpenAI API Key to chat and generate images! 🎨")

# ===========================
# User Input: OpenAI Key
# ===========================
user_api_key = st.text_input(
    "Enter your OpenAI API Key:", 
    type="password",
    help="Your OpenAI API Key will only be used for this session."
)

# ===========================
# Define Roles
# ===========================
roles = {
    "Film Critic": "You are a sharp and insightful film critic with expertise in film analysis and visual storytelling.",
    "Fashion Consultant": "You are an energetic fashion consultant giving trendy and personalized style advice.",
    "Dance Coach": "You are a professional dance coach giving detailed guidance on rhythm, moves, and stage performance.",
    "Digital Artist": "You are a digital artist providing vivid, imaginative prompts for visual art and image creation.",
    "Creative Writing Mentor": "You are a creative writing mentor helping craft emotional, vivid, and expressive writing."
}

st.sidebar.header("🧠 Choose a Role")
role = st.sidebar.selectbox("Select a role for the chatbot:", list(roles.keys()))
role_prompt = roles[role]

st.sidebar.markdown("---")
enable_image = st.sidebar.checkbox("Enable Image Generation")

# ===========================
# Chat Section
# ===========================
st.subheader(f"💬 Chat with {role}")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_area("Enter your message here:", height=120)

if st.button("Send Message"):
    if not user_api_key.strip():
        st.warning("Please enter your OpenAI API Key!")
    elif not user_input.strip():
        st.warning("Please enter a message to send!")
    else:
        try:
            client = OpenAI(api_key=user_api_key)
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": role_prompt},
                        *st.session_state.chat_history
                    ]
                )
                ai_reply = response.choices[0].message.content
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
        except Exception as e:
            st.error(f"Chat failed: {e}")

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**🧍 You:** {chat['content']}")
    else:
        st.markdown(f"**🎭 {role}:** {chat['content']}")

# ===========================
# Image Generation Section
# ===========================
st.markdown("---")
st.subheader("🎨 Image Studio")

image_prompt = st.text_input(
    "Describe your image idea (e.g., 'A dreamy sunset over a neon city skyline'):"
)

if st.button("Generate Image"):
    if not user_api_key.strip():
        st.warning("Please enter your OpenAI API Key!")
    elif image_prompt.strip() == "":
        st.warning("Please enter an image prompt!")
    elif enable_image:
        try:
            client = OpenAI(api_key=user_api_key)
            with st.spinner("Generating image..."):
                result = client.images.generate(
                    model="gpt-image-1",  # or "dall-e-3" if supported
                    prompt=image_prompt,
                    size="1024x1024"
                )

                # ✅ Decode base64 image data
                image_base64 = result.data[0].b64_json
                image_bytes = base64.b64decode(image_base64)

                # ✅ Display image
                st.image(image_bytes, caption="🎨 AI-generated image", use_container_width=True)
        except Exception as e:
            st.error(f"Image generation failed: {e}\n(Make sure your API Key supports image generation)")

# ===========================
# Footer
# ===========================
st.markdown("---")
st.caption("Created with ❤️ · Each user uses their own OpenAI API Key · Powered by OpenAI & Streamlit")

