<template>
    <div>
        <div class="fs-2 fw-semibold mt-2" align="center">Modify Venue</div>
        <div class="container-md border border-dark ms-10 mt-3 mb-3 w-75">
            <form @submit.prevent="submitForm">
                <div class="row mt-3 ms-4">
                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Venue Name </label>
                        <div class="col-sm-10">
                            <select class="form-select w-50 text-bg-light" disabled readonly required>
                                <option :value="venueId" :label="venueName"></option>
                            </select>
                        </div>
                    </div>
                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Show Timing </label>
                        <div class="col-sm-10">
                            <input type="time" name="timing" class="form-control w-50" :value="timing" disabled readonly
                                required />
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
                                <option selected :value="language">{{ language }}</option>
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
                            <button class="ms-2 btn btn-dark" type="submit">Modify Venue</button>
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
            venueName: null,
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
        fetch('http://127.0.0.1:5000/admin/dashboard/shows/' + this.$route.params.id + '/modify_venue', {
            method: 'GET',
            headers: {
                'Authentication-Token': this.token,
            },
            mode: 'cors'
        })
        .then(response => response.json())
        .then(data => {
            this.venueId = data.venueId
            this.timing = data.timing
            this.languagesList = data.languageList
            this.ticketPrice = data.ticketPrice
            this.language = data.language
            this.venueName = data.name
            this.startDate = data.startDate
            this.endDate = data.endDate
            this.releaseDate = data.releaseDate
            this.showId = data.showId
        })
    },

    methods: {
        async submitForm() {
            const response = await fetch('http://127.0.0.1:5000/admin/dashboard/shows/' + this.$route.params.id + '/modify_venue', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
                body: JSON.stringify({
                    "timing": this.timing,
                    "ticket_price": this.ticketPrice,
                    "language": this.language,
                    "start_date": this.startDate,
                    "end_date": this.endDate,
                }),
                mode: 'cors'
            })
            if (response.ok) {
                    this.$router.push('/admin/dashboard/shows/' + this.showId + '/venues')
                }
            
        }
    }
}

</script>