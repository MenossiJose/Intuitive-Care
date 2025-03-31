import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/",
});

export function searchOperators(query) {
  return api.get("buscar_nome", {
    params: { termo: query },
  });
}

export default api;
