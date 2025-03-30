// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MenuBar from './MenuBar';
import HomePage from './HomePage';
import ChatPage from './ChatScreen';
import InfoBankPage from './InfoBank';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} /> {/* No MenuBar here */}
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
      </Routes>
    </Router>
  );
};

export default App;
