import axios from "axios";
import type { AxiosInstance } from "axios";

const api: AxiosInstance = axios.create({
  baseURL: "http://127.0.0.1:5000",
  //baseURL: "https://lastro.thomasfresco.pt/",
  headers: {
    "Content-Type": "application/json",
  },
});

export async function getRequest<T>(endpoint: string): Promise<T> {
  const response = await api.get<T>(endpoint);
  return response.data;
}

export async function postRequest<T>(endpoint: string, data: any): Promise<T> {
  const response = await api.post<T>(endpoint, data);
  return response.data;
}
