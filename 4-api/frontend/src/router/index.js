import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Resultados from "../pages/Resultados.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/resultados",
    name: "Resultados",
    component: Resultados,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
