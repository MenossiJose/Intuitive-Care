<template>
  <header class="header">
    <div class="header-container">
      <div class="logo">
        <h1>Intuitive Care</h1>
      </div>

      <nav class="navigation">
        <RouterLink to="/" class="nav-link" active-class="active"
          >Home</RouterLink
        >
        <RouterLink to="/resultados" class="nav-link" active-class="active"
          >Resultados</RouterLink
        >
      </nav>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
.header {
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.8em 1.5em;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
}

.logo h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #c8a4f4;
  margin: 0;
}

.navigation {
  display: flex;
  align-items: center;
  gap: 2em;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  font-size: 1.1rem;
  padding: 0.5em 0;
  position: relative;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #c8a4f4;
}

.nav-link::after {
  content: "";
  position: absolute;
  width: 0;
  height: 2px;
  bottom: 0;
  left: 0;
  background-color: #c8a4f4;
  transition: width 0.3s ease;
}

.nav-link:hover::after,
.nav-link.active::after {
  width: 100%;
}

.nav-link.active {
  color: #c8a4f4;
}

@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    padding: 1em;
  }

  .logo {
    margin-bottom: 0.5em;
  }

  .navigation {
    gap: 1em;
    width: 100%;
    justify-content: center;
  }
}
</style>
