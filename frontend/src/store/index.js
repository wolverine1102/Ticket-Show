import { createStore } from 'vuex'
import CurrentUser from "./modules/CurrentUser.js";
import Venues from "./modules/Venues.js";
import Shows from "./modules/Shows.js";
import HostedShows from "./modules/HostedShows.js";
import Search from "./modules/Search.js";
import BookShow from "./modules/BookShow.js";

const store = createStore({
    modules: {
        CurrentUser,
        Venues,
        Shows,
        HostedShows,
        Search,
        BookShow,
    },
})

export default store;