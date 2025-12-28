import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Cookies from "js-cookie";
import { useChat } from "../composables/useChat";
import { usePublicIP } from "../composables/usePublicIP";
import { sendQuery } from "../requests/requests";
import { BiSearch } from "react-icons/bi";

const PromptBar = () => {
  const [input, setInput] = useState("");
  const [cookieAccepted, setCookieAccepted] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { messages, addMessage, isLoading, setIsLoading } = useChat();
  const ip = usePublicIP(cookieAccepted);

  const historySize = 2;

  useEffect(() => {
    setCookieAccepted(Cookies.get("lastro-userDataConsent") === "true");
  }, []);

  const handleSend = async () => {
    if (!input.trim() || !ip) return;

    const prompt = input.trim();

    if (location.pathname !== "/explorar") navigate("/explorar");

    setIsLoading(true);

    try {
      const response = await sendQuery({
        cookieConsent: cookieAccepted,
        userIp: ip,
        previousPrompts: messages.slice(-historySize).map((msg) => msg.prompt),
        currentPrompt: prompt,
      });

      addMessage({
        prompt,
        queries: response.queries,
        descriptions: response.descriptions,
        results: response.results,
      });
      setInput("");
    } catch (err) {
      console.error(err);
      addMessage({ prompt });
      setInput("");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="fixed bottom-0 left-0 w-full bg-color-bg border-t border-color-2/25 z-50">
      <div className="flex items-center h-full menu-footer-setup">
        <div className="flex gap-2 w-full bg-color-2/5 rounded-full transition-all focus-within:ring-1 focus-within:ring-color-2/25">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Procure qualquer coisa..."
            disabled={!ip || isLoading}
            className={`flex-1 bg-transparent pl-6 text-color-1 text-body-2 placeholder:text-color-2/40 focus:outline-none transition-all ${
              isLoading ? "opacity-40" : "opacity-100"
            }`}
          />
          <button
            onClick={handleSend}
            disabled={!ip || isLoading || !input.trim()}
            className="text-color-1 pr-8 pl-4 rounded-lg hover:opacity-80 disabled:opacity-40 disabled:cursor-not-allowed transition-opacity flex items-center justify-center w-12 h-12 relative cursor-pointer"
          >
            <svg
              className={`animate-spin h-5 w-5 absolute transition-opacity duration-300 ${
                isLoading ? "opacity-100 delay-150" : "opacity-0 delay-0"
              }`}
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="3"
              ></circle>
              <path
                className="opacity-75"
                stroke="currentColor"
                strokeWidth="3"
                strokeLinecap="round"
                d="M12 2a10 10 0 0 1 10 10"
              ></path>
            </svg>
            <BiSearch
              className={`h-6 w-6 absolute transition-opacity duration-300 ${
                isLoading ? "opacity-0 delay-0" : "opacity-100 delay-150"
              }`}
            />
          </button>
        </div>
      </div>
    </div>
  );
};

export default PromptBar;
