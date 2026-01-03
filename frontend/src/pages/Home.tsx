import { useEffect, useState } from "react";
import { useParams} from "react-router-dom";
import { getRandomProjects } from "../requests/requests";
import { useContentReady } from "../composables/usePageTransition";

import ProjectHome from "../components/ProjectHome";
import ProjectBlockHome from "../components/ProjectBlockHome";
import LoadingState from "../components/LoadingState";
import logoSvg from "../assets/logo.svg";

const Home = () => {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<Project>();
  const [randomProjects, setRandomProjects] = useState<Projects | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useContentReady(true);

  useEffect(() => {
    getRandomProjects(1).then((res) => setProject((res as Project[])[0]));
  }, []);

  useEffect(() => {
    const loadRandomProjects = async () => {
      setIsLoading(true);
      try {
        const projects = await getRandomProjects(100);
        setRandomProjects(projects as Projects);
      } catch (error) {
        console.error("Error fetching random projects:", error);
      } finally {
        setIsLoading(false);
      }
    };

    loadRandomProjects();
  }, []);

  if (!project) return <div />;

  return <div className="grid-setup !pt-[var(--menu-height)]">
    <ProjectHome currentProjectId={id} />

    <a href="https://amusicaportuguesaagostardelapropria.org/" target="_blank"><img src={logoSvg}
      alt="Loading"
      className={`relative z-10 w-20 h-20 mx-auto transition-opacity duration-500 mb-12 mt-[calc(var(--spacing)*-20)]`}
      /></a>

    <div className="relative mt-8">
        {isLoading && <LoadingState messages={[["Carregando..."]]} />}

        {randomProjects && (
          <ProjectBlockHome
            title="Explorar Arquivo"
            projects={randomProjects}
            topOffset={0}
          />
        )}
      </div>
  </div>;
};

export default Home;
