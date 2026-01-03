import { useEffect, useState, useRef, useLayoutEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { BiArrowBack } from "react-icons/bi";
import { getProject, getSuggestions } from "../requests/requests";
import ProjectBlock from "../components/ProjectBlock";
import VideoSection from "../components/VideoSection";
import ProjectFooter from "../components/ProjectFooter";
import LoadingState from "../components/LoadingState";
import { useContentReady } from "../composables/usePageTransition";
import gsap from "gsap";

const suggestionsLoadingMessages = [
  ["A", "gerar", "sugestões..."],
  ["A", "procurar", "projectos", "relacionados..."],
];

const Project: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project>();
  const [suggestions, setSuggestions] = useState<Suggestions>([]);
  const [isLoadingProject, setIsLoadingProject] = useState(true);
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(true);
  const [headerHeight, setHeaderHeight] = useState<number>(0);
  const headerRef = useRef<HTMLDivElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  useContentReady(!!project && !isLoadingProject);

  useEffect(() => {
    if (id) {
      // Load project first
      setIsLoadingProject(true);
      setIsLoadingSuggestions(true);
      setProject(undefined);
      setSuggestions([]);

      getProject(id).then((res) => {
        setProject(res as Project);
        setIsLoadingProject(false);
      });

      // Load suggestions separately
      getSuggestions(id).then((res) => {
        setSuggestions(res as Suggestions);
        setIsLoadingSuggestions(false);
      });
    }
  }, [id]);

  useEffect(() => {
    const observer = new ResizeObserver((entries) => {
      entries.forEach((entry) => {
        setHeaderHeight(entry.target.clientHeight);
      });
    });

    if (headerRef.current) observer.observe(headerRef.current);

    return () => observer.disconnect();
  }, [project]);

  useLayoutEffect(() => {
    if (
      !isLoadingSuggestions &&
      suggestions.length > 0 &&
      suggestionsRef.current
    ) {
      const blocks = suggestionsRef.current.querySelectorAll(
        "[data-project-block]"
      );
      if (blocks.length === 0) return;

      const ctx = gsap.context(() => {
        gsap.set(blocks, { opacity: 0, xPercent: 20 });

        gsap.to(blocks, {
          opacity: 1,
          xPercent: 0,
          duration: 1.2,
          stagger: 0.25,
          ease: "expo.out",
        });
      }, suggestionsRef.current);

      return () => ctx.revert();
    }
  }, [isLoadingSuggestions, suggestions]);

  if (!project) return <div />;

  return (
    <div className="grid-setup !py-[var(--menu-height)]">
      <div>
        <div
          ref={headerRef}
          className="sticky top-[var(--menu-height)] bg-color-bg z-2 py-3"
        >
          <div className="flex flex-col gap-1">
            <div className="flex gap-3">
              <button
                onClick={() => navigate("/explorar")}
                className="text-2xl hover:opacity-70 transition-opacity mt-px cursor-pointer"
                aria-label="Go back"
              >
                <BiArrowBack />
              </button>
              <h1 className="text-title-2">
                {project.title == "" ? "Sem título registado" : project.title}
              </h1>
            </div>
            <p className="text-note-1 opacity-50 mt-1 mb-3">
              {project.author == "" ? "Sem autor registado" : project.author}
            </p>
          </div>

          <span className="block h-px w-full bg-color-1 opacity-50" />
        </div>

        <VideoSection project={project} />

        {isLoadingSuggestions ? (
          <LoadingState
            messages={suggestionsLoadingMessages}
            fullHeight={true}
          />
        ) : (
          <div ref={suggestionsRef} className="overflow-x-clip">
            {suggestions.map((suggestion, index) => (
              <div key={index} data-project-block>
                <ProjectBlock
                  title={suggestion.description}
                  projects={suggestion.projects}
                  topOffset={headerHeight}
                />
              </div>
            ))}
          </div>
        )}
      </div>

      <ProjectFooter currentProjectId={id} />
    </div>
  );
};

export default Project;
