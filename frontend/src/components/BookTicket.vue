<template>
    <div>
        <br>
        <div class="fs-2 text-dark ms-5 fw-bolder">{{ showName }}</div>
        <div class="container-md ms-5 mt-3 mb-3">
            <form @submit.prevent="submitDate">
                <div class="m-4 row">
                    <label class="col-sm-2 col-form-label fs-5">Choose a Date :</label>
                    <input type="date" :min="startDate" :max="endDate" class="form-control w-50" v-model="date" required>
                    <button class="btn btn-dark col-sm-1 ms-2" type="submit">Next</button>
                </div>
            </form>
        </div>
        <hr class="border border-dark border-2 opacity-75">
        <br>
        <div v-if="venueDict != null">
            <div class="container-md border border-dark ms-10 mt-3 mb-3" v-for="(venueId, index) in Object.keys(venueDict)"
                :key="venueId">
                <div class="row">
                    <div class="fs-4 fw-semibold mt-2">{{ venueList[index] }}</div>
                    <div v-for="show in venueDict[venueId]" class="col-sm-3 mb-3 ms-3 mt-2">
                        <div class="card" style="width: 18rem;">
                            <div class="card-body">
                                <ul>
                                    <li><span class="fw-semibold">Language</span> : {{ show.language }}</li>
                                    <li><span class="fw-semibold">Timing</span> : {{ show.timing }}</li>
                                    <li><span class="fw-semibold">Date</span> : {{ showDate }}</li>
                                </ul>

                                <p v-if="show.availableSeats === 0" class="text-center">
                                    <RouterLink :to="'/book_ticket/' + showName + '/' + date + '/' + show.showId"
                                        @click="bookTicket(show.date, show.showId)" class="btn btn-dark disabled">
                                        Book</RouterLink>
                                </p>

                                <p v-else class="text-center">
                                    <RouterLink :to="'/book_ticket/' + showName + '/' + date + '/' + show.showId"
                                        @click="bookTicket(date, show.showId)" class="btn btn-dark">Book
                                    </RouterLink>
                                </p>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>



<script>
import { mapState } from 'vuex';

export default {
    data() {
        return {
            date: null,
            venueList: null,
            venueDict: null,
        }
    },

    computed:{
        ...mapState({
            token: state => state.CurrentUser.token,
        }),
        showName: {
            get() {
                return this.$store.state.BookShow.showName
            },
            set(showName) {
                this.$store.commit("BookShow/updateShowName", showName)
            }
        },
        startDate: {
            get() {
                return this.$store.state.BookShow.startDate
            },
            set(startDate) {
                this.$store.commit("BookShow/updateStartDate", startDate)
            }
        },
        endDate: {
            get() {
                return this.$store.state.BookShow.endDate
            },
            set(endDate) {
                this.$store.commit("BookShow/updateEndDate", endDate)
            }
        },
        showDate: {
            get() {
                return this.$store.state.BookShow.showDate
            },
            set(showDate) {
                this.$store.commit("BookShow/updateShowDate", showDate)
            }
        },
    },

    created() {
        this.showName = this.$route.params.showName
        fetch('http://127.0.0.1:5000/book_ticket/' + this.showName, {
            method: 'GET',
            headers: {
                'Authentication-Token': this.token,
            },
            mode: 'cors'
        })
        .then(response => response.json())
        .then(data => {
            if(data != []) {
                this.startDate = data.startDate,
                this.endDate = data.endDate
            }
        })
    },

    methods: {
        bookTicket(date, id) {
            this.$router.push('/book_ticket/' + this.showName + '/' + date + '/' + id)
        },

        async submitDate() {
            const response = await fetch('http://127.0.0.1:5000/book_ticket/' + this.showName, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
                body: JSON.stringify({
                    "date": this.date,
                }),
                mode: 'cors'
            })
            if (response.ok) {
                const data = await response.json()
                this.venueDict = data.venueDict
                this.venueList = data.venueList
                this.showDate = data.showDate
            }
        },
    }
}

</script>