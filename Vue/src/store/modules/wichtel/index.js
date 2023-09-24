import axios from "axios";

const state = {
  wichtelEvents: [],
};

const mutations = {
  setWichtelevents(state, payload) {
    const WiEventDO = [];
    for (const event in payload) {
      WiEventDO.push(payload[event]);
    }
    state.wichtelEvents = WiEventDO;
  },
  addWichtelEvent(state, payload) {
    state.wichtelEvents.push(payload);
  },
  updateSubs(state, payload) {
    const event = state.wichtelEvents.find((event) => event.id === payload.id);
    event.subs = payload.subs;
  },
  deleteWichtelevent() {},
};

const actions = {
  fetchWichtelEvents(context) {
    const token = context.rootState.auth.token;
    axios
      .get(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/wichtelEvents.json?auth=${token}`
      )
      .then((res) => {
        const WiEventDO = [];
        for (const event in res.data) {
          const ev = res.data[event];
          ev.id = event;
          WiEventDO.push(ev);
        }
        context.commit("setWichtelevents", WiEventDO);
      })
      .catch((error) => {
        console.log(error);
      });
  },
  storeWichtelEvent(context, payload) {
    const token = context.rootState.auth.token;
    const name = payload.name;
    const pw = payload.pw;
    const date = payload.date;
    const subscribers = payload.subs;
    const wichtelEvent = {
      name: name,
      date: date,
      password: pw,
      subs: subscribers,
    };
    axios
      .post(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/wichtelEvents.json?auth=${token}`,
        wichtelEvent
      )
      .then((res) => {
        wichtelEvent.id = res.data.name;
        context.commit("addWichtelEvent", wichtelEvent);
        const guestList = wichtelEvent.subs.filter((sub) => sub.email);
        for (const person in guestList) {
          console.log(
            `send Mail to ${guestList[person].name} at ${guestList[person].email}`
          );
        }
      })
      .catch((error) => {
        console.log(error);
      });
  },
  updateEvent(context, payload) {
    const token = context.rootState.auth.token;
    const userId = context.rootState.auth.userId;
    const change = payload.change;
    const event = JSON.parse(
      JSON.stringify(context.getters.getWichtelEvent(change.eventId))
    );

    switch (change.kind) {
      case "user": {
        const sub = event.subs.find(
          (sub) => sub.name === change.name && sub.email === change.email
        );
        sub.id = userId;
        break;
      }
      case "wish": {
        const sub = event.subs.find((sub) => sub.id === userId);
        sub.wish = change.wish;
        break;
      }
      default: {
        break;
      }
    }

    axios
      .patch(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/wichtelEvents/${event.id}.json?auth=${token}`,
        event
      )
      .then(() => {
        context.commit("updateSubs", event);
        switch (change.kind) {
          case "user": {
            const numOfSubscriber = event.subs.filter((sub) => sub.id).length;
            if (numOfSubscriber === event.subs.length) {
              context.dispatch("drawWichtelForEvent", { eventId: event.id });
            }
            break;
          }
          default: {
            break;
          }
        }
      })
      .catch((error) => {
        console.log(error);
      });
  },
  drawWichtelForEvent(context, payload) {
    const token = context.rootState.auth.token;
    const event = JSON.parse(
      JSON.stringify(context.getters.getWichtelEvent(payload.eventId))
    );
    const subs = event.subs;
    const usedSubs = [];

    for (const sub in subs) {
      const withoutMe = subs.filter((person) => person.id != subs[sub].id);
      const subsToUse = withoutMe.filter(
        (person) => !usedSubs.find((used) => person.id === used.id)
      );
      const chosenIndex = Math.floor(Math.random() * subsToUse.length);
      usedSubs.push(subsToUse[chosenIndex]);
      subs[sub].wichtel = subsToUse[chosenIndex].id;
    }
    context.commit("updateSubs", event);

    axios
      .patch(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/wichtelEvents/${event.id}.json?auth=${token}`,
        event
      )
      .then(() => {
        context.commit("updateSubs", event);
        console.log("send Mail an alle")
      })
      .catch((error) => {
        console.log(error);
      });
  },
};

const getters = {
  getAllWichtelevents: (state) => state.wichtelEvents,
  getAllWichtelEventsOfUser: (state) => (userId) =>
    state.wichtelEvents.filter((event) =>
      event.subs.some((sub) => sub.id === userId)
    ),
  getWichtelEvent: (state) => (wiEvId) =>
    state.wichtelEvents.find((event) => event.id === wiEvId),
  getAllWichtelEventbyNameAndPw: (state) => (name, pw) =>
    state.wichtelEvents.find(
      (event) => event.name === name && event.password === pw
    ),
  getSubsOfWichtelEvent: (state) => (wiEvId) =>
    state.wichtelEvents.find((event) => event.id === wiEvId).subs,
};

const wichtelModule = {
  state,
  mutations,
  actions,
  getters,
};

export default wichtelModule;
