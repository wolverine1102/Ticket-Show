<template>
    <div>
        <div class="container-sm border border-light-subtle ms-10 mt-5 mb-3 w-50">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title fs-2">{{ venueList.name }}</h5>
                    <h6 class="card-subtitle mb-2 fw-light">{{
                        venueList.place + ',' + ' ' + venueList.location + ',' + ' ' +
                        venueList.city + ',' + ' ' + venueList.state
                    }}</h6>
                    <div class="card-text">
                        <section>
                            <div>
                                <span class="fs-6 fw-semibold">Available Facilities : </span>
                                <span>{{ venueList.availableFacilities }}</span>
                            </div>
                        </section>
                    </div>
                    <br>
                    <p class="fs-5 fw-semibold">Hosted Shows :</p>
                    <hr class="border border-dark border-2 opacity-75">
                    <div class="list-group" v-for="show in showList">
                        <RouterLink :to="'/book_ticket/' + show" class="list-group-item 
                                list-group-item-action list-group-item-secondary fw-medium">{{ show }}</RouterLink>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>



<script>
export default {
    computed: {
        venueList: {
            get() {
                return this.$store.state.Search.venueList
            },
            set(venueList) {
                this.$store.commit("Search/updateVenueList", venueList)
            }
        },
        showList: {
            get() {
                return this.$store.state.Search.showList
            },
            set(showList) {
                this.$store.commit("Search/updateShowList", showList)
            }
        },
    },

    created() {
        fetch('http://127.0.0.1:5000/venues/' + this.$route.params.name, {
            method: 'GET',
            mode: 'cors'
        })
        .then(response => response.json())
        .then(data => {
            if(data != []) {
                this.showList = data.shows,
                this.venueList = data.venues
            }
        })
    }
}

</script>