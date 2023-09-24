<template>

  <div class="container mt-2">
      <div class="d-flex justify-content-start mt-2">
    <i class="fa-sharp fa-solid fa-circle-info" @click="toggleKanbanInfo"></i>
      <KanbanInfo v-if="showKanbanInfo"/>
  </div>
    <div class="row">
      <h4 class="text-center text-danger" v-if="!loggedIn">
        Die Nutzung des Kanban-Boards ist nur als eingeloggter User möglich
      </h4>
      <div
        class="col-12 col-lg-4 mt-2"
        v-for="statusCard in statusCards"
        :key="statusCard.status"
      >
        <StatusCard
          :title="statusCard.title"
          :titleClasses="statusCard.titleClasses"
          :newTasks="statusCard.newTasks"
          :status="statusCard.status"
          :tasks="filteredTasks(statusCard.status)"
          @new-task="addTask"
          @status-updated="updateStatus"
          @delete-task="deleteTask"
        />
      </div>
    </div>
  </div>
</template>

<script>
import StatusCard from "./StatusCard.vue";
import logger from "../../mixins/logger";
import { mapActions } from "vuex";
import KanbanInfo from './KanbanInfo.vue';

export default {
  name: "KanbanBoard",
  mixins: [logger],
  components: {
    StatusCard,
    KanbanInfo
  },
  provide() {
    return {
      maxNumberOfChars: 255,
    };
  },
  data() {
    return {
      showKanbanInfo: false
    };
  },
  computed: {
    newTasks() {
      return this.tasks.filter((task) => task.status === 0);
    },
    tasks() {
      return this.$store.getters.tasks;
    },
    statusCards() {
      return this.$store.getters.statusCards;
    },
    loggedIn() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    toggleKanbanInfo(){
      this.showKanbanInfo = !this.showKanbanInfo;
    },
    filteredTasks(status) {
      return this.tasks.filter((task) => task.status === status);
    },
    ...mapActions({
      addTask: "addTaskToTasks",
      updateStatus: "updateStatusOfTask",
      deleteTask: "deleteTaskFromTasks",
    }),
  },
};
</script>

<style sscoped></style>
