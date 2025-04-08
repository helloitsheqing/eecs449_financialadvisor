import React, { createContext, useState } from 'react';

const LogUserContext = createContext();

export const LogUserProvider = ({ children }) => {
  const [username, setUsername] = useState(-1);       //  Log user

  return (
    <LogUserContext.Provider value={{
        username, setUsername,
    }}>
      {children}
    </LogUserContext.Provider>
  );
};

export default LogUserContext;
