<template>
    <div>
        <div align="right" class="me-2 mb-1 mt-2">
            <RouterLink class="nav-link fw-semibold text-black" aria-current="page" to="/admin/dashboard/venues/create">
                + Add a Venue </RouterLink>
        </div>
        <table class="table">
            <thead class="table-dark">
                <tr>
                    <th scope="col" class="fs-6">S.No</th>
                    <th scope="col" class="fs-6">Name</th>
                    <th scope="col" class="fs-6">Address</th>
                    <th scope="col" class="fs-6">Available Facilities</th>
                    <th scope="col" class="fs-6">Capacity</th>
                    <th scope="col" class="fs-6"></th>
                    <th scope="col" class="fs-6"></th>
                </tr>
            </thead>
            <tbody v-for="(venue, index) in venueList" :key="venue.id">
                <tr>
                    <th scope="row"> {{ index + 1 }} </th>
                    <td> {{ venue.name }} </td>
                    <td> {{ venue.place + ',' + ' ' + venue.location + ',' + ' ' + venue.city + ',' + ' ' +
                        venue.state }} </td>
                    <td> {{ venue.available_facilities }} </td>
                    <td> {{ venue.capacity }} </td>
                    <td>
                        <RouterLink :to="'/admin/dashboard/venues/' + venue.id + '/modify'"
                            class="link-underline-opacity-0 link-dark fw-medium">
                            Modify</RouterLink>
                    </td>
                    <td class="btn btn-link fw-medium link-underline link-underline-opacity-0" type="button"
                        @click="deleteVenue(venue.name, venue.id)">
                        Delete</td>
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
        venueList: {
            get() {
                return this.$store.state.Venues.venueList
            },
            set(venueList) {
                this.$store.commit("Venues/updateVenueList", venueList)
            }
        },
    },

    created() {
        fetch('http://127.0.0.1:5000/admin/dashboard/venues/', {
            method: 'GET',
            headers: {
                'Authentication-Token': this.token,
            },
            mode: 'cors'
        })
        .then(response => response.json())
        .then(data => {
            if(data != []) {
                this.venueList = data
            }
        })
    },

    methods: {
        deleteVenue(name, id) {
            const result = confirm('Are you sure you want to delete Venue - ' + name + '?')
            if (result) {
                this.delete(id)
            }
        },

        async delete(id) {
            const response = await fetch('http://127.0.0.1:5000/admin/dashboard/venues/' + id + '/delete', {
                method: 'GET',
                headers: {
                    'Authentication-Token': this.token
                },
                mode: 'cors'
            })
            if (response.ok) {
                fetch('http://127.0.0.1:5000/admin/dashboard/venues/', {
                    method: 'GET',
                    headers: {
                        'Authentication-Token': this.token
                    },
                    mode: 'cors'
                })
                .then(response => response.json())
                .then(data => {
                    if(data != []) {
                        this.venueList = data
                    }
                })
            }
        },
    },
}

</script>