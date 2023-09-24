<template>
  <div>
    <input
      type="text"
      class="form-control"
      placeholder="Neue Aufgabe"
      v-model="content"
      v-focus="{ color: 'green' }"
    />
    <small>Noch {{ numberOfCharsLeft }} Zeichen erlaubt.</small>
    <div>
      <small class="text-danger" v-if="contentCheck">Ohne Text kein Task</small>
    </div>
    
    <div class="d-grid my-2">
      <button class="btn btn-secondary" @click="submitTask()">Eintragen</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "NewTask",
  inject: ["maxNumberOfChars"],
  emits: {
    "new-task": (task) => {
      if (task.content === "") {
        console.warn("NewTaskComponent: Der Content sollte nicht leer sein");
        return false;
      }
      return true;
    },
  },
  data() {
    return {
      content: "",
      contentCheck: false,
    };
  },
  computed: {
    numberOfCharsLeft() {
      return this.maxNumberOfChars - this.content.length;
    },
  },
  methods: {
    submitTask() {
      if (this.content !== "") {
        this.contentCheck = false;
        this.$emit("new-task", {
          content: this.content,
        });
        this.content = "";
      } else {
        this.contentCheck = true;
      }
    },
  },
};
</script>

<style scoped></style>
