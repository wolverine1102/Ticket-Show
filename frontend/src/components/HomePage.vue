<template>
    <div>
        <div class="container-md ms-10 mt-3 mb-3">
            <div class="row row-cols-2">
                <div class="card g-1 w-50" v-for="(show, index) in showList" :key="show.id">
                    <div class="row g-0">
                        <div class="col-md-4">
                            <img :src="show.photo" class="img-thumbnail rounded-start" alt="..." />
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
    </div>
</template>


<script>
import { RouterLink, RouterView } from 'vue-router';
import { mapState } from 'vuex';

export default {
    computed: {
        ...mapState({
            currentUserEmail: state => state.CurrentUser.currentUserEmail,
            currentUserFirstName: state => state.CurrentUser.currentUserFirstName,
            currentUserLastName: state => state.CurrentUser.currentUserLastName,
            currentUserRoles: state => state.CurrentUser.currentUserRoles,
            token: state => state.CurrentUser.token,
        }),
        showList: {
            get() {
                return this.$store.state.Shows.showList
            },
            set(showList) {
                this.$store.commit("Shows/updateShowList", showList)
            }
        },
    },

    created() {
        fetch('http://127.0.0.1:5000/home/', {
            method: 'GET',
            mode: 'cors'
        })
        .then(response => response.json())
        .then(data => {
            if(data != []) {
                this.showList = data
            }
        })
    },
}

</script>