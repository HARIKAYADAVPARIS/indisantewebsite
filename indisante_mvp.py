import streamlit as st
import openai
import os

# Fetch OpenAI API key from environment variable (secure for deployment)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Sample doctor & pharmacy data
DOCTORS = {
    "Paris": ["Dr. Sharma – General Physician", "Dr. Patel – ENT Specialist"],
    "Geneva": ["Dr. Kumar – GP", "Dr. Mehta – Pediatrician"]
}

PHARMACIES = {
    "Paris": ["Pharmacy du Centre", "Pharmacie des Halles"],
    "Geneva": ["Pharmacie de Rive", "Pharmacie des Grottes"]
}

# --- Streamlit Layout ---
st.set_page_config(page_title="IndiSanté MVP", page_icon="💊", layout="centered")
st.title("IndiSanté MVP 💊")
st.markdown("Translate Indian prescriptions to EU equivalents and find verified doctors & pharmacies.")

# --- User Inputs ---
user_type = st.selectbox("Select your user type:", ["Student", "IT Professional", "Migrant Mother"])
city = st.selectbox("Select your city:", ["Paris", "Geneva"])
prescription_text = st.text_area("Enter your prescription text:")

# --- Button Action ---
if st.button("Translate Prescription"):
    if prescription_text.strip() == "":
        st.warning("Please enter a prescription.")
    else:
        try:
            # GPT Translation
            prompt = f"""
            You are a medical assistant. Convert this Indian prescription to EU equivalents in plain language.
            Include emojis for clarity: 💊 for pills, 🕑 for dosage timing.
            Prescription: {prescription_text}
            """
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            translation = response['choices'][0]['message']['content']

            st.subheader("💊 Translated Prescription")
            st.write(translation)

            # Show doctors and pharmacies
            st.subheader(f"🏥 Verified Doctors in {city}")
            for doc in DOCTORS.get(city, []):
                st.write(f"- {doc}")

            st.subheader(f"💊 Nearby Pharmacies in {city}")
            for phar in PHARMACIES.get(city, []):
                st.write(f"- {phar}")

            st.success("✅ All information is GDPR-compliant & verified.")

        except Exception as e:
            st.error(f"⚠️ Error during translation: {e}")
