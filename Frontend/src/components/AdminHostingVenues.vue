<template>
    <div>
        <div align="right" class="me-2 mb-1 mt-2">
            <RouterLink class="nav-link fw-semibold text-black" aria-current="page"
                :to="'/admin/dashboard/shows/' + showId + '/add_venue'">
                + Add a Venue </RouterLink>
        </div>
        <table class="table">
            <thead class="table-dark">
                <tr>
                    <th scope="col" class="fs-6">S.No</th>
                    <th scope="col" class="fs-6">Name</th>
                    <th scope="col" class="fs-6">Timing</th>
                    <th scope="col" class="fs-6">Ticket Price</th>
                    <th scope="col" class="fs-6">Language</th>
                    <th scope="col" class="fs-6">Start Date</th>
                    <th scope="col" class="fs-6">End Date</th>
                    <th scope="col" class="fs-6"></th>
                    <th scope="col" class="fs-6"></th>
                </tr>
            </thead>
            <tbody v-for="(hostingVenue, index) in hostingVenuesList" :key="hostingVenue.id">
                <tr>
                    <th scope="row"> {{ index + 1 }} </th>
                    <td> {{ hostingVenue.name }} </td>
                    <td> {{ hostingVenue.timing }} </td>
                    <td> {{ hostingVenue.ticketPrice }} </td>
                    <td> {{ hostingVenue.language }} </td>
                    <td> {{ hostingVenue.startDate }} </td>
                    <td> {{ hostingVenue.endDate }} </td>
                    <td>
                        <RouterLink :to="'/admin/dashboard/shows/' + hostingVenue.id + '/modify_venue'"
                            class="link-underline-opacity-0 link-dark fw-medium">
                            Modify</RouterLink>
                    </td>
                    <td class="btn btn-link fw-medium link-underline link-underline-opacity-0" type="button"
                        @click="deleteVenue(hostingVenue.name, hostingVenue.id)">Delete</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>


<script>
import { mapState } from 'vuex';

export default {
    computed: {
        ...mapState({
            token: state => state.CurrentUser.token
        }),
        hostingVenuesList: {
            get() {
                return this.$store.state.HostedShows.hostingVenuesList
            },
            set(hostingVenuesList) {
                this.$store.commit("HostedShows/updateHostingVenuesList", hostingVenuesList)
            }
        },
        showId: {
            get() {
                return this.$store.state.HostedShows.showId
            },
            set(showId) {
                this.$store.commit("HostedShows/updateShowId", showId)
            }
        },
    },

    created() {
        fetch('http://127.0.0.1:5000/admin/dashboard/shows/' + this.$route.params.id + '/venues', {
            method: 'GET',
            headers: {
                'Authentication-Token': this.token,
            },
            mode: 'cors'
        })
        .then(response => response.json())
        .then(data => {
            this.showId = this.$route.params.id
            if(data != []) {
                this.hostingVenuesList = data
            }
        })
    },

    methods: {
        deleteVenue(name, id) {
            const result = confirm('Are you sure you want to delete Show - ' + name + '?')
            if (result) {
                this.delete(id)
            }
        },

        async delete(id) {
            const response = await fetch('http://127.0.0.1:5000/admin/dashboard/shows/' + id + '/delete_venue', {
                method: 'GET',
                headers: {
                    'Authentication-Token': this.token,
                },
                mode: 'cors'
            })
            if (response.ok) {
                fetch('http://127.0.0.1:5000/admin/dashboard/shows/' + this.showId + '/venues', {
                    method: 'GET',
                    headers: {
                        'Authentication-Token': this.token,
                    },
                    mode: 'cors'
                })
                .then(response => response.json())
                .then(data => {
                    if(data != []) {
                        this.hostingVenuesList = data
                    }
                })
            }
        },
    },

}

</script>