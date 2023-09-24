// initial state
const state = () => ({
    currentUserEmail: null,
    currentUserFirstName: null,
    currentUserLastName: null,
    currentUserRoles: null,
    token: null
})

// getters
const getters = {}

// actions
const actions = {}

// mutations
const mutations = {
    updateCurrentUserEmail (state, email) {
        state.currentUserEmail = email
    },
    updateCurrentUserFirstName (state, first_name) {
        state.currentUserFirstName = first_name
    },
    updateCurrentUserLastName (state, last_name) {
        state.currentUserLastName = last_name
    },
    updateRoles (state, roles) {
        state.currentUserRoles = roles
    },
    updateToken (state, token) {
        state.token = token
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }