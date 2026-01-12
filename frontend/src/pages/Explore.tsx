import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import gsap from "gsap";

import CookiePopup from "../components/CookiePopup";
import ProjectBlock from "../components/ProjectBlock";
import LoadingState from "../components/LoadingState";
import { useChat } from "../composables/useChat";
import { useContentReady } from "../composables/usePageTransition";
import { getRandomProjects } from "../requests/requests";

const searchLoadingMessages = [
  ["A", "procurar..."],
  ["Já", "não", "falta", "muito..."],
  ["A", "ponderar..."],
  ["Só", "mais", "um", "pouco..."],
  ["A", "finalizar..."],
];

const Explore: React.FC = () => {
  const { messages, isLoading, addMessage } = useChat();
  const navigate = useNavigate();

  useContentReady(true);
  const [headerHeights, setHeaderHeights] = useState<Record<number, number>>(
    {}
  );
  const headerRefs = useRef<Record<number, HTMLDivElement | null>>({});
  const searchResultRefs = useRef<Record<number, HTMLDivElement | null>>({});
  const projectBlockRefs = useRef<Record<string, HTMLDivElement | null>>({});
  const loadingRef = useRef<HTMLDivElement | null>(null);
  const animatedMessageIds = useRef<Set<number>>(new Set());

  const handleStartExploring = async () => {
    try {
      const randomProjects = await getRandomProjects(100);
      const descriptions = [
        "Um ponto de partida",
        "Apenas o começo",
        "Vai um empurrão?",
      ];
      const randomDescription =
        descriptions[Math.floor(Math.random() * descriptions.length)];

      addMessage({
        prompt: "começar a explorar",
        descriptions: [randomDescription],
        results: [randomProjects as Projects],
      });
    } catch (error) {
      console.error("Error fetching random projects:", error);
    }
  };

  useEffect(() => {
    const observer = new ResizeObserver((entries) => {
      entries.forEach((entry) => {
        const idx = parseInt(entry.target.getAttribute("data-idx") || "0");
        setHeaderHeights((prev) => ({
          ...prev,
          [idx]: entry.target.clientHeight,
        }));
      });
    });

    Object.values(headerRefs.current).forEach((ref) => {
      if (ref) observer.observe(ref);
    });

    return () => observer.disconnect();
  }, [messages.length]);

  useEffect(() => {
    if (isLoading && loadingRef.current) {
      setTimeout(() => {
        loadingRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }, 300);
    }
  }, [isLoading]);

  useLayoutEffect(() => {
    if (messages.length === 0) return;
    const latestIdx = messages.length - 1;
    const latestMessage = messages[latestIdx];
    const messageId = latestMessage.id ?? latestIdx;

    // Check if this message has already been animated by its unique ID
    if (animatedMessageIds.current.has(messageId)) return;

    const searchResultEl = searchResultRefs.current[latestIdx];
    if (!searchResultEl) return;

    // Mark this message ID as animated
    animatedMessageIds.current.add(messageId);

    const header = searchResultEl.querySelector("[data-search-header]");
    const blocks = searchResultEl.querySelectorAll("[data-project-block]");

    const ctx = gsap.context(() => {
      gsap.set([header, ...Array.from(blocks)], { opacity: 0, xPercent: 20 });

      if (header) {
        gsap.to(header, {
          opacity: 1,
          xPercent: 0,
          duration: 1.2,
          ease: "expo.out",
        });
      }

      if (blocks.length > 0) {
        gsap.to(blocks, {
          opacity: 1,
          xPercent: 0,
          duration: 1.2,
          stagger: 0.25,
          ease: "expo.out",
          delay: 0.2,
        });
      }
    }, searchResultEl);

    return () => ctx.revert();
  }, [messages.length, messages]);

  return (
    <div className="grid-setup !pt-[var(--menu-height)] overflow-x-clip">
      <CookiePopup />

      <div
        className={`fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center transition-opacity duration-250 ease-out z-0 ${
          messages.length > 0 || isLoading
            ? "opacity-0 pointer-events-none"
            : "opacity-100"
        }`}
      >
        <p className="text-body-1 text-color-1">
          <span className="opacity-50">Escreva na barra de pesquisa ou </span>
          <button
            onClick={handleStartExploring}
            className="text-color-1 opacity-50 hover:opacity-100 underline transition-opacity duration-300 cursor-pointer"
          >
            clique aqui
          </button>
          <span className="opacity-50"> para começar.</span>
        </p>
      </div>

      <div className="relative">
        {messages.map((msg, idx) => {
          if (msg.results && msg.results.length > 0) {
            return (
              <div
                key={idx}
                ref={(el) => {
                  searchResultRefs.current[idx] = el;
                }}
              >
                <div
                  ref={(el) => {
                    headerRefs.current[idx] = el;
                  }}
                  data-idx={idx}
                  data-search-header
                  className="sticky top-[var(--menu-height)] bg-color-bg z-10 py-3"
                >
                  <div className="opacity-50">
                    <p className="text-note-3 uppercase">
                      pesquisa #{(msg.id ?? idx) + 1}
                      {msg.contextProject && (
                        <span>
                          {" "}
                          —{" "}
                          <button
                            onClick={() =>
                              navigate(`/projetos/${msg.contextProject!.id}`)
                            }
                            className="text-note-2 text-color-2 hover:text-color-1 transition-colors group"
                          >
                            <span className="opacity-60 group-hover:opacity-100 transition-opacity duration-250 cursor-pointer">
                              [a partir de {msg.contextProject.title} —{" "}
                              {msg.contextProject.author}]
                            </span>
                          </button>
                        </span>
                      )}
                    </p>
                    <h2 className="text-body-1 mt-0.5">{msg.prompt}</h2>
                    <span className="block h-px w-full bg-color-1 opacity-50 mt-2" />
                  </div>
                </div>

                {msg.results.map((projects, resultIdx) => {
                  if (projects && projects.length > 0) {
                    const title =
                      msg.descriptions?.[resultIdx] ||
                      msg.queries?.[resultIdx] ||
                      msg.prompt;
                    return (
                      <div
                        key={`${idx}-${resultIdx}`}
                        data-project-block
                        ref={(el) => {
                          projectBlockRefs.current[`${idx}-${resultIdx}`] = el;
                        }}
                      >
                        <ProjectBlock
                          title={title}
                          projects={projects}
                          topOffset={headerHeights[idx] || 0}
                        />
                      </div>
                    );
                  }
                  return null;
                })}
              </div>
            );
          }

          // error fallback
          return (
            <div
              key={idx}
              className="p-6 rounded-xl border border-red-500/30 bg-red-500/5 mt-2"
            >
              <p className="text-body-1 text-color-1 mb-2">{msg.prompt}</p>
              <p className="text-note-3 text-red-500">
                Não foi possível comunicar com o servidor. Tente novamente mais
                tarde.
              </p>
            </div>
          );
        })}

        {isLoading && (
          <div ref={loadingRef}>
            <LoadingState messages={searchLoadingMessages} />
          </div>
        )}
      </div>
    </div>
  );
};

export default Explore;
