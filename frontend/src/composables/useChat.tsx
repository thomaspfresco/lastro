import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";

interface ChatContextType {
  messages: ChatMessage[];
  addMessage: (message: ChatMessage) => void;
  clearMessages: () => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

const MAX_MESSAGES = 25;

export const ChatProvider = ({ children }: { children: ReactNode }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [messageCounter, setMessageCounter] = useState(0);

  const addMessage = (message: ChatMessage) => {
    setMessages((prev) => {
      const messageWithId = { ...message, id: messageCounter };
      const newMessages = [...prev, messageWithId];
      if (newMessages.length > MAX_MESSAGES) {
        return newMessages.slice(newMessages.length - MAX_MESSAGES);
      }
      return newMessages;
    });
    setMessageCounter((prev) => prev + 1);
  };

  const clearMessages = () => {
    setMessages([]);
  };

  return (
    <ChatContext.Provider
      value={{ messages, addMessage, clearMessages, isLoading, setIsLoading }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChat must be used within ChatProvider");
  }
  return context;
};
