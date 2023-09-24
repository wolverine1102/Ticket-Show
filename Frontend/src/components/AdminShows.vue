<template>
    <div>
        <div align="right" class="me-2 mb-1 mt-2">
            <RouterLink class="nav-link fw-semibold text-black me-2" aria-current="page" to="/admin/dashboard/shows/create">
                + Add a Show </RouterLink>
        </div>

        <div class="card mt-3 w-75 ms-5 mb-3" v-for="(show, index) in showList" :key="show.id">
            <div class="card-header text-bg-dark">
                <RouterLink :to="'/admin/dashboard/shows/' + show.id + '/venues'" class="link-light link-underline 
                    link-underline-opacity-0 fw-semibold fs-5">{{ show.name }}</RouterLink>
            </div>
            <div class="card-body">
                <p class="card-text"><span class="fw-semibold">Rating</span>: {{ show.rating }}</p>
                <p class="card-text"><span class="fw-semibold">Category</span>: {{ show.category }}</p>
                <p class="card-text"><span class="fw-semibold">Tags</span>: {{ show.tags }}</p>
                <p class="card-text"><span class="fw-semibold">Languages</span>: {{ show.languages }}</p>
                <p class="card-text"><span class="fw-semibold">Duration</span>: {{ show.duration }}</p>
                <p class="card-text"><span class="fw-semibold">Release Date</span>: {{ show.release_date }}</p>
                <p class="card-text"><span class="fw-semibold">Description</span>: {{ show.description }}</p>
                <RouterLink :to="'/admin/dashboard/shows/' + show.id + '/modify'" class="btn btn-link fs-5
                    fw-semibold text-black link-underline link-underline-opacity-0"> Modify </RouterLink>

                <div class="btn btn-link text-black fs-5 fw-semibold link-underline link-underline-opacity-0"
                    @click="deleteShow(show.name, show.id)"> Delete </div>
            </div>
        </div>
    </div>
</template>


<script>
import { mapState } from 'vuex';

export default {
    computed: {
        ...mapState({
            token: state => state.CurrentUser.token
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
        fetch('http://127.0.0.1:5000/admin/dashboard/shows/', {
            method: 'GET',
            headers: {
                'Authentication-Token': this.token,
            },
            mode: 'cors'
        })
        .then(response => response.json())
        .then(data => {
            if(data != []) {
                this.showList = data
            }
        })
    },

    methods: {
        deleteShow(name, id) {
            const result = confirm('Are you sure you want to delete Show - ' + name + '?')
            if (result) {
                this.delete(id)
            }
        },

        async delete(id) {
            const response = await fetch('http://127.0.0.1:5000/admin/dashboard/shows/' + id + '/delete', {
                method: 'GET',
                headers: {
                    'Authentication-Token': this.token
                },
                mode: 'cors'
            })
            if (response.ok) {
                fetch('http://127.0.0.1:5000/admin/dashboard/shows/', {
                    method: 'GET',
                    headers: {
                        'Authentication-Token': this.token,
                    },
                    mode: 'cors'
                })
                .then(response => response.json())
                .then(data => {
                    if(data != []) {
                        this.showList = data
                    }
                })
            }
        },
    },

}

</script>