//import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./index.css";

import Home from "./pages/Home";
import About from "./pages/About";
import Explore from "./pages/Explore";
import Project from "./pages/Project";
import PageTransition from "./components/PageTransition";
import PromptBar from "./components/PromptBar";
import Menu from "./components/Menu";

import { ChatProvider } from "./composables/useChat";
import { useMetadata } from "./composables/useMetadata";

function App() {
  useMetadata();

  return (
    <BrowserRouter>
      <ChatProvider>
        <Menu />

        <Routes>
          <Route element={<PageTransition />}>
            <Route path="/" element={<Home />} />
            <Route path="/sobre" element={<About />} />
            <Route path="/explorar" element={<Explore />} />
            <Route path="/projetos/:id" element={<Project />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>

        <PromptBar />
      </ChatProvider>
    </BrowserRouter>
  );
}

createRoot(document.getElementById("root")!).render(
  //<StrictMode>
  <App />
  //</StrictMode>
);
