<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title">{{event.name}}</h4>
      <p class="card-text">{{ shinyDate }}</p>
      <router-link :to="{name: 'WichtelEvent', params: {id: event.id }}" class="stretched-link"></router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "WichtelEvent",
  props: {
    event: Object,
  },
  computed: {
    shinyDate() {
        const date = new Date(this.event.date);
        const shinyDate = date.getDate() + "." + (date.getMonth() + 1) + "." + date.getFullYear();
        return shinyDate
    }
  }
};
</script>

<style scoped></style>
