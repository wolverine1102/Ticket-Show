<template>
    <div>
        <br>
        <div class="d-flex justify-content-between">
            <p class="fs-4 ms-3 fw-bolder">{{ venueName }} : {{ showName }} - {{ language }}</p>
            <p class="fs-4 me-3 fw-bolder">{{ timing }}, {{ showDate }}</p>
        </div>
        <div class="container-md border border-dark ms-10 mt-3 mb-3">
            <div class="d-flex justify-content-between">
                <div class="ms-4 mt-4 fs-4 fw-semibold">Available Seats : {{ availableSeats }}</div>
                <div class="me-4 mt-4 fs-4 fw-semibold">Ticket Price : {{ price }}</div>
            </div>
            <form @submit.prevent="confirmBooking">
                <div class="m-4 row">
                    <label class="col-sm-2 col-form-label fs-5 text-center"> Number of Seats </label>
                    <div class="col-sm-10">
                        <input type="number" min="1" class="form-control w-50" :class="{ 'is-invalid': invalid }"
                            v-model="numOfSeats" required />
                        <div v-show="invalid" class="invalid-feedback">Invalid Number of Seats. Please enter again.</div>
                    </div>
                </div>
                <div class="m-4 row">
                    <label class="col-sm-2 col-form-label fs-5 text-center"> Total Amount </label>
                    <div class="col-sm-10">
                        <input type="number" name="ticket_price" class="form-control w-50" :value="totalAmount" disabled />
                    </div>
                </div>
                <div class="m-3" align="center">
                    <button class="btn btn-dark" :class="{ 'disabled': invalid }" type="submit">Confirm Booking</button>
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
            numOfSeats: null,
            totalAmount: null,
            invalid: false,
            language: null,
        }
    },

    computed: {
        ...mapState({
            token: state => state.CurrentUser.token,
            currentUserEmail: state => state.CurrentUser.currentUserEmail,
            showDate: state => state.BookShow.showDate,
            showName: state => state.BookShow.showName,
            numOfSeats: state => state.BookShow.numOfSeats,
        }),
        venueName: {
            get() {
                return this.$store.state.BookShow.venueName
            },
            set(venueName) {
                this.$store.commit("BookShow/updateVenueName", venueName)
            }
        },
        timing: {
            get() {
                return this.$store.state.BookShow.timing
            },
            set(timing) {
                this.$store.commit("BookShow/updateTiming", timing)
            }
        },
        price: {
            get() {
                return this.$store.state.BookShow.price
            },
            set(price) {
                this.$store.commit("BookShow/updatePrice", price)
            }
        },
        availableSeats: {
            get() {
                return this.$store.state.BookShow.availableSeats
            },
            set(availableSeats) {
                this.$store.commit("BookShow/updateAvailableSeats", availableSeats)
            }
        },
    },

    created() {
        fetch('http://127.0.0.1:5000/book_ticket/' + this.showName + '/' + this.$route.params.date + '/' + this.$route.params.hostedShowId, {
            method: 'GET',
            headers: {
                'Authentication-Token': this.token,
            },
            mode: 'cors'
        })
        .then(response => response.json())
        .then(data => {
            if(data != []) {
                this.venueName = data.venueName
                this.timing = data.timing
                this.price = data.price
                this.availableSeats = data.availableSeats
                this.language = data.language
            }
        })
    },

    watch: {
        numOfSeats(newValue) {
            if (newValue <= this.availableSeats) {
                this.totalAmount = newValue * this.price
                this.invalid = false
            }
            else if (newValue > this.availableSeats) {
                this.totalAmount = null
                this.invalid = true
            }
        }
    },

    methods: {
        async confirmBooking() {
            const response = await fetch('http://127.0.0.1:5000/book_ticket/' + this.showName + '/' + this.$route.params.date + '/' + this.$route.params.hostedShowId,  {
                method: 'POST',
                headers: {
                    'Authentication-Token': this.token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "num_of_seats": this.numOfSeats,
                    "email_id": this.currentUserEmail,
                }),
                mode: 'cors'
            })
            if (response.ok) {
                this.$router.push('/')
            }
        }
    }
}

</script>