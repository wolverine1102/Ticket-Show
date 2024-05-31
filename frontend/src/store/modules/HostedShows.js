// initial state
const state = () => ({
    id: null,
    showId: null,
    venueId: null,
    timing: null,
    ticketPrice: null,
    language: null,
    startDate: null,
    endDate: null,
    seatsBooked: null,
    hostingVenuesList: null,
    venues: null,
    languagesList: null,
    releaseDate: null
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
    updateShowId (state, showId) {
        state.showId = showId
    },
    updateVenueId (state, venueId) {
        state.venueId = venueId
    },
    updateTiming (state, timing) {
        state.timing = timing
    },
    updateTicketPrice (state, ticketPrice) {
        state.ticketPrice = ticketPrice
    },
    updateLanguage (state, language) {
        state.language = language
    },
    updateStartDate (state, startDate) {
        state.startDate = startDate
    },
    updateEndDate (state, endDate) {
        state.endDate = endDate
    },
    updateseatsBooked (state,seatsBooked) {
        state.seatsBooseatsBooked =seatsBooked
    },
    updateHostingVenuesList (state, hostingVenuesList) {
        state.hostingVenuesList = hostingVenuesList
    },
    updateVenues (state, venues) {
        state.venues = venues
    },
    updateLanguagesList (state, languagesList) {
        state.languagesList = languagesList
    },
    updateReleaseDate (state, releaseDate) {
        state.releaseDate = releaseDate
    },

}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }