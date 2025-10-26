import { useEffect, useState } from "react";

import { getProjects, getProject } from "../requests/project";
import { getVimeoThumb } from "../hooks/getVimeoThumb";

const Home = () => {
  const [projects, setProjects] = useState<Projects>([]);
  const [project, setProject] = useState<Project>();

  useEffect(() => {
    getProjects().then((res) => setProjects(res as Projects));
  }, []);

  useEffect(() => {
    if (projects.length > 0) {
      getProject(projects[1].id).then((res) => setProject(res as Project));
    }
  }, [projects]);

  return (
    <div>
      <h1>Projects</h1>
      <p>{projects[1]?.title}</p>
      <p>Selected Project: {project?.title}</p>
      {project && <img src={getVimeoThumb(project.id)} alt={project.title} />}
    </div>
  );
};

export default Home;
