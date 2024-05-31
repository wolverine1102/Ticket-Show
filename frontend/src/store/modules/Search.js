// initial state
const state = () => ({
    keyword: null,
    showList: null,
    venueList: null,
})

// getters
const getters = {}

// actions
const actions = {}

// mutations
const mutations = {
    updateKeyword (state, keyword) {
        state.keyword = keyword
    },
    updateVenueList (state, venueList) {
        state.venueList = venueList
    },
    updateShowList (state, showList) {
        state.showList = showList
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }