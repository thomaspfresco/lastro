import ProjectCard from "./ProjectCard";
import { useState, useRef, useLayoutEffect } from "react";
import { getRandomProjects } from "../requests/requests";
import gsap from "gsap";
import LoadingState from "./LoadingState";

interface ProjectBlockProps {
  title: string;
  projects: Projects;
  topOffset?: number;
}

const ProjectBlockHome: React.FC<ProjectBlockProps> = ({
  title,
  projects: initialProjects,
  topOffset = 0,
}) => {
  const [isCollapsed] = useState(false);
  const [projects, setProjects] = useState<Projects>(initialProjects);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [previousCount, setPreviousCount] = useState(initialProjects.length);
  const projectRefs = useRef<Record<string, HTMLDivElement | null>>({});

  const handleLoadMore = async () => {
    setIsLoadingMore(true);
    try {
      const moreProjects = (await getRandomProjects(99)) as Projects;
      setPreviousCount(projects.length);
      setProjects((prev) => [...prev, ...moreProjects]);
    } catch (error) {
      console.error("Error loading more projects:", error);
    } finally {
      setIsLoadingMore(false);
    }
  };

  useLayoutEffect(() => {
    // Only animate new projects
    if (projects.length > previousCount) {
      const newProjectElements = [];
      for (let i = previousCount; i < projects.length; i++) {
        const el = projectRefs.current[`${projects[i].id}-${i}`];
        if (el) newProjectElements.push(el);
      }

      if (newProjectElements.length > 0) {
        gsap.fromTo(
          newProjectElements,
          { opacity: 0, xPercent: 20 },
          {
            opacity: 1,
            xPercent: 0,
            duration: 1.2,
            ease: "expo.out",
          }
        );
      }
    }
  }, [projects.length, previousCount, projects]);

  return (
    <div className="project-block relative z-0">
      <div
        className="sticky bg-color-bg z-20 py-3"
        style={{ top: `calc(var(--menu-height) + ${topOffset}px)` }}
      >
        <div className="flex gap-4 mb-3">
          <h2 className="text-title-2">{title}</h2>
        </div>

        <span className="block h-px w-full bg-color-1 opacity-50" />
      </div>

      <div
        className={`
          grid transition-[grid-template-rows,opacity,margin] duration-250 ease-in-out
          ${
            isCollapsed
              ? "grid-rows-[0fr] opacity-0 mb-0"
              : "grid-rows-[1fr] opacity-100 mb-8"
          }
        `}
      >
        <div className="overflow-hidden">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-y-6 md:gap-y-8 gap-x-0 md:gap-x-6 lg:gap-x-8">
            {projects.map((project, index) => (
              <div
                key={`${project.id}-${index}`}
                ref={(el) => {
                  projectRefs.current[`${project.id}-${index}`] = el;
                }}
              >
                <ProjectCard project={project} />
              </div>
            ))}
          </div>
          <div
            className={`flex ${
              isLoadingMore
                ? "justify-start pt-6"
                : "justify-start md:justify-center"
            }`}
          >
            {isLoadingMore ? (
              <LoadingState messages={[["A", "carregar", "mais..."]]} />
            ) : (
              <button
                onClick={handleLoadMore}
                className="text-note-2 cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250 underline pt-4 pb-4 mt-7"
              >
                Ver mais projetos
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectBlockHome;
