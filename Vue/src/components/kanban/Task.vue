<template>
  <div class="alert" :class="alertClass">
    {{task.content}}
  </div>
</template>

<script>
export default {
    name: "SingleTask",
    props: {
        task: Object,
        alertColor: {
            type: String,
            default: "secondary"
        }
    },
    computed: {
        alertClass() {
            return `alert-${this.alertColor}`;
        }
    }

};
</script>

<style scope></style>
