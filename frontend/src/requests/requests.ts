import { getRequest, postRequest } from "./setup";

export async function getProjects() {
  return await getRequest("/projects");
}

export async function getProject(id: string) {
  return await getRequest(`/projects/${id}`);
}

export async function getSuggestions(id: string) {
  return await getRequest(`/suggestions/${id}`);
}

export async function getRandomProjects(count: number) {
  return await getRequest(`/random-projects/${count}`);
}

export async function sendQuery(data: {
  cookieConsent: boolean;
  userIp: string;
  previousQueries: string[];
  currentPrompt: string;
}): Promise<QueryResponse> {
  return postRequest<QueryResponse>("/query", data);
}
