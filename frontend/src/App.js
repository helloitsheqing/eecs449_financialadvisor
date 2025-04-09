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
import { LogUserProvider } from './context.js';
import InsertExcel from './InsertExcel.js';
// import ProtectedRoute from './ProtectedRoute';

const App = () => {
  return (
    <LogUserProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/existing-chat" element={<ExistingChatPage />} />
          <Route path="/upload-excel" element={<InsertExcel/>} />

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
          <Route
            path="/settings"
            element={
              <>
                <MenuBar />
                <SettingsPage />
              </>
            }
          />
          <Route
            path="/upload-excel"
            element={
              <>
                <MenuBar />
                <InsertExcel />
              </>
            }
          />
          {/* Fallback route for unknown paths */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </LogUserProvider>
  );
};

export default App;