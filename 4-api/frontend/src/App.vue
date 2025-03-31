<script setup>
import { RouterLink, RouterView } from "vue-router";
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";
</script>

<template>
  <div id="app">
    <Header />

    <main>
      <RouterView />
    </main>

    <Footer />
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

body,
html {
  margin: 0;
  padding: 0;
  height: 100%;
}
</style>
