// initial state
const state = () => ({
    startDate: null,
    endDate: null,
    showName: null,
    showDate: null,
    venueName: null,
    timing: null,
    price: null,
    availableSeats: null,
})

// getters
const getters = {}

// actions
const actions = {}

// mutations
const mutations = {
    updateStartDate (state, startDate) {
        state.startDate = startDate
    },
    updateEndDate (state, endDate) {
        state.endDate = endDate
    },
    updateShowName (state, showName) {
        state.showName = showName
    },
    updateShowDate (state, showDate) {
        state.showDate = showDate
    },
    updateVenueName (state, venueName) {
        state.venueName = venueName
    },
    updateTiming (state, timing) {
        state.timing = timing
    },
    updatePrice (state, price) {
        state.price = price
    },
    updateAvailableSeats (state, availableSeats) {
        state.availableSeats = availableSeats
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }