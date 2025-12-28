import ProjectCard from "./ProjectCard";
import { MdArrowBackIosNew } from "react-icons/md";
import { useState, useRef, useLayoutEffect } from "react";
import gsap from "gsap";

interface ProjectBlockProps {
  title: string;
  projects: Projects;
  topOffset?: number;
}

const CARDS_PER_CHUNK = 10;

const ProjectBlock: React.FC<ProjectBlockProps> = ({
  title,
  projects,
  topOffset = 0,
}) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [visibleCount, setVisibleCount] = useState(CARDS_PER_CHUNK);
  const blockRef = useRef<HTMLDivElement>(null);
  const previousVisibleCount = useRef(CARDS_PER_CHUNK);

  const handleToggle = () => {
    setIsCollapsed((prev) => !prev);
  };

  const handleShowMore = () => {
    const newVisible = Math.min(
      visibleCount + CARDS_PER_CHUNK,
      projects.length
    );
    setVisibleCount(newVisible);
  };

  const hasMore = visibleCount < projects.length;

  useLayoutEffect(() => {
    if (visibleCount <= previousVisibleCount.current) return;
    if (!blockRef.current) return;

    const startRowIndex = Math.ceil(previousVisibleCount.current / 2);
    const endRowIndex = Math.ceil(visibleCount / 2);
    const newRows: HTMLElement[] = [];

    for (let i = startRowIndex; i < endRowIndex; i++) {
      const row = blockRef.current.querySelector(
        `[data-row-index="${i}"]`
      ) as HTMLElement;
      if (row) newRows.push(row);
    }

    if (newRows.length > 0) {
      const ctx = gsap.context(() => {
        gsap.set(newRows, { opacity: 0, xPercent: 10 });
        gsap.to(newRows, {
          opacity: 1,
          xPercent: 0,
          duration: 1.0,
          stagger: 0.1,
          ease: "expo.out",
        });
      }, blockRef.current);

      previousVisibleCount.current = visibleCount;

      return () => ctx.revert();
    }

    previousVisibleCount.current = visibleCount;
  }, [visibleCount]);

  return (
    <div ref={blockRef} className="project-block relative z-0">
      <div
        className="sticky bg-color-bg z-10 pt-px pb-3"
        style={{ top: `calc(var(--menu-height) + ${topOffset}px)` }}
      >
        <div className="flex justify-between gap-4 mb-3">
          <h2 className="text-title-2">{title}</h2>
          <button
            onClick={handleToggle}
            className="text-xl hover:opacity-70 transition-opacity mt-[2px] cursor-pointer"
            aria-label={isCollapsed ? "Expand section" : "Collapse section"}
          >
            <MdArrowBackIosNew
              className={`transition-transform duration-250 ${
                isCollapsed ? "-rotate-180" : "-rotate-90"
              }`}
            />
          </button>
        </div>

        <span className="block h-px w-full bg-color-1 opacity-50" />
      </div>

      <div
        className={`
          grid transition-[grid-template-rows,opacity,margin] duration-250 ease-in-out
          ${
            isCollapsed
              ? "grid-rows-[0fr] opacity-0 mb-0"
              : "grid-rows-[1fr] opacity-100 mb-24"
          }
        `}
      >
        <div className="overflow-hidden">
          <div className="flex flex-col gap-2 relative z-0">
            {Array.from({ length: Math.ceil(visibleCount / 2) }).map(
              (_, rowIndex) => {
                const startIndex = rowIndex * 1;
                const rowProjects = projects.slice(startIndex, startIndex + 1);

                return (
                  <div
                    key={rowIndex}
                    data-row-index={rowIndex}
                    className="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-0 md:gap-6 lg:gap-8"
                  >
                    <div className="hidden lg:block" />
                    {rowProjects.map((project) => (
                      <div key={project.id}>
                        <ProjectCard project={project} />
                        <span className="block h-px w-full bg-color-1 opacity-50 mt-2" />
                      </div>
                    ))}
                  </div>
                );
              }
            )}

            {hasMore && (
              <div className="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-x-0 md:gap-x-6 lg:gap-x-8 pt-4 lg:pt-6">
                <div className="hidden lg:block" />
                <div>
                  <button
                    onClick={handleShowMore}
                    className="h-8 text-note-2 underline cursor-pointer text-color-2 hover:text-color-1 transition-all duration-300"
                  >
                    Mostrar mais ({projects.length - visibleCount} restantes)
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectBlock;
