import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/",
});

export function searchOperatorsByName(query) {
  return api.get("buscar_detalhada_nome", {
    params: { termo: query },
  });
}

export function searchOperatorsByCnpj(query) {
  return api.get("buscar_detalhada_cnpj", {
    params: { termo: query },
  });
}

export function searchOperatorsByRazaoSocial(query) {
  return api.get("buscar_razao_social", {
    params: { termo: query },
  });
}

export function searchOperatorsByCity(query) {
  return api.get("buscar_cidade_uf", {
    params: { cidade: query },
  });
}

export function searchOperatorsByModalidade(query) {
  return api.get("buscar_modalidade", {
    params: { termo: query },
  });
}

export default api;
