<template>
  <div class="search-bar">
    <input
      type="text"
      :value="modelValue"
      @input="updateValue($event)"
      :placeholder="placeholder"
      @keyup.enter="submitSearch"
    />
    <button @click="submitSearch">Buscar</button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  placeholder: {
    type: String,
    default: "Digite o termo de busca...",
  },
});

const emit = defineEmits(["update:modelValue", "search"]);

function updateValue(event) {
  emit("update:modelValue", event.target.value);
}

function submitSearch() {
  if (props.modelValue.trim()) {
    emit("search");
  }
}
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  margin: 1em 0;
}
.search-bar input {
  flex: 1;
  padding: 0.5em;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.search-bar button {
  margin-left: 0.5em;
  padding: 0.5em 1em;
  border: none;
  background-color: #c8a4f4;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}
.search-bar button:hover {
  background-color: #a675d9;
}
</style>
