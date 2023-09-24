<template>
    <div>
        <nav class="navbar bg-light border-bottom border-bottom-dark" data-bs-theme="light">
            <div class="container-fluid ms-3">
                <RouterLink to="/" class="link-dark">
                    <TicketIcon />
                </RouterLink>

                <ul class="nav nav-underline">
                    <li class="nav-item">
                        <RouterLink to="/admin/dashboard/venues" class="nav-link fs-5 text-black fw-semibold">VENUES
                        </RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink to="/admin/dashboard/shows" class="nav-link fs-5 text-black fw-semibold">SHOWS
                        </RouterLink>
                    </li>
                </ul>

                <div class="me-3 mt-2" align="right">
                    <p type="button" class="fs-5 fw-medium bs-dark-text-emphasis" @click="logout"> Logout </p>
                </div>
            </div>
        </nav>
        <RouterView />
    </div>
</template>


<script>
import { RouterLink, RouterView } from 'vue-router';
import TicketIcon from "./icons/TicketIcon.vue";

export default {
    components: {
        TicketIcon,
    },

    computed: {
        currentUserEmail: {
            get() {
                return this.$store.state.CurrentUser.currentUserEmail
            },
            set(email) {
                this.$store.commit("CurrentUser/updateCurrentUserEmail", email)
            }
        },
        currentUserFirstName: {
            get() {
                return this.$store.state.CurrentUser.currentUserFirstName
            },
            set(first_name) {
                this.$store.commit("CurrentUser/updateCurrentUserFirstName", first_name)
            }
        },
        currentUserLastName: {
            get() {
                return this.$store.state.CurrentUser.currentUserLastName
            },
            set(last_name) {
                this.$store.commit("CurrentUser/updateCurrentUserLastName", last_name)
            }
        },
        currentUserRoles: {
            get() {
                return this.$store.state.CurrentUser.currentUserRoles
            },
            set(roles) {
                this.$store.commit("CurrentUser/updateRoles", roles)
            }
        },
        token: {
            get() {
                return this.$store.state.CurrentUser.token
            },
            set(token) {
                this.$store.commit("CurrentUser/updateToken", token)
            }
        },
    },

    methods: {
        async logout() {
            const response = await fetch('http://127.0.0.1:5000/user/logout', {
                method: 'GET',
                headers: {
                    'Authentication-Token': this.token
                },
                mode: 'cors'
            })
            if (response.ok) {
                this.currentUserEmail = null;
                this.currentUserFirstName = null;
                this.currentUserLastName = null;
                this.currentUserRoles = null;
                this.token = null;

                sessionStorage.removeItem('email')
                sessionStorage.removeItem('first_name')
                sessionStorage.removeItem('last_name')
                sessionStorage.removeItem('roles')
                sessionStorage.removeItem('token')

                this.$router.push('/')
            }
        }
    }
}

</script>