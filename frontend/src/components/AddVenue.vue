<template>
    <div>
        <div class="fs-2 fw-semibold mt-2" align="center">Add New Venue</div>
        <div class="container-md border border-dark ms-10 mt-3 mb-3">
            <form @submit.prevent="submitForm">
                <div class="row mt-3 ms-4">
                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Venue ID </label>
                        <div class="col-sm-10">
                            <input v-model="id" type="text" name="id" class="form-control w-50"
                                :class="{ 'is-invalid': venueExists }" required />
                            <div v-show="venueExists" class="invalid-feedback">This venue id is already exists.</div>
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Name </label>
                        <div class="col-sm-10">
                            <input v-model="name" type="text" name="name" class="form-control w-50" required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Place </label>
                        <div class="col-sm-10">
                            <input v-model="place" type="text" name="place" class="form-control w-50" required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Location </label>
                        <div class="col-sm-10">
                            <input v-model="location" type="text" name="location" class="form-control w-50" required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> City </label>
                        <div class="col-sm-10">
                            <input v-model="city" type="text" name="city" class="form-control w-50" required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> State </label>
                        <div class="col-sm-10">
                            <input v-model="state" type="text" name="state" class="form-control w-50" required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Available Facilities </label>
                        <div class="col-sm-10">
                            <input v-model="availableFacilities" type="text" name="available_facilities"
                                class="form-control w-50" />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Capacity </label>
                        <div class="col-sm-10">
                            <input v-model="capacity" type="number" name="capacity" class="form-control w-50" required />
                        </div>
                    </div>
                    <div class="row m-3">
                        <div class="col-sm-10">
                            <button class="btn btn-dark" type="submit">Add Venue</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>


<script>
import { mapState } from 'vuex';

export default {
    data() {
        return {
            venueExists: false
        }
    },

    computed:{
        ...mapState({
            token: state => state.CurrentUser.token
        }),
        id: {
            get() {
                return this.$store.state.Venues.id
            },
            set(id) {
                this.$store.commit("Venues/updateId", id)
            }
        },
        name: {
            get() {
                return this.$store.state.Venues.name
            },
            set(name) {
                this.$store.commit("Venues/updateName", name)
            }
        },
        place: {
            get() {
                return this.$store.state.Venues.place
            },
            set(place) {
                this.$store.commit("Venues/updatePlace", place)
            }
        },
        location: {
            get() {
                return this.$store.state.Venues.location
            },
            set(location) {
                this.$store.commit("Venues/updateLocation", location)
            }
        },
        city: {
            get() {
                return this.$store.state.Venues.city
            },
            set(city) {
                this.$store.commit("Venues/updateCity", city)
            }
        },
        state: {
            get() {
                return this.$store.state.Venues.state
            },
            set(state) {
                this.$store.commit("Venues/updateState", state)
            }
        },
        availableFacilities: {
            get() {
                return this.$store.state.Venues.availableFacilities
            },
            set(availableFacilities) {
                this.$store.commit("Venues/updateAvailableFacilities", availableFacilities)
            }
        },
        capacity: {
            get() {
                return this.$store.state.Venues.capacity
            },
            set(capacity) {
                this.$store.commit("Venues/updateCapacity", capacity)
            }
        },
        
    },

    created() {
        this.id = null
        this.name = null
        this.place = null
        this.location = null
        this.city = null
        this.state = null
        this.availableFacilities = null
        this.capacity = null
    },

    methods: {
        async submitForm() {
            const response = await fetch('http://127.0.0.1:5000/admin/dashboard/venues/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token
                },
                body: JSON.stringify({
                    "id": this.id,
                    "name": this.name,
                    "place": this.place,
                    "location": this.location,
                    "city": this.city,
                    "state": this.state,
                    "available_facilities": this.availableFacilities,
                    "capacity": this.capacity
                }),
                mode: 'cors'
            })
            if (response.ok) {
                this.$router.push('/admin/dashboard/venues')
            }
            else {
                this.venueExists = true
            }
        }
    }
}

</script>