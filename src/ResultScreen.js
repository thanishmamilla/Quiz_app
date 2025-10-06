import React from 'react';

function ResultScreen({ scoreData, onRestart }) {
  if (!scoreData) {
    return <p>Processing results...</p>;
  }

  const { score, total_questions, results } = scoreData;

  return (
    <div className="result-screen">
      <h2>Quiz Complete!</h2>
      <p className="final-score">
        Your Score: **{score} out of {total_questions}**
      </p>

      <h3>Review Your Answers (✨ BONUS)</h3>
      <div className="results-review-list">
        {results.map((r, index) => (
          <div key={r.id} className={`result-item ${r.is_correct ? 'correct' : 'incorrect'}`}>
            <p className="review-question-text">
              {index + 1}. {r.text}
            </p>
            <p>
              **Your Answer:** {r.user_answer_index !== -1 ? 'Option ' + (r.user_answer_index + 1) : 'Skipped'}
            </p>
            <p>
              **Correct Answer:** {r.correct_answer_text}
            </p>
            <span className="status-indicator">
              {r.is_correct ? '✅ Correct' : '❌ Incorrect'}
            </span>
          </div>
        ))}
      </div>

      <button onClick={onRestart} className="restart-button">
        Try Another Quiz
      </button>
    </div>
  );
}

export default ResultScreen;