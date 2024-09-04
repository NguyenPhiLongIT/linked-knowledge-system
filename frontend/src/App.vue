<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <nav>
    <a href="http://localhost:5001">Home</a>
    <a class="active" href="http://localhost:5173">Network</a>
  </nav>
  <RouterView />
</template>

<style scoped>

nav {
  width: 100%;
  font-size: 12px;
  margin-top: 1rem;
}

nav a.active {
  background-color: rgb(226, 220, 220);
  border: 1px solid;
  font-weight: 600;
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 3px solid var(--color-border);
  font-size: 20px;
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  nav {
    text-align: left;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
