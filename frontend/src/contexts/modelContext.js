import React, { createContext, useState } from 'react';

const ModelContext = createContext({
    model: 'deepseek-r1:1.5b', // Default value
    setModel: () => {} // Empty function as placeholder
});

export const ModelProvider = ({ children }) => {
  const [model, setModel] = useState("deepseek-r1:1.5b");

  return (
    <ModelContext.Provider value={{
        model, setModel,
    }}>
      {children}
    </ModelContext.Provider>
  );
};

export default ModelContext;
