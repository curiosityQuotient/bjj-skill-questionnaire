import streamlit as st
import json
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="BJJ Skill Questionnaire",
    page_icon="🥋",
    layout="wide"
)

# Load questions from JSON file
def load_questions():
    """Load questions from the JSON file"""
    file_path = Path("questions/short-test-structured.json")
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        st.error("Questions file not found!")
        return []

# Initialize session state
if 'answers' not in st.session_state:
    st.session_state.answers = {}
    
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Main app
def main():
    st.title("🥋 BJJ Skill Questionnaire - Short Test")
    st.markdown("---")
    
    # Load questions
    questions = load_questions()
    
    if not questions:
        st.error("No questions found. Please check the questions file.")
        return
    
    # Display all questions on one page
    display_all_questions(questions)
    
    # Submit button
    if st.button("Submit Answers"):
        st.session_state.submitted = True
        st.rerun()
    
    # Show results if submitted
    if st.session_state.submitted:
        display_results(questions)

def display_all_questions(questions):
    """Display all questions at once"""
    st.header("Questions")
    
    # Store answers in session state as we go
    for question in questions:
        st.subheader(f"Question {question['id']}")
        st.markdown(f"**{question['question']}**")
        
        # Get user's previous answer if exists
        user_answer = st.session_state.answers.get(question['id'], None)
        
        # Display options as radio buttons
        answer = st.radio(
            "Select your answer:",
            options=[option['letter'] for option in question['options']],
            format_func=lambda x: f"{x}. {get_option_text(question['options'], x)}",
            index=get_option_index(question['options'], user_answer) if user_answer else 0,
            key=f"q_{question['id']}"
        )
        
        # Save answer
        st.session_state.answers[question['id']] = answer
        st.markdown("---")

def get_option_text(options, letter):
    """Get the text for an option by its letter"""
    for option in options:
        if option['letter'] == letter:
            return option['text']
    return ""

def get_option_index(options, letter):
    """Get the index of an option by its letter"""
    for i, option in enumerate(options):
        if option['letter'] == letter:
            return i
    return 0

def display_results(questions):
    """Display quiz results"""
    st.header("Quiz Results")
    
    # Calculate overall score
    correct_answers = 0
    total_questions = len(questions)
    
    # Calculate topic-based scores
    topic_scores = {}
    topic_totals = {}
    
    # Initialize topic tracking
    for question in questions:
        topic = question.get('topic', 'Unknown')
        if topic not in topic_scores:
            topic_scores[topic] = 0
            topic_totals[topic] = 0
        topic_totals[topic] += 1
    
    # Display each question with user's answer and correct answer
    for i, question in enumerate(questions):
        user_answer = st.session_state.answers.get(question['id'], "Not answered")
        correct_answer = question['correct_answer']
        
        # Check if answer is correct
        is_correct = user_answer == correct_answer
        
        # Update scores
        if is_correct:
            correct_answers += 1
            topic = question.get('topic', 'Unknown')
            topic_scores[topic] += 1
            st.success(f"**Question {question['id']}:** ✅ Correct")
        else:
            st.error(f"**Question {question['id']}:** ❌ Incorrect")
        
        st.markdown(f"**Question:** {question['question']}")
        st.markdown(f"**Your answer:** {user_answer}. {get_option_text(question['options'], user_answer)}")
        st.markdown(f"**Correct answer:** {correct_answer}. {get_option_text(question['options'], correct_answer)}")
        st.markdown("---")
    
    # Final score
    score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    st.subheader("Final Score")
    st.metric("Overall Score", f"{correct_answers}/{total_questions}", f"{score_percentage:.1f}%")
    
    # Topic-based scores
    st.subheader("Topic-Based Scores")
    cols = st.columns(min(len(topic_scores), 3))
    for i, (topic, correct) in enumerate(topic_scores.items()):
        total = topic_totals[topic]
        percentage = (correct / total) * 100 if total > 0 else 0
        col = cols[i % len(cols)]
        col.metric(topic, f"{correct}/{total}", f"{percentage:.0f}%")
    
    # Performance message
    if score_percentage >= 90:
        st.balloons()
        st.success("🏆 Excellent! You have mastered these BJJ fundamentals!")
    elif score_percentage >= 70:
        st.info("👍 Good job! You have a solid understanding of these techniques.")
    elif score_percentage >= 50:
        st.warning("📚 Keep studying! Review these concepts to improve your knowledge.")
    else:
        st.error("📖 Time to hit the books! These fundamentals are crucial for your BJJ development.")
    
    # Reset button
    if st.button("Reset Quiz"):
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.rerun()

if __name__ == "__main__":
    main()