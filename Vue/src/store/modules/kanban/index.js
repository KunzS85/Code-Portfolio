import axios from "axios";

const state = {
  tasks: [],
  statusCards: [],
};

const mutations = {
  setStatusCards(state, payload) {
    state.statusCards = payload;
  },
  setTasks(state, payload) {
    state.tasks = payload;
  },
  addTask(state, payload) {
    state.tasks.push(payload.task);
  },
  updateStatus(state, payload) {
    const task = state.tasks.find(
      (task) => task.id === Number(payload.statusDO.taskId)
    );
    task.status = payload.statusDO.newStatus;
  },
  deleteTask(state, payload) {
    const taskIndex = state.tasks.findIndex(
      (task) => task.id === payload.unwantedTask.id
    );
    state.tasks.splice(taskIndex, 1);
  },
};
const actions = {
  fetchStatusCards(context) {
    axios
      .get(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/statusCards.json`
      )
      .then((res) => {
        context.commit("setStatusCards", res.data);
      })
      .catch((error) => {
        console.log(error);
      });
  },
  fetchTasks(context) {
    axios
      .get(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/tasks.json`
      )
      .then((res) => {
        const tasksDO = [];
        for (const task in res.data) {
          tasksDO.push({
            ...res.data[task],
            dbId: task,
          });
        }
        context.commit("setTasks", tasksDO);
      })
      .catch((error) => {
        console.log(error);
      });
  },
  addTaskToTasks(context, payload) {
    const token = context.rootState.auth.token;
    const newTask = payload;
    newTask.id = Math.random();

    axios
      .post(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/tasks.json?auth=${token}`,
        newTask
      )
      .then((res) => {
        newTask.dbId = res.data.name;
        context.commit("addTask", {
          task: newTask,
        });
      })
      .catch((error) => {
        console.log(error);
      });
  },
  updateStatusOfTask(context, payload) {
    const token = context.rootState.auth.token;
    const task = context.getters.getTaskById(payload.taskId);
    const newStatusOfTask = {
      status: payload.newStatus,
    };
    axios
      .patch(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/tasks/${task.dbId}.json?auth=${token}`,
        newStatusOfTask
      )
      .then(() => {
        context.commit("updateStatus", {
          statusDO: payload,
        });
      })
      .catch((error) => {
        console.log(error);
      });
  },
  deleteTaskFromTasks(context, payload) {
    const token = context.rootState.auth.token;
    const task = context.getters.getTaskById(payload.id);
    axios
      .delete(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/tasks/${task.dbId}.json?auth=${token}`
      )
      .then(() => {
        context.commit("deleteTask", {
          unwantedTask: payload,
        });
      })
      .catch((error) => {
        console.log(error);
      });
  },
};

const getters = {
  tasks: (state) => state.tasks,
  statusCards: (state) => state.statusCards,
  getTaskById: (state) => (id) =>
    state.tasks.find((task) => task.id === Number(id)),
};

const kanbanModule = {
  state,
  mutations,
  actions,
  getters,
};

export default kanbanModule;
