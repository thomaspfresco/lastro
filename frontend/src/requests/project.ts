import { getRequest } from "./setup";

export async function getProjects() {
  return await getRequest("/projects");
}

export async function getProject(id: string) {
  return await getRequest(`/projects/${id}`);
}

// export async function getUserById(id: string) {
//   return getRequest(`/users/${id}`);
// }

// export async function createUser(data: { name: string; email: string }) {
//   return postRequest("/users", data);
// }

// export async function updateUser(
//   id: string,
//   data: { name?: string; email?: string }
// ) {
//   return putRequest(`/users/${id}`, data);
// }

// export async function deleteUser(id: string) {
//   return deleteRequest(`/users/${id}`);
// }
