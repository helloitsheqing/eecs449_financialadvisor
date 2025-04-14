import React, { createContext, useState } from 'react';

const ModelContext = createContext();

export const ModelProvider = ({ children }) => {
  const [agent_model, setAgentModel] = useState('deepseek-r1:1.5b');       //  Log user

  return (
    <ModelContext.Provider value={{
        agent_model, setAgentModel,
    }}>
      {children}
    </ModelContext.Provider>
  );
};

export default ModelContext;
