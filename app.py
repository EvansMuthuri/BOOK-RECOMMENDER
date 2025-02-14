from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_book_recommendations(category, preferences, num_books=5):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Act as an experienced librarian and book critic. Recommend {num_books} books for the category: {category}.
    Consider these additional preferences: {preferences}
    
    For each book, provide:
    1. Title and Author
    2. Brief description (2-3 sentences)
    3. Why it's recommended for this reader
    4. Reading difficulty level (Beginner/Intermediate/Advanced)
    
    Format each recommendation clearly with proper spacing and organization.
    """
    
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.set_page_config(page_title="Book Recommendation System")
st.header("📚 Personal Book Recommender")
st.write("Get personalized book recommendations based on your interests!")

# Categories
categories = [
    "Personal Finance & Investment",
    "Personal Growth & Self-Help",
    "Science Fiction & Fantasy",
    "Productivity & Time Management",
    "Programming & Technology",
    "Business & Entrepreneurship",
    "Psychology & Mental Health",
    "History & Biography",
    "Philosophy & Critical Thinking",
    "Health & Wellness"
]

# User inputs
selected_category = st.selectbox("Choose a category:", categories)

# Additional preferences
st.subheader("Additional Preferences")
col1, col2 = st.columns(2)

with col1:
    reading_level = st.select_slider(
        "Reading Level",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Intermediate"
    )
    
    book_length = st.select_slider(
        "Preferred Book Length",
        options=["Short", "Medium", "Long"],
        value="Medium"
    )

with col2:
    writing_style = st.multiselect(
        "Preferred Writing Style",
        ["Practical", "Academic", "Conversational", "Story-based"],
        default=["Practical"]
    )
    
    specific_topics = st.text_area(
        "Any specific topics or themes you're interested in?",
        placeholder="E.g., AI in healthcare, medieval fantasy, startup funding..."
    )

num_recommendations = st.slider("Number of recommendations", 3, 10, 5)

# Compile preferences
preferences = f"""
- Reading Level: {reading_level}
- Book Length: {book_length}
- Writing Style: {', '.join(writing_style)}
- Specific Interests: {specific_topics}
"""

if st.button("Get Recommendations"):
    with st.spinner("Finding the perfect books for you..."):
        try:
            recommendations = get_book_recommendations(
                selected_category,
                preferences,
                num_recommendations
            )
            
            st.subheader("📖 Your Personalized Book Recommendations")
            st.write(recommendations)
            
            st.info("""
            💡 Note: These recommendations are generated based on AI analysis. 
            It's always good to read reviews and previews before making a final decision.
            """)
            
        except Exception as e:
            st.error("Oops! Something went wrong. Please try again or check your API key configuration.")
            st.error(str(e))

# Add footer with additional information
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Made with for book lovers</p>
</div>
""", unsafe_allow_html=True)