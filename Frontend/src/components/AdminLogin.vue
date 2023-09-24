<template>
    <div>
        <div class="fs-2 fw-semibold mt-2" align="center"> Admin Login</div>
        <div class="container-md border border-dark ms-10 mt-3 mb-3">
            <div align="center" v-show="incorrectCredentials">
                <div class="alert alert-danger d-flex align-items-center mt-3 w-75" role="alert">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-info-circle-fill" viewBox="0 0 16 16">
                        <path
                            d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z" />
                    </svg>
                    <div class="ps-2" v-if="notAuthorized"><strong>You are not authorized to view this page.</strong></div>
                    <div class="ps-2" v-else><strong>Bad Credentials. Please login again.</strong></div>
                </div>
            </div>
            <form @submit.prevent="submitForm">
                <div class="m-4 row">
                    <label class="col-sm-2 col-form-label"> Email ID </label>
                    <div class="col-sm-10">
                        <input type="email" name="email" class="form-control w-50" v-model="email" required />
                    </div>
                </div>

                <div class="m-4 row">
                    <label class="col-sm-2 col-form-label">Password</label>
                    <div class="col-sm-10">
                        <input type="password" name="password" class="form-control w-50" v-model="password" required />
                    </div>
                </div>

                <div class="m-3" align="center">
                    <button class="btn btn-dark" type="submit">Sign in</button>
                </div>
            </form>
        </div>
    </div>
</template>



<script>
export default {
    data() {
        return {
            email: null,
            password: null,
            incorrectCredentials: false,
            notAuthorized: false,
            role: 'admin'
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

    methods: {
        async submitForm() {
            const response = await fetch('http://127.0.0.1:5000/user/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "email": this.email,
                    "password": this.password,
                    "role": this.role
                }),
                mode: 'cors'
            })
            if (response.ok) {
                const data = await response.json()
                this.currentUserEmail = data.email,
                this.currentUserFirstName = data.first_name
                this.currentUserLastName = data.last_name
                this.currentUserRoles = data.roles
                this.token = data.token
                console.log('Success')
                
                sessionStorage.email = this.currentUserEmail
                sessionStorage.first_name = this.currentUserFirstName
                sessionStorage.last_name = this.currentUserLastName
                sessionStorage.roles = this.currentUserRoles
                sessionStorage.token = this.token

                this.$router.push('/admin/dashboard/venues')
            }
            else {
                this.incorrectCredentials = true
                if (response.status === 403) {
                    this.notAuthorized = true
                }
            }
        }
    }
}

</script>