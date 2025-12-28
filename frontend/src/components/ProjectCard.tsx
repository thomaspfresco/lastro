import { useVimeoThumb } from "../composables/useVimeoThumb";
import { Link } from "react-router-dom";
import { useState } from "react";
import logoSvg from "../assets/logo.svg";

interface ProjectCardProps {
  project: Project;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ project }) => {
  const [imageLoaded, setImageLoaded] = useState(false);

  return (
    <Link
      to={`/projetos/${project.id}`}
      className="group relative w-full flex flex-row gap-4 overflow-hidden rounded-lg p-2"
    >
      {/* Image wrapper */}
      <div className="aspect-square relative h-16 flex-shrink-0 rounded-[5%] bg-color-bg overflow-hidden z-10">
        {/* Loading logo */}
        <img
          src={logoSvg}
          alt="Loading"
          className={`relative z-10 w-10 h-10 mx-auto my-auto transition-opacity duration-500 ${
            imageLoaded ? "opacity-0" : "opacity-50"
          }`}
        />

        {/* Thumbnail */}
        <img
          src={useVimeoThumb(project.id)}
          alt={project.title}
          loading="lazy"
          onLoad={() => setImageLoaded(true)}
          className={`
            absolute inset-0
            z-20
            w-full h-full
            object-cover
            grayscale
            transition-all
            duration-1000
            ease-out
            group-hover:grayscale-0
            group-hover:scale-[1.02]
            ${imageLoaded ? "opacity-100" : "opacity-0"}
          `}
        />
      </div>

      {/* Text content */}
      <div className="relative z-10 w-full">
        <h3 className="text-body-1 group-hover:underline transition-all duration-300">
          {project.title || "Sem título registado"}
        </h3>

        <p className="text-note-2 pt-0.5 opacity-50 group-hover:underline transition-all duration-300">
          {project.author || "Sem autor registado"}
        </p>

        <p className="text-note-2 pt-2 opacity-35">
          {project.category || "Sem categoria registada"}
        </p>
      </div>
    </Link>
  );
};

export default ProjectCard;
