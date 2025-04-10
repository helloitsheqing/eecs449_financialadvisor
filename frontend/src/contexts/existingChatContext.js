import React, { createContext, useState } from 'react';

const ExistingChatContext = createContext();

export const ExistingChatProvider = ({ children }) => {
  const [existingChat, setExistingChat] = useState(-1);       //  Log user

  return (
    <ExistingChatContext.Provider value={{
      existingChat, setExistingChat,
    }}>
      {children}
    </ExistingChatContext.Provider>
  );
};

export default ExistingChatContext;
