<template>
    <div>
        <nav class="navbar bg-body-tertiary fixed-top">
            <div class="container-fluid">
                <a class="navbar-brand fs-3 ms-3 fw-semibold">Welcome {{ currentUserFirstName }}, </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar"
                    aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar"
                    aria-labelledby="offcanvasNavbarLabel">
                    <div class="offcanvas-header">
                        <h5 class="offcanvas-title fw-semibold fs-4" id="offcanvasNavbarLabel">MENU</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                    </div>
                    <div class="offcanvas-body">
                        <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                            <li class="nav-item">
                                <RouterLink to="/" class="nav-link active fs-5 bs-dark-text-emphasis" aria-current="page">
                                    Home</RouterLink>
                            </li>
                            <li class="nav-item">
                                <RouterLink to="/admin/dashboard/venues" class="nav-link active fs-5 bs-dark-text-emphasis"
                                    aria-current="page">Admin Dashboard</RouterLink>
                            </li>
                            <li class="nav-item">
                                <p type="button" class="fs-5 bs-dark-text-emphasis mt-1" @click="logout">Logout</p>
                            </li>
                        </ul>
                    </div>
                    <div class="offcanvas-header">
                        <p type="button" class="btn btn-link fs-6 link-dark mt-1 link-underline link-underline-opacity-0"
                            :class="{ 'disabled': disabled }" @click="triggerExport">Export Venues as CSV</p>
                    </div>
                </div>
            </div>
        </nav>
        <br><br><br>
        <div class="m-4 fs-4 fw-semibold">Your Ticktes</div>
        <hr class="border border-dark border-2 opacity-75">
        <div class="container-lg ms-6 mb-3">
            <div class="row justify-content-center">
                <div class="card w-75 mt-3" v-for="(bookedShow, index) in bookedShowsList">
                    <div class="card-body">
                        <h5 class="card-title fw-medium fs-4">{{ bookedShow.show }} - {{ bookedShow.language }}</h5>
                        <h6 class="card-subtitle mb-2 text-body-secondary">{{ bookedShow.venue }}</h6>
                        <p class="card-text fw-semibold">{{ bookedShow.date }} | {{ bookedShow.timing }}</p>
                        <p class="card-text fw-semibold">{{ bookedShow.numOfSeats }} ticket</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>



<script>
export default {
    data() {
        return {
            bookedShowsList: null,
            disabled: !sessionStorage.roles.includes('admin')
        }
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

    created() {
        fetch('http://127.0.0.1:5000/user/dashboard', {
            method: 'GET',
            headers: {
                'Authentication-Token': this.token,
            },
            mode: 'cors'
        })
        .then(response => response.json())
        .then(data => {
            if(data != []) {
                this.bookedShowsList = data.bookedShowsList
            }
        })
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
        },

        async triggerExport() {
            const response = await fetch('http://127.0.0.1:5000/export_csv', {
                method: 'GET',
                headers: {
                    'Authentication-Token': this.token
                },
                mode: 'cors'
            })
            if (response.ok) {
                const data = await response.json()
                if (data.state === 'SUCCESS') {
                    window.location.href = 'http://127.0.0.1:5000/download'
                    alert('CSV files downloaded successfully')
                }
            }
        }
    }
}

</script>