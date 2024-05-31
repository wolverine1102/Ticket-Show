<template>
    <div>
        <div v-if="render">
            <nav class="navbar bg-light border-bottom border-bottom-dark" data-bs-theme="light">
                <div class="container-fluid ms-3">
                    <RouterLink to="/" class="link-dark">
                        <TicketIcon />
                    </RouterLink>

                    <div class="input-group mt-2 mb-1 w-50">
                        <input type="text" class="form-control" placeholder="Search for Movies, Events, Venues"
                            aria-label="Search for Shows, Events" aria-describedby="button-addon2" v-model="searchKey"
                            @keyup.enter="search" />
                        <button class="btn btn-dark" @click="search">Search</button>
                    </div>

                    <RouterLink to="/user/dashboard" class="link-dark me-2" v-if="loggedIn">
                        <PersonIcon />
                    </RouterLink>

                    <RouterLink to="/user/login" class="link-underline-opacity-0 link-dark" v-else>
                        <LoginButton />
                    </RouterLink>
                </div>
            </nav>
        </div>

        <RouterView />

    </div>
</template>


<script>
import { RouterLink, RouterView } from 'vue-router';
import TicketIcon from "./icons/TicketIcon.vue";
import LoginButton from "./icons/LoginButton.vue";
import PersonIcon from "./icons/PersonIcon.vue";
import { mapState } from 'vuex';

export default {
    components: {
        TicketIcon, 
        LoginButton,
        PersonIcon,
    },

    data() {
        return {
            searchKey: null,
        }
    },

    computed: {
        ...mapState({
            currentUserEmail: state => state.CurrentUser.currentUserEmail,
        }),
        keyword: {
            get() {
                return this.$store.state.Search.keyword
            },
            set(keyword) {
                this.$store.commit("Search/updateKeyword", keyword)
            }
        },

        render() {
            const paths = [
                '/user/dashboard',
                '/admin/dashboard',
                '/admin/dashboard/venues',
                '/admin/dashboard/shows',
                '/admin/dashboard/venues/create',
                '/admin/dashboard/venues/' + this.$route.params.id + '/modify',
                '/admin/dashboard/shows/create',
                '/admin/dashboard/shows/' + this.$route.params.id + '/modify',
                '/admin/dashboard/shows/' + this.$route.params.id + '/venues',
                '/admin/dashboard/shows/' + this.$route.params.id + '/add_venue',
                '/admin/dashboard/shows/' + this.$route.params.id + '/modify_venue'
            ]
            if (paths.includes(this.$route.path)) {
                return false;
            }
            else {
                return true;
            }
        },

        loggedIn() {
            if (this.currentUserEmail != null) {
                return true;
            }
            else {
                return false;
            }
        }
    },

    methods: {
        search() {
            if(this.searchKey) {
                this.keyword = this.searchKey
                sessionStorage.keyword = this.keyword
                this.$router.push('/search/' + this.keyword)
                this.searchKey = null
            }
        }
    }
}

</script>