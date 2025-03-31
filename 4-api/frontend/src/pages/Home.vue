<template>
  <div class="home-container">
    <h1>Bem-vindo ao Sistema Intuitive Care</h1>
    <div class="card">
      <p>
        Esta plataforma permite consultar e analisar dados presentes no BD
        criado no item 3.
      </p>
      <p>
        Utilize a interface para buscar informações e visualizar resultados.
      </p>
    </div>
    <div class="actions">
      <router-link to="/resultados" class="btn primary">
        Consultar Resultados
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.actions {
  margin-top: 2rem;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s ease;
}

.primary {
  background-color: #c8a4f4;
  color: white;
}

.primary:hover {
  background-color: #c8a4f4;
  transform: translateY(-2px);
}
</style>
