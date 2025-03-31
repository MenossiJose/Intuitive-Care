<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>Intuitive Care</h3>
        <p>Automação do ciclo financeiro</p>
      </div>
    </div>

    <div class="footer-bottom">
      <p>
        &copy; {{ currentYear }} Intuitive Care. Todos os direitos reservados.
      </p>
    </div>
  </footer>
</template>

<script setup>
import { computed } from "vue";

const currentYear = computed(() => new Date().getFullYear());
</script>

<style scoped>
.footer {
  background-color: #f8f9fa;
  padding: 2rem 0;
  border-top: 1px solid #e7e7e7;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  padding: 0 1rem;
}

.footer-section {
  flex: 1;
  min-width: 200px;
  margin-bottom: 1.5rem;
  padding: 0 1rem;
}

.footer-section h3 {
  color: #c8a4f4;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  padding-top: 1.5rem;
  margin-top: 1.5rem;
  border-top: 1px solid #e7e7e7;
  color: #777;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
  }

  .footer-section {
    margin-bottom: 2rem;
  }
}
</style>
