// // import React, { useState, useEffect, useCallback } from 'react';
// // import StartScreen from './StartScreen';
// // import QuizView from './QuizView';
// // import ResultScreen from './ResultScreen';
// // import './App.css'; // Add some basic styling

// // const API_BASE_URL = 'http://localhost:5000/api';
// // const QUIZ_DURATION_SECONDS = 60; // ✨ BONUS: 60 seconds per quiz

// // function App() {
// //   // States: 'start', 'in_progress', 'results'
// //   const [quizState, setQuizState] = useState('start'); 
// //   const [quizzes, setQuizzes] = useState([]);
// //   const [questions, setQuestions] = useState([]);
// //   const [selectedQuizId, setSelectedQuizId] = useState(null);
// //   const [scoreData, setScoreData] = useState(null);

// //   // --- Initial Load: Fetch Available Quizzes ---
// //   useEffect(() => {
// //     fetch(`${API_BASE_URL}/quizzes`)
// //       .then(res => res.json())
// //       .then(data => setQuizzes(data))
// //       .catch(err => console.error("Error fetching quizzes:", err));
// //   }, []);

// //   // --- Quiz Flow Handlers ---

// //   const startQuiz = useCallback((quizId) => {
// //     setSelectedQuizId(quizId);
// //     setQuizState('in_progress');
// //     // Fetch questions for the selected quiz
// //     fetch(`${API_BASE_URL}/quizzes/${quizId}/questions`)
// //       .then(res => res.json())
// //       .then(data => setQuestions(data))
// //       .catch(err => {
// //         console.error("Error fetching questions:", err);
// //         alert("Could not load quiz questions.");
// //         setQuizState('start');
// //       });
// //   }, []);

// //   const submitAnswers = useCallback((answers) => {
// //     const payload = { answers };
    
// //     fetch(`${API_BASE_URL}/quizzes/${selectedQuizId}/submit`, {
// //       method: 'POST',
// //       headers: {
// //         'Content-Type': 'application/json',
// //       },
// //       body: JSON.stringify(payload),
// //     })
// //     .then(res => res.json())
// //     .then(data => {
// //       setScoreData(data);
// //       setQuizState('results');
// //     })
// //     .catch(err => {
// //       console.error("Error submitting quiz:", err);
// //       alert("Submission failed. Check console for details.");
// //     });
// //   }, [selectedQuizId]);

// //   const resetQuiz = () => {
// //     setQuizState('start');
// //     setQuestions([]);
// //     setSelectedQuizId(null);
// //     setScoreData(null);
// //   };

// //   // --- Render based on State ---

// //   let content;
// //   if (quizState === 'start') {
// //     content = <StartScreen quizzes={quizzes} onStart={startQuiz} />;
// //   } else if (quizState === 'in_progress') {
// //     content = (
// //       <QuizView 
// //         questions={questions} 
// //         duration={QUIZ_DURATION_SECONDS}
// //         onSubmit={submitAnswers} 
// //       />
// //     );
// //   } else if (quizState === 'results') {
// //     content = <ResultScreen scoreData={scoreData} onRestart={resetQuiz} />;
// //   }

// //   return (
// //     <div className="App">
// //       <header className="App-header">
// //         <h1>Full-Stack Quiz App</h1>
// //       </header>
// //       <main className="quiz-container">
// //         {content}
// //       </main>
// //     </div>
// //   );
// // }

// // export default App;



// // frontend/src/App.js
// import React, { useState, useEffect, useCallback } from 'react';
// import StartScreen from './StartScreen';
// import QuizView from './QuizView';
// import ResultScreen from './ResultScreen';
// import './App.css'; 
// import { useAuth } from './AuthContext'; 
// import Login from './Login';
// import AdminDashboard from './AdminDashboard';

// const API_BASE_URL = 'http://localhost:5000/api';
// const QUIZ_DURATION_SECONDS = 60; // Define or import this constant

// function App() {
//   const { isAuthenticated, isAdmin, logout } = useAuth();
  
//   // --- CORE QUIZ STATES (Restored) ---
//   // States: 'start', 'in_progress', 'results'
//   const [quizState, setQuizState] = useState('start'); 
//   const [quizzes, setQuizzes] = useState([]);
//   const [questions, setQuestions] = useState([]);
//   const [selectedQuizId, setSelectedQuizId] = useState(null);
//   const [scoreData, setScoreData] = useState(null);
//   // ------------------------------------

//   const [view, setView] = useState('quiz'); // 'quiz', 'login', 'admin'

//   // --- Initial Load: Fetch Available Quizzes (Restored useEffect) ---
//   const fetchQuizzes = useCallback(() => {
//     fetch(`${API_BASE_URL}/quizzes`)
//       .then(res => res.json())
//       .then(data => setQuizzes(data))
//       .catch(err => console.error("Error fetching quizzes:", err));
//   }, []);

//   useEffect(() => {
//     // Only fetch quizzes when the view is the main 'quiz' view
//     if (view === 'quiz') {
//       fetchQuizzes();
//     }
//   }, [view, fetchQuizzes]);

//   // --- Quiz Flow Handlers (Restored) ---

//   const startQuiz = useCallback((quizId) => {
//     setSelectedQuizId(quizId);
//     setQuizState('in_progress');
//     // Fetch questions for the selected quiz
//     fetch(`${API_BASE_URL}/quizzes/${quizId}/questions`)
//       .then(res => res.json())
//       .then(data => setQuestions(data))
//       .catch(err => {
//         console.error("Error fetching questions:", err);
//         alert("Could not load quiz questions.");
//         setQuizState('start');
//       });
//   }, []); // Dependencies: none needed, API_BASE_URL is constant

//   const submitAnswers = useCallback((answers) => {
//     const payload = { answers };
    
//     // Ensure the token is included if the user is logged in
//     const headers = {
//         'Content-Type': 'application/json',
//     };
//     if (isAuthenticated) {
//         headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
//     }

//     fetch(`${API_BASE_URL}/quizzes/${selectedQuizId}/submit`, {
//       method: 'POST',
//       headers: headers,
//       body: JSON.stringify(payload),
//     })
//     .then(res => res.json())
//     .then(data => {
//       setScoreData(data);
//       setQuizState('results');
//     })
//     .catch(err => {
//       console.error("Error submitting quiz:", err);
//       alert("Submission failed. Check console for details.");
//     });
//   }, [selectedQuizId, isAuthenticated]);


//   const resetQuiz = () => {
//     setQuizState('start');
//     setQuestions([]);
//     setSelectedQuizId(null);
//     setScoreData(null);
//     // Refetch the quiz list in case an admin added a new one
//     fetchQuizzes(); 
//   };
//   // ------------------------------------
  
//   const handleSuccessfulLogin = () => {
//     setView('quiz'); // Go back to the main quiz list after login
//   }

//   // --- Render based on State ---

//   let content;
//   if (view === 'login') {
//       content = <Login onLoginSuccess={handleSuccessfulLogin} />;
//   } else if (view === 'admin') {
//       content = <AdminDashboard />;
//   } else if (quizState === 'start') {
//     // Corrected to use the StartScreen component
//     content = <StartScreen quizzes={quizzes} onStart={startQuiz} />;
//   } else if (quizState === 'in_progress') {
//     content = (
//       <QuizView 
//         questions={questions} 
//         duration={QUIZ_DURATION_SECONDS}
//         onSubmit={submitAnswers} 
//       />
//     );
//   } else if (quizState === 'results') {
//     content = <ResultScreen scoreData={scoreData} onRestart={resetQuiz} />;
//   }

//   // Fallback for initial loading
//   if (!content) {
//     content = <p>Loading application...</p>;
//   }


//   return (
//     <div className="App">
//       <header className="App-header">
//         <h1>Full-Stack Quiz App</h1>
//         <div className="user-controls">
//           {/* Navigation/Auth buttons */}
//           <button onClick={() => setView('quiz')}>Home</button>
//           {isAdmin && <button onClick={() => setView('admin')}>Admin</button>}
          
//           {isAuthenticated ? (
//             <button onClick={logout}>Log Out</button>
//           ) : (
//             <button onClick={() => setView('login')}>Log In</button>
//           )}
//         </div>
//       </header>
//       <main className="quiz-container">
//         {content}
//       </main>
//     </div>
//   );
// }

// export default App;



import React, { useState, useEffect, useCallback } from 'react';
import StartScreen from './StartScreen';
import QuizView from './QuizView';
import ResultScreen from './ResultScreen';
import './App.css';
import { useAuth } from './AuthContext'; 
import Login from './Login';
import AdminDashboard from './AdminDashboard';

const API_BASE_URL = 'http://localhost:5000/api';
const QUIZ_DURATION_SECONDS = 60; 

function App() {
  const { isAuthenticated, isAdmin, logout, saveScore } = useAuth();
  
  // Core Quiz States
  const [quizState, setQuizState] = useState('start'); 
  const [quizzes, setQuizzes] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [selectedQuizId, setSelectedQuizId] = useState(null);
  const [scoreData, setScoreData] = useState(null);
  
  // App View State: 'quiz' (homepage/quiz flow), 'login', 'admin'
  const [view, setView] = useState('quiz'); 

  // --- Initial Load: Fetch Available Quizzes ---
  const fetchQuizzes = useCallback(() => {
    fetch(`${API_BASE_URL}/quizzes`)
      .then(res => res.json())
      .then(data => setQuizzes(data))
      .catch(err => console.error("Error fetching quizzes:", err));
  }, []);

  useEffect(() => {
    if (view === 'quiz') {
      fetchQuizzes();
    }
  }, [view, fetchQuizzes]);

  // --- Quiz Flow Handlers ---

  const startQuiz = useCallback((quizId) => {
    setSelectedQuizId(quizId);
    setQuizState('in_progress');
    
    const headers = {};
    const currentToken = localStorage.getItem('access_token'); 
    if (currentToken) {
        headers['Authorization'] = `Bearer ${currentToken}`;
    }

    // Fetch questions for the selected quiz
    fetch(`${API_BASE_URL}/quizzes/${quizId}/questions`, {
        method: 'GET',
        headers: headers,
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        setQuestions(data);
    })
    .catch(err => {
        console.error("Error fetching questions:", err);
        alert("Could not load quiz questions.");
        setQuizState('start');
        fetchQuizzes(); // Try reloading the quiz list
    });
  }, [fetchQuizzes]);

  const submitAnswers = useCallback((answers) => {
    const payload = { answers };
    
    const currentToken = localStorage.getItem('access_token'); 
    
    if (!currentToken) {
        alert("You must be logged in to submit a quiz score.");
        setQuizState('start');
        return;
    }

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentToken}`, 
    };

    fetch(`${API_BASE_URL}/quizzes/${selectedQuizId}/submit`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(payload),
    })
    .then(res => {
        if (res.status === 401) {
            logout(); 
            alert("Session expired. Please log in again.");
            return;
        }
        return res.json();
    })
    .then(data => {
      if (data) {
        // Save the result data to local storage
        saveScore(selectedQuizId, data); 

        setScoreData(data);
        setQuizState('results');
      }
    })
    .catch(err => {
      console.error("Error submitting quiz:", err);
      alert("Submission failed. Check console for details.");
    });
  }, [selectedQuizId, logout, saveScore]);

  const resetQuiz = () => {
    setQuizState('start');
    setQuestions([]);
    setSelectedQuizId(null);
    setScoreData(null);
    fetchQuizzes(); 
  };
  
  // NEW: Handler for "View Results" button on StartScreen
  const viewResults = useCallback((quizId, results) => {
    setSelectedQuizId(quizId);
    setScoreData(results);
    setQuizState('results');
  }, []); 

  const handleSuccessfulLogin = () => {
    setView('quiz'); 
    fetchQuizzes(); // Reload quiz list after login
  }

  // --- Render based on State ---

  let content;
  if (view === 'login') {
      content = <Login onLoginSuccess={handleSuccessfulLogin} />;
  } else if (view === 'admin') {
      content = <AdminDashboard />;
  } else if (quizState === 'start') {
    content = (
      <StartScreen 
        quizzes={quizzes} 
        onStart={startQuiz} 
        onViewResults={viewResults} // Pass the viewResults handler
      />
    );
  } else if (quizState === 'in_progress') {
    content = (
      <QuizView 
        questions={questions} 
        duration={QUIZ_DURATION_SECONDS}
        onSubmit={submitAnswers} 
      />
    );
  } else if (quizState === 'results') {
    content = <ResultScreen scoreData={scoreData} onRestart={resetQuiz} />;
  }
  
  if (!content) {
    content = <p>Loading application...</p>;
  }


  return (
    <div className="App">
      <header className="App-header">
        <h1>Prashnamanch</h1>
        <div className="user-controls">
          <button onClick={() => setView('quiz')}>Home</button>
          {isAdmin && <button onClick={() => setView('admin')}>Create Quiz</button>}
          
          {isAuthenticated ? (
            <button onClick={logout}>Log Out</button>
          ) : (
            <button onClick={() => setView('login')}>Log In</button>
          )}
        </div>
      </header>
      <main className="quiz-container">
        {content}
      </main>
    </div>
  );
}

export default App;