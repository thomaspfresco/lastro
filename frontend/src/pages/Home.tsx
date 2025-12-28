import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getRandomProjects } from "../requests/requests";
import { useContentReady } from "../composables/usePageTransition";
import ProjectHome from "../components/ProjectHome";

const Home = () => {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<Project>();

  useContentReady(true);

  useEffect(() => {
    getRandomProjects(1).then((res) => setProject((res as Project[])[0]));
  }, []);

  if (!project) return <div />;

  return <div className="grid-setup">
    <ProjectHome currentProjectId={id} />
  </div>;
};

export default Home;
