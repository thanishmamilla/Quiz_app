import React, { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

// Helper function to get a user-specific storage key
const getUserKey = (username) => `quiz_scores_${username}`;

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null); // { username: '...', role: 'user' | 'admin' }
    const [token, setToken] = useState(localStorage.getItem('access_token'));
    
    // Attempt to parse user data from token when component mounts
    useEffect(() => {
        if (token) {
            try {
                // Get username from payload (sub) and role from custom claim
                const parts = token.split('.');
                if (parts.length === 3) {
                    const payload = JSON.parse(atob(parts[1]));
                    setUser({ 
                        username: payload.sub, 
                        role: payload.role 
                    });
                }
            } catch (error) {
                console.error("Failed to parse token:", error);
                logout();
            }
        }
    }, [token]);

    const login = (accessToken, role, username) => {
        localStorage.setItem('access_token', accessToken);
        setToken(accessToken);
        setUser({ username, role });
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        setToken(null);
        setUser(null);
    };

    // Function to get stored scores for the current user
    const getStoredScores = () => {
        if (!user || !user.username) return {};
        const key = getUserKey(user.username);
        const scores = localStorage.getItem(key);
        return scores ? JSON.parse(scores) : {};
    };

    // Function to save a new score
    const saveScore = (quizId, scoreData) => {
        if (!user || !user.username) return;

        const key = getUserKey(user.username);
        const currentScores = getStoredScores();
        
        // Ensure quizId is stored as a string key
        currentScores[String(quizId)] = scoreData; 
        localStorage.setItem(key, JSON.stringify(currentScores));
    };

    const isAuthenticated = !!token;
    const isAdmin = user?.role === 'admin';

    return (
        <AuthContext.Provider value={{ token, user, isAuthenticated, isAdmin, login, logout, getStoredScores, saveScore }}>
            {children}
        </AuthContext.Provider>
    );
};