// initial state
const state = () => ({
    id: null,
    name: null,
    place: null,
    location: null,
    city: null,
    state: null,
    availableFacilities: null,
    capacity: null,
    venueList: null,
})

// getters
const getters = {}

// actions
const actions = {}

// mutations
const mutations = {
    updateId (state, id) {
        state.id = id
    },
    updateName (state, name) {
        state.name = name
    },
    updatePlace (state, place) {
        state.place = place
    },
    updateLocation (state, location) {
        state.location = location
    },
    updateCity (state, city) {
        state.city = city
    },
    updateState (state, _state) {
        state.state = _state
    },
    updateAvailableFacilities (state, availableFacilities) {
        state.availableFacilities = availableFacilities
    },
    updateCapacity (state, capacity) {
        state.capacity = capacity
    },
    updateVenueList (state, venueList) {
        state.venueList = venueList
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }