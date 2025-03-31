<template>
  <div class="resultados-container">
    <h1>Resultados da Pesquisa</h1>

    <!-- Dropdown -->
    <div class="search-options">
      <label for="searchType">Tipo de Busca:</label>
      <select id="searchType" v-model="selectedSearchType">
        <option value="name">Nome Fantasia</option>
        <option value="cnpj">CNPJ</option>
        <option value="razaoSocial">Razão Social</option>
        <option value="modalidade">Modalidade</option>
        <option value="city">Cidade</option>
      </select>
    </div>

    <SearchBar
      v-model="searchQuery"
      placeholder="Pesquisar..."
      @search="performSearch"
    />

    <div class="results-section">
      <div v-if="loading" class="loading">
        <p>Carregando resultados...</p>
      </div>

      <div v-else-if="results.length === 0 && searched" class="no-results">
        <p>Nenhum resultado encontrado para "{{ searchQuery }}"</p>
      </div>

      <div v-else-if="results.length > 0" class="results-list">
        <h2>{{ results.length }} resultado(s) encontrado(s)</h2>
        <table class="results-table">
          <thead>
            <tr>
              <th>Nome Fantasia</th>
              <th>CNPJ</th>
              <th>Modalidade</th>
              <th>Cidade</th>
              <th>UF</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(result, index) in results" :key="index">
              <td>{{ result.nome_fantasia }}</td>
              <td>{{ result.cnpj }}</td>
              <td>{{ result.modalidade }}</td>
              <td>{{ result.cidade }}</td>
              <td>{{ result.uf }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="initial-state">
        <p>Utilize a barra de pesquisa acima para buscar resultados</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import SearchBar from "../components/SearchBar.vue";

import {
  searchOperatorsByName,
  searchOperatorsByCnpj,
  searchOperatorsByRazaoSocial,
  searchOperatorsByCity,
  searchOperatorsByModalidade,
} from "../services/api.js";

const searchQuery = ref("");
const selectedSearchType = ref("name");
const results = ref([]);
const loading = ref(false);
const searched = ref(false);

async function performSearch() {
  if (!searchQuery.value.trim()) return;

  loading.value = true;
  searched.value = true;

  try {
    let response;
    switch (selectedSearchType.value) {
      case "name":
        response = await searchOperatorsByName(searchQuery.value);
        break;
      case "cnpj":
        response = await searchOperatorsByCnpj(searchQuery.value);
        break;
      case "razaoSocial":
        response = await searchOperatorsByRazaoSocial(searchQuery.value);
        break;
      case "modalidade":
        response = await searchOperatorsByModalidade(searchQuery.value);
        break;
      case "city":
        response = await searchOperatorsByCity(searchQuery.value);
        break;
      default:
        response = await searchOperatorsByName(searchQuery.value);
        break;
    }
    results.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar resultados:", error);
    results.value = [];
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.resultados-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

h1,
h2 {
  color: #333;
  margin-bottom: 20px;
}

.search-options {
  margin-bottom: 15px;
}

.search-options label {
  margin-right: 10px;
  font-weight: bold;
}

.search-options select {
  padding: 0.5em;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.results-section {
  margin-top: 20px;
}

.loading,
.no-results,
.initial-state {
  padding: 20px;
  text-align: center;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.results-table th,
.results-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

.results-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}
</style>
