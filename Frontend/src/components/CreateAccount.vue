<template>
    <div class="fs-2 fw-semibold mt-2" align="center">Create New Account</div>
    <div class="container-md border border-dark ms-10 mt-3 mb-3">
        <form @submit.prevent="submitForm">
            <div class="m-4 row">
                <label class="col-sm-2 col-form-label"> Email ID </label>
                <div class="col-sm-10">
                    <input type="email" name="email" class="form-control w-50" :class="{ 'is-invalid': emailExists }"
                        v-model="email" @click="emailChange"
                        required />
                    <div v-show="emailExists" class="invalid-feedback">This email id is already associated with an account.
                    </div>
                </div>
            </div>

            <div class="m-4 row">
                <label class="col-sm-2 col-form-label"> First Name </label>
                <div class="col-sm-10">
                    <input type="text" name="first_name" class="form-control w-50" v-model="first_name" required />
                </div>
            </div>

            <div class="m-4 row">
                <label class="col-sm-2 col-form-label"> Last Name </label>
                <div class="col-sm-10">
                    <input type="text" name="last_name" class="form-control w-50" v-model="last_name" required />
                </div>
            </div>

            <div class="m-4 row">
                <label class="col-sm-2 col-form-label"> Password </label>
                <div class="col-sm-10">
                    <input type="password" name="password" class="form-control w-50" :class="{ 'is-invalid': notValid }"
                    v-model="password" required />
                    <div v-show="notValid" class="invalid-feedback">Password should have atleast 12 characters</div>
                </div>
            </div>

            <div class="m-3" align="center">
                <button class="btn btn-dark" :class="{ 'disabled': notValid }" type="submit">Sign Up</button>
            </div>
        </form>
    </div>
</template>



<script>
export default {
    data() {
        return {
            email: null,
            first_name: null,
            last_name: null,
            password: null,
            notValid: '',
            emailExists: false
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

    watch: {
        password(newValue) {
            this.notValid = newValue.length < 12 ? true : false
        },
    },

    methods: {
        emailChange() {
            this.emailExists = false
        },

        async submitForm() {
            const response = await fetch('http://127.0.0.1:5000/user/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "email": this.email,
                    "first_name": this.first_name,
                    "last_name": this.last_name,
                    "password": this.password
                }),
                mode: 'cors'
            })
            if (response.ok) {
                const data = await response.json()
                this.currentUserEmail = data.email
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

                this.$router.push('/')
            }
            else {
                this.emailExists = true
            }
        }
    }
}

</script>