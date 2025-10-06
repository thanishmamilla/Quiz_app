import React, { useState, useEffect } from 'react';

function QuizView({ questions, duration, onSubmit }) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({}); // { questionId: selectedIndex }
  const [timeLeft, setTimeLeft] = useState(duration);

  // --- Timer Logic (✨ BONUS) ---
  useEffect(() => {
    if (questions.length === 0) return; // Wait for questions to load
    if (timeLeft <= 0) {
      handleSubmission();
      return;
    }

    const timerId = setInterval(() => {
      setTimeLeft(prevTime => prevTime - 1);
    }, 1000);

    return () => clearInterval(timerId); // Cleanup
  }, [timeLeft, questions]);

  // --- Handlers ---
  
  const handleOptionChange = (questionId, optionIndex) => {
    setUserAnswers(prev => ({
      ...prev,
      [questionId]: optionIndex
    }));
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const handlePrev = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };
  
  const handleSubmission = () => {
    // Stop the timer by setting time to 0
    setTimeLeft(0); 
    onSubmit(userAnswers);
  };

  // --- Render ---

  if (questions.length === 0) {
    return <p>Loading questions...</p>;
  }
  
  const currentQuestion = questions[currentQuestionIndex];
  const isLastQuestion = currentQuestionIndex === questions.length - 1;

  return (
    <div className="quiz-view">
      <div className="quiz-header">
        <h2>Question {currentQuestionIndex + 1} of {questions.length}</h2>
        <div className={`timer ${timeLeft <= 10 ? 'timer-critical' : ''}`}>
          Time Left: {timeLeft > 0 ? timeLeft : 0}s
        </div>
      </div>

      <p className="question-text">{currentQuestion.text}</p>
      
      <div className="options-list">
        {currentQuestion.options.map((option, index) => (
          <label key={index} className="option-label">
            <input
              type="radio"
              name={`question-${currentQuestion.id}`}
              value={index}
              checked={userAnswers[currentQuestion.id] === index}
              onChange={() => handleOptionChange(currentQuestion.id, index)}
            />
            {option}
          </label>
        ))}
      </div>

      <div className="navigation-controls">
        <button 
          onClick={handlePrev} 
          disabled={currentQuestionIndex === 0}
        >
          Previous
        </button>
        
        {isLastQuestion ? (
          <button onClick={handleSubmission} className="submit-button">
            Submit Quiz
          </button>
        ) : (
          <button onClick={handleNext}>
            Next
          </button>
        )}
      </div>
    </div>
  );
}

export default QuizView;