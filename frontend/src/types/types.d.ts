interface Project {
  id: string;
  title: string;
  author: string;
  category: string;
  link?: string;
  date?: string;
  direction?: string;
  sound?: string;
  production?: string;
  support?: string;
  assistance?: string;
  research?: string;
  location?: string;
  instruments?: string;
  keywords?: string;
  infoPool?: string;
  created_at: string;
}

type Projects = Project[];

interface Suggestion {
  description: string;
  projects: Project[];
}

type Suggestions = Suggestion[];

interface CookiePopupProps {
  onAccept?: () => void;
}

interface ChatMessage {
  id?: number; // Unique sequential ID for each message
  prompt: string;
  queries?: string[];
  descriptions?: string[];
  results?: Projects[];
}

interface QueryResponse {
  queries: string[];
  descriptions: string[];
  results: Projects[];
}
