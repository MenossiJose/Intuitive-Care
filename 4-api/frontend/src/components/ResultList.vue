<template>
  <div class="result-list">
    <div v-if="loading">Carregando resultados...</div>

    <div v-else-if="results.length === 0">Nenhum resultado encontrado.</div>

    <div v-else>
      <div v-for="(result, index) in results" :key="index" class="result-item">
        <ResultItem :data="result" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { searchOperatorsByName } from "../services/api.js";
import ResultItem from "./ResultItem.vue";

const results = ref([]);
const loading = ref(false);
const route = useRoute();

onMounted(async () => {
  const query = route.query.q;
  if (query) {
    loading.value = true;
    try {
      const response = await searchOperatorsByName(query);
      results.value = response.data;
    } catch (error) {
      console.error("Erro ao buscar os resultados:", error);
      results.value = [];
    } finally {
      loading.value = false;
    }
  }
});
</script>

<style scoped>
.result-list {
  padding: 1em;
}

.result-item {
  margin-bottom: 1em;
  padding: 0.75em;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
