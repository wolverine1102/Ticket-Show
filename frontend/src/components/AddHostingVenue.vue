<template>
    <div>
        <div class="fs-2 fw-semibold mt-2" align="center">Add a Venue</div>
        <div class="container-md border border-dark ms-10 mt-3 mb-3">
            <div align="center" v-show="showExists">
                <div class="alert alert-danger d-flex align-items-center mt-3 w-75" role="alert">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-info-circle-fill" viewBox="0 0 16 16">
                        <path
                            d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z" />
                    </svg>
                    <div class="ps-2"><strong>This show already exists. Change the venue or the timing.</strong></div>
                </div>
            </div>

            <form @submit.prevent>
                <div class="row mt-3 ms-4">
                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Venue Name </label>
                        <div class="col-sm-10">
                            <select v-model="venueId" class="form-select w-50 text-bg-light" required>
                                <option value="null" disabled label="Select a Venue"></option>
                                <option v-for="venue in venues" :value="venue.id">
                                    {{ venue.name }}</option>
                            </select>
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Show Timing </label>
                        <div class="col-sm-10">
                            <input type="time" name="timing" class="form-control w-50" v-model="timing" required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Ticket Price </label>
                        <div class="col-sm-10">
                            <input type="text" name="ticket_price" class="form-control w-50" v-model="ticketPrice"
                                required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Language </label>
                        <div class="col-sm-10">
                            <select class="form-select w-50 text-bg-light" v-model="language" required>
                                <option value="null" disabled label="Select Language"></option>
                                <option v-for="language in languagesList" :value="language">
                                    {{ language }}</option>
                            </select>
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Start Date </label>
                        <div class="col-sm-10">
                            <input type="date" name="start_date" class="form-control w-50" :min=releaseDate
                                v-model="startDate" required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> End Date </label>
                        <div class="col-sm-10">
                            <input type="date" name="end_date" class="form-control w-50" :min=releaseDate v-model="endDate"
                                required />
                        </div>
                    </div>

                    <div class="row m-3">
                        <div class="col-sm-10">
                            <button class="btn btn-dark" type="submit" value="another"
                                @click="submitForm($event.target.value)">Add Another Venue</button>
                            <button class=" ms-2 btn btn-dark" type="submit" value="exit"
                                @click="submitForm($event.target.value)">Add Venue & Exit</button>
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
            showExists: false,
        }
    },

    computed: {
        ...mapState({
            token: state => state.CurrentUser.token
        }),
        showId: {
            get() {
                return this.$store.state.HostedShows.showId
            },
            set(showId) {
                this.$store.commit("HostedShows/updateShowId", showId)
            }
        },
        venueId: {
            get() {
                return this.$store.state.HostedShows.venueId
            },
            set(venueId) {
                this.$store.commit("HostedShows/updateVenueId", venueId)
            }
        },
        timing: {
            get() {
                return this.$store.state.HostedShows.timing
            },
            set(timing) {
                this.$store.commit("HostedShows/updateTiming", timing)
            }
        },
        ticketPrice: {
            get() {
                return this.$store.state.HostedShows.ticketPrice
            },
            set(ticketPrice) {
                this.$store.commit("HostedShows/updateTicketPrice", ticketPrice)
            }
        },
        language: {
            get() {
                return this.$store.state.HostedShows.language
            },
            set(language) {
                this.$store.commit("HostedShows/updateLanguage", language)
            }
        },
        startDate: {
            get() {
                return this.$store.state.HostedShows.startDate
            },
            set(startDate) {
                this.$store.commit("HostedShows/updateStartDate", startDate)
            }
        },
        endDate: {
            get() {
                return this.$store.state.HostedShows.endDate
            },
            set(endDate) {
                this.$store.commit("HostedShows/updateEndDate", endDate)
            }
        },
        venues: {
            get() {
                return this.$store.state.HostedShows.venues
            },
            set(venues) {
                this.$store.commit("HostedShows/updateVenues", venues)
            }
        },
        languagesList: {
            get() {
                return this.$store.state.HostedShows.languagesList
            },
            set(languagesList) {
                this.$store.commit("HostedShows/updateLanguagesList", languagesList)
            }
        },
        releaseDate: {
            get() {
                return this.$store.state.HostedShows.releaseDate
            },
            set(releaseDate) {
                this.$store.commit("HostedShows/updateReleaseDate", releaseDate)
            }
        },
    },

    created() {
        fetch('http://127.0.0.1:5000/admin/dashboard/shows/' + this.$route.params.id + '/add_venue', {
            method: 'GET',
            headers: {
                'Authentication-Token': this.token,
            },
            mode: 'cors'
        })
        .then(response => response.json())
        .then(data => {
            this.venues = data.venues
            this.releaseDate = data.releaseDate
            this.languagesList = data.languages
            this.showId = this.$route.params.id
        })
        this.venueId = null
        this.timing = null
        this.language = null
        this.ticketPrice = null
        this.startDate = null
        this.endDate = null
    },

    methods: {
        async submitForm(value) {
            const response = await fetch('http://127.0.0.1:5000/admin/dashboard/shows/' + this.showId + '/add_venue', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
                body: JSON.stringify({
                    "venue_id": this.venueId,
                    "timing": this.timing,
                    "ticket_price": this.ticketPrice,
                    "language": this.language,
                    "start_date": this.startDate,
                    "end_date": this.endDate,
                }),
                mode: 'cors'
            })
            if (response.ok) {
                console.log(value)
                if (value === 'another') {
                    this.venueId = null
                    this.timing = null
                    this.language = null
                    this.ticketPrice = null
                    this.startDate = null
                    this.endDate = null
                    this.$router.push('/admin/dashboard/shows/' + this.showId + '/add_venue')
                }
                else {
                    this.$router.push('/admin/dashboard/shows/' + this.showId + '/venues')
                }
            }
            else {
                this.showExists = true
            }
        }
    }
}

</script>