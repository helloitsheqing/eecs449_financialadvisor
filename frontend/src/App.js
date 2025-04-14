import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import MenuBar from './MenuBar';
import HomePage from './HomePage';
import ChatPage from './ChatScreen';
import InfoBankPage from './InfoBank';
import LoginPage from './login.js';
import SignupPage from './signup.js'
import SettingsPage from './settings.js';
import ExistingChatPage from './existingChatScreen.js';
import { LogUserProvider } from './contexts/context.js';
import { ExistingChatProvider } from './contexts/existingChatContext';
import InsertExcel from './InsertExcel.js';
import { ModelProvider } from './contexts/modelPreference.js';
// import ProtectedRoute from './ProtectedRoute';

const App = () => {
  return (
    <ExistingChatProvider>
      <LogUserProvider>
        <ModelProvider>
        <Router>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/existing-chat" element={<ExistingChatPage />} />
            <Route path="/upload-excel" element={<InsertExcel/>} />
            <Route path="/settings" element={<SettingsPage/>} />

            {/* Protected Routes - Only accessible when authenticated */}
            {/* <Route element={<ProtectedRoute />}> */}
            <Route>
              <Route
                path="/chat"
                element={
                  <>
                    <MenuBar />
                    <ChatPage />
                  </>
                }
              />
              <Route
                path="/infobank"
                element={
                  <>
                    <MenuBar />
                    <InfoBankPage />
                  </>
                }
              />
            </Route>

            {/* Fallback route for unknown paths */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
        </ModelProvider>
      </LogUserProvider>
    </ExistingChatProvider>
  );
};

export default App;
