<template>
    <div>
        <div class="fs-2 ms-4 mt-4">Search result for "{{ keyword }}" </div>
        <div class="m-4 fs-4 fw-semibold">MOVIES and EVENTS</div>
        <hr class="border border-dark border-2 opacity-75">
        <div class="container-md ms-10 mt-3 mb-3">
            <div class="row row-cols-2">

                <div class="card g-1 w-50" v-for="(show, index) in showList" :key="show.id">
                    <div class="row g-0">
                        <div class="col-md-4">
                            <img :src="show.photo" class="img-thumbnail rounded-start" alt="...">
                        </div>
                        <div class="col-md-8">
                            <div class="card-body">
                                <h5 class="card-title">{{ show.name }}</h5>
                                <p class="card-text fw-lighter">{{ show.description }}</p>
                                <div>
                                    <ul class="fw-semibold">
                                        <li v-if="show.rating != null">{{ show.rating }}/10</li>
                                        <li>{{ show.languages }}</li>
                                        <li>{{ show.tags }}</li>
                                        <li>{{ show.release_date }}</li>
                                        <li>{{ show.duration }}</li>
                                    </ul>
                                </div>
                                <RouterLink :to="'/book_ticket/' + show.name" class=" btn btn-dark"> Book Ticket
                                </RouterLink>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="m-4 fs-4 fw-semibold">VENUES</div>
        <hr class="border border-dark border-2 opacity-75">
        <div class="container-sm ms-10 mt-3 mb-3 w-50">
            <div class="list-group">

                <RouterLink :to="'/venues/' + venue.name" class="list-group-item list-group-item-action" aria-current="true"
                    v-for="(venue, index) in venueList" :key="venue.id">
                    <div class="d-flex w-50 justify-content-between">
                        <h5 class="mb-1">{{ venue.name }}</h5>
                    </div>
                    <p class="mb-1">{{ venue.place + ',' + ' ' + venue.location + ',' + ' ' + venue.city + ',' + ' ' +
                        venue.state }}
                    </p>
                </RouterLink>

            </div>
        </div>
    </div>
</template>



<script>
export default {
    computed: {
        keyword: {
            get() {
                return this.$store.state.Search.keyword
            },
            set(keyword) {
                this.$store.commit("Search/updateKeyword", keyword)
            }
        },
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
        this.keyword = sessionStorage.keyword;
        fetch('http://127.0.0.1:5000/search/' + this.keyword, {
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
    },

    watch: {
        keyword(newValue) {
            fetch('http://127.0.0.1:5000/search/' + newValue, {
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
}

</script>