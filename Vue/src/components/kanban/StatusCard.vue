<template>
  <div class="card" @drop="onDrop($event)" @dragover.prevent @dragenter.prevent>
    <div class="card-header text-center" :class="titleClasses">
      <h4>{{ title }}</h4>
    </div>
    <div class="card-body">
      <Task
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        :alertColor="alertColor"
        draggable="true"
        @dragstart="startDrag($event, task)"
        @dblclick="deleteTask(task)"
      />
    </div>
    <div class="card-footer" v-if="newTasks && loggedIn">
      <NewTask @new-task="newTask" />
    </div>
  </div>
</template>

<script>
import Task from "./Task.vue";
import NewTask from "./NewTask.vue";

export default {
  name: "StatusCard",
  components: {
    Task,
    NewTask,
  },
  props: {
    title: String,
    titleClasses: String,
    newTasks: Boolean,
    status: Number,
    tasks: Array,
  },
  emits: {
    "new-task": (task) => {
      if ("status" in task === false) {
        console.warn(
          " StatusCardComponent: Jede Aufgabe muss ein Status-Attribut haben."
        );
        return false;
      }
      return true;
    },
    "status-updated": (statusDO) => {
      if ("newStatus" in statusDO === false) {
        console.warn(
          " StatusCardComponent: Jede Aufgabe muss ein Status-Attribut haben."
        );
        return false;
      }
      return true;
    },
    "delete-task": (task) => {
      if ("id" in task === false) {
        console.warn(
          " StatusCardComponent: Jede Aufgabe die gelöscht werden soll, muss eine ID beinhalten."
        );
        return false;
      }
      return true;
    },
  },
  computed: {
    alertColor() {
      switch (this.status) {
        case 0:
          return "secondary";
        case 1:
          return "primary";
        case 2:
          return "success";
      }
      return "danger";
    },
    loggedIn() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    newTask(task) {
      task.status = this.status;
      this.$emit("new-task", task);
    },
    startDrag(event, task) {
      event.dataTransfer.dropEffect = "move";
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("taskId", task.id);
    },
    onDrop(event) {
      if (this.loggedIn) {
        const taskId = event.dataTransfer.getData("taskId");
        this.$emit("status-updated", {
          taskId: taskId,
          newStatus: this.status,
        });
      }
    },
    deleteTask(task) {
      if (this.loggedIn) {
        this.$emit("delete-task", task);
      }
    },
  },
};
</script>

<style scoped></style>
