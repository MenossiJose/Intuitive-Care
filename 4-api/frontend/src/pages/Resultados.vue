<template>
  <div class="resultados-container">
    <h1>Resultados da Pesquisa</h1>

    <!-- Barra de busca -->
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
        <!-- Exibição dos resultados em uma tabela -->
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
import { searchOperators } from "../services/api.js";

const searchQuery = ref("");
const results = ref([]);
const loading = ref(false);
const searched = ref(false);

async function performSearch() {
  if (!searchQuery.value.trim()) return;

  loading.value = true;
  searched.value = true;

  try {
    // Chama a API passando o termo de busca
    const response = await searchOperators(searchQuery.value);
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
