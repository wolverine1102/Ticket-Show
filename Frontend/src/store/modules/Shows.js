// initial state
const state = () => ({
    id: null,
    name: null,
    rating: null,
    category: null,
    tags: null,
    languages: null,
    duration: null,
    releaseDate: null,
    description: null,
    photo: null,
    showList: null
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
    updateRating (state, rating) {
        state.rating = rating
    },
    updateCategory (state, category) {
        state.category = category
    },
    updateTags (state, tags) {
        state.tags = tags
    },
    updateLanguages (state, languages) {
        state.languages = languages
    },
    updateDuration (state, duration) {
        state.duration = duration
    },
    updateReleaseDate (state, releaseDate) {
        state.releaseDate = releaseDate
    },
    updateDescription (state, description) {
        state.description = description
    },
    updatePhoto (state, photo) {
        state.photo = photo
    },
    updateShowList (state, showList) {
        state.showList = showList
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }