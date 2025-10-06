import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const API_BASE_URL = 'http://localhost:5000/api';

// Initial structure for a new question
const initialQuestion = {
    text: '', 
    options: ['', '', '', ''], 
    correct_index: 0 // 0-based index (0, 1, 2, or 3)
};

function AdminDashboard() {
  const { token, isAdmin } = useAuth();
  const [quizTitle, setQuizTitle] = useState('');
  const [questions, setQuestions] = useState([initialQuestion]);
  const [message, setMessage] = useState('');

  if (!isAdmin) {
    return <p>Access Denied. You must be logged in as an administrator.</p>;
  }
  
  // --- Handlers for Question Form ---

  // --- Handlers for Question Form ---

const handleQuestionChange = (qIndex, field, value) => {
  const newQuestions = [...questions]; // Shallow copy of the questions array
  
  // Create a deep copy of the question object being modified
  const updatedQuestion = { ...newQuestions[qIndex] };

  if (field === 'option') {
      const [optIndex, optValue] = value;
      
      // Create a new array for options to maintain immutability
      const newOptions = [...updatedQuestion.options];
      newOptions[optIndex] = optValue;
      
      updatedQuestion.options = newOptions;
  } else {
      updatedQuestion[field] = value;
  }
  
  // Replace the old question object with the new, updated one
  newQuestions[qIndex] = updatedQuestion;
  
  setQuestions(newQuestions);
};
  
 // Corrected addQuestion
const addQuestion = () => {
    setQuestions([...questions, {
        ...initialQuestion,
        options: [...initialQuestion.options] // Create a NEW options array
    }]);
};

  const removeQuestion = (qIndex) => {
      if (questions.length > 1) {
          setQuestions(questions.filter((_, index) => index !== qIndex));
      } else {
          setMessage("A quiz must have at least one question.");
      }
  };

  // --- Submission Logic ---

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    
    // Simple validation: check for title and ensuring all questions/options are filled
    if (!quizTitle || questions.some(q => q.text === '' || q.options.some(opt => opt === ''))) {
        setMessage('Error: Please ensure the quiz title and all question fields are filled.');
        return;
    }

    const payload = { title: quizTitle, questions };

    try {
      const response = await fetch(`${API_BASE_URL}/quizzes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` // IMPORTANT: Sends the token for Admin verification
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`Success! Quiz "${quizTitle}" added successfully with ID: ${data.quiz_id}.`);
        // Reset form
        setQuizTitle('');
        setQuestions([initialQuestion]);
      } else if (response.status === 403) {
        setMessage("Error: You do not have sufficient permissions (Admin required).");
      } else {
        setMessage(`Error: ${data.msg || "Failed to add quiz."}`);
      }
    } catch (error) {
      console.error('Submission error:', error);
      setMessage("Network error. Could not connect to the server.");
    }
  };

  return (
    <div className="admin-dashboard">
      <h3>Admin Panel: Add New Quiz</h3>
      <form onSubmit={handleSubmit} className="admin-form">
        <input 
          type="text" 
          placeholder="Quiz Title (e.g., 'React Hooks Basics')" 
          value={quizTitle} 
          onChange={e => setQuizTitle(e.target.value)} 
          required 
          className="quiz-title-input"
        />
        
        {questions.map((q, qIndex) => (
            <div key={qIndex} className="question-form-block">
                <h4>Question {qIndex + 1}</h4>
                <input 
                    type="text" 
                    placeholder="Question Text" 
                    value={q.text} 
                    onChange={e => handleQuestionChange(qIndex, 'text', e.target.value)} 
                    required 
                    className="question-text-input"
                />
                
                <div className="options-grid">
                    {q.options.map((option, oIndex) => (
                        <div key={oIndex} className="option-input-group">
                            <input 
                                type="text" 
                                placeholder={`Option ${oIndex + 1}`} 
                                value={option} 
                                onChange={e => handleQuestionChange(qIndex, 'option', [oIndex, e.target.value])} 
                                required 
                            />
                            <label className="correct-label">
                                <input 
                                    type="radio" 
                                    name={`correct-q-${qIndex}`} 
                                    checked={q.correct_index === oIndex} 
                                    onChange={() => handleQuestionChange(qIndex, 'correct_index', oIndex)} 
                                />
                                Correct
                            </label>
                        </div>
                    ))}
                </div>
                
                <button 
                    type="button" 
                    onClick={() => removeQuestion(qIndex)} 
                    className="remove-q-button"
                    disabled={questions.length === 1}
                >
                    Remove Question
                </button>
            </div>
        ))}
        
        <div className="action-buttons">
            <button type="button" onClick={addQuestion} className="add-q-button">
                + Add Another Question
            </button>
            <button type="submit" className="submit-quiz-button">
                Submit New Quiz
            </button>
        </div>

        {message && <p className={message.includes('Error') ? 'error-msg' : 'success-msg'}>{message}</p>}
      </form>
    </div>
  );
}

export default AdminDashboard;