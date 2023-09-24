<template>
  <TheNavOneColLayout>
    <template #default>
      <KanbanBoard></KanbanBoard>
    </template>
  </TheNavOneColLayout>
</template>

<script>
import TheNavOneColLayout from "@/layouts/TheNavOneColLayout.vue";
import KanbanBoard from "@/components/kanban/KanbanBoard.vue";

export default {
  name: "KanbanPage",
  components: {
    TheNavOneColLayout,
    KanbanBoard,
  },
};
</script>

<style></style>
