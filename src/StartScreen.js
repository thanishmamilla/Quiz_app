// import React from 'react';

// function StartScreen({ quizzes, onStart }) {
//   if (quizzes.length === 0) {
//     return <p>Loading quizzes or no quizzes available...</p>;
//   }

//   return (
//     <div className="start-screen">
//       <h2>Welcome! Select a Quiz to Begin</h2>
//       {quizzes.map(quiz => (
//         <button 
//           key={quiz.id}
//           className="quiz-start-button"
//           onClick={() => onStart(quiz.id)}
//         >
//           Start: {quiz.title}
//         </button>
//       ))}
//     </div>
//   );
// }

// export default StartScreen;



import React from 'react';
import { useAuth } from './AuthContext'; 

function StartScreen({ quizzes, onStart, onViewResults }) {
  const { isAuthenticated, getStoredScores } = useAuth();
  
  // Get all completed quiz scores for the current user
  const completedQuizzes = isAuthenticated ? getStoredScores() : {};
  
  if (quizzes.length === 0) {
    return <p>Loading quizzes or no quizzes available...</p>;
  }

  return (
    <div className="start-screen">
      <h2>Welcome! Select a Quiz to Begin</h2>
      {quizzes.map(quiz => {
        const quizId = String(quiz.id);
        const isCompleted = completedQuizzes.hasOwnProperty(quizId);
        const scoreInfo = completedQuizzes[quizId];
        
        return (
          <button 
            key={quizId}
            className={`quiz-start-button ${isCompleted ? 'view-results-button' : ''}`}
            onClick={() => {
              if (isCompleted) {
                // If completed, trigger viewResults with the stored data
                onViewResults(quizId, scoreInfo);
              } else {
                // Otherwise, start the quiz
                onStart(quiz.id);
              }
            }}
          >
            {isCompleted 
              ? `View Results: ${quiz.title} (${scoreInfo.score}/${scoreInfo.total_questions})`
              : `Start: ${quiz.title}`}
          </button>
        );
      })}
    </div>
  );
}

export default StartScreen;