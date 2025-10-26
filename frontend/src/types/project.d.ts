interface Project {
  id: string;
  title: string;
  author: string;
  category: string;
  link?: string;
  date?: string;
  direction?: string[];
  sound?: string[];
  production?: string[];
  support?: string[];
  assistance?: string[];
  research?: string[];
  location?: string;
  instruments?: string[];
  keywords?: string[];
  infoPool?: string;
  created_at: string;
}

type Projects = Project[];
