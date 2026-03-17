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
    file_path = Path("questions/phase-1-structured.json")
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        st.error("Questions file not found!")
        return []

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    
if 'answers' not in st.session_state:
    st.session_state.answers = {}
    
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Main app
def main():
    st.title("🥋 BJJ Skill Questionnaire - Phase 1")
    st.markdown("---")
    
    # Load questions
    questions = load_questions()
    
    if not questions:
        st.error("No questions found. Please check the questions file.")
        return
    
    # Sidebar with progress
    with st.sidebar:
        st.header("Progress")
        progress = (st.session_state.current_question) / len(questions)
        st.progress(progress)
        st.write(f"Question {st.session_state.current_question + 1} of {len(questions)}")
        
        # Reset button
        if st.button("Reset Quiz"):
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.experimental_rerun()
    
    # Display current question or results
    if st.session_state.current_question < len(questions) and not st.session_state.submitted:
        display_question(questions[st.session_state.current_question])
    elif st.session_state.submitted:
        display_results(questions)
    else:
        # Move to results if all questions answered
        st.session_state.submitted = True
        st.experimental_rerun()

def display_question(question):
    """Display a single question with options"""
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
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("Previous") and st.session_state.current_question > 0:
            st.session_state.current_question -= 1
            st.experimental_rerun()
    
    with col2:
        if st.button("Next"):
            if st.session_state.current_question < len(load_questions()) - 1:
                st.session_state.current_question += 1
                st.experimental_rerun()
            else:
                # Last question, submit
                st.session_state.submitted = True
                st.experimental_rerun()
    
    with col3:
        if st.button("Submit Quiz"):
            st.session_state.submitted = True
            st.experimental_rerun()

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
    
    # Calculate score
    correct_answers = 0
    total_questions = len(questions)
    
    # Display each question with user's answer and correct answer
    for i, question in enumerate(questions):
        user_answer = st.session_state.answers.get(question['id'], "Not answered")
        correct_answer = question['correct_answer']
        
        # Check if answer is correct
        is_correct = user_answer == correct_answer
        
        if is_correct:
            correct_answers += 1
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
    st.metric("Score", f"{correct_answers}/{total_questions}", f"{score_percentage:.1f}%")
    
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

if __name__ == "__main__":
    main()