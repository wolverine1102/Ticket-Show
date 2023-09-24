<template>
    <div>
        <div class="fs-2 fw-semibold mt-2" align="center">Add New Show</div>
        <div class="container-md border border-dark ms-10 mt-3 mb-3">
            <form @submit.prevent="submitForm">
                <div class="row mt-3 ms-4">
                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Show ID </label>
                        <div class="col-sm-10">
                            <input v-model="id" type="text" name="id" class="form-control w-50"
                                :class="{ 'is-invalid': showExists }" required />
                            <div v-show="showExists" class="invalid-feedback">This show id is already exists.</div>
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Name </label>
                        <div class="col-sm-10">
                            <input v-model="name" type="text" name="name" class="form-control w-50" required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Rating </label>
                        <div class="col-sm-10">
                            <input v-model="rating" type="text" name="rating" class="form-control w-50" />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Category </label>
                        <div class="col-sm-10">
                            <input v-model="category" type="text" name="category" class="form-control w-50" required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Tags </label>
                        <div class="col-sm-10">
                            <input v-model="tags" type="text" name="tags" class="form-control w-50" required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Languages </label>
                        <div class="col-sm-10">
                            <input v-model="languages" type="text" name="languages" class="form-control w-50" required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Duration </label>
                        <div class="col-sm-10">
                            <input v-model="duration" type="text" name="duration" class="form-control w-50" />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Release Date </label>
                        <div class="col-sm-10">
                            <input v-model="releaseDate" type="date" name="release_date" class="form-control w-50"
                                required />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label class="col-form-label"> Photo Link </label>
                        <div class="col-sm-10">
                            <input v-model="photo" type="url" name="photo" class="form-control w-50" />
                        </div>
                    </div>

                    <div class="row ms-3 mb-1">
                        <label for="description" class="col-form-label"> Description </label>
                        <div class="col-sm-10" style="height: 100px">
                            <textarea v-model="description" class="form-control" id="description" name="description"
                                style="height: 100px" required></textarea>
                        </div>
                    </div>

                    <div class="row m-3">
                        <div class="col-sm-10">
                            <button class="btn btn-dark" type="submit">Add Show and Next</button>
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
            showExists: false
        }
    },

    computed:{
        ...mapState({
            token: state => state.CurrentUser.token
        }),
        id: {
            get() {
                return this.$store.state.Shows.id
            },
            set(id) {
                this.$store.commit("Shows/updateId", id)
            }
        },
        name: {
            get() {
                return this.$store.state.Shows.name
            },
            set(name) {
                this.$store.commit("Shows/updateName", name)
            }
        },
        rating: {
            get() {
                return this.$store.state.Shows.rating
            },
            set(rating) {
                this.$store.commit("Shows/updateRating", rating)
            }
        },
        category: {
            get() {
                return this.$store.state.Shows.category
            },
            set(category) {
                this.$store.commit("Shows/updateCategory", category)
            }
        },
        tags: {
            get() {
                return this.$store.state.Shows.tags
            },
            set(tags) {
                this.$store.commit("Shows/updateTags", tags)
            }
        },
        languages: {
            get() {
                return this.$store.state.Shows.languages
            },
            set(languages) {
                this.$store.commit("Shows/updateLanguages", languages)
            }
        },
        duration: {
            get() {
                return this.$store.state.Shows.duration
            },
            set(duration) {
                this.$store.commit("Shows/updateDuration", duration)
            }
        },
        releaseDate: {
            get() {
                return this.$store.state.Shows.releaseDate
            },
            set(releaseDate) {
                this.$store.commit("Shows/updateReleaseDate", releaseDate)
            }
        },
        description: {
            get() {
                return this.$store.state.Shows.description
            },
            set(description) {
                this.$store.commit("Shows/updateDescription", description)
            }
        },
        photo: {
            get() {
                return this.$store.state.Shows.photo
            },
            set(photo) {
                this.$store.commit("Shows/updatePhoto", photo)
            }
        },
    },

    created() {
        this.id = null
        this.name = null
        this.rating = null
        this.category = null
        this.tags = null
        this.languages = null
        this.duration = null
        this.releaseDate = null
        this.description = null
        this.photo = null
    },

    methods: {
        async submitForm() {
            const response = await fetch('http://127.0.0.1:5000/admin/dashboard/shows/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
                body: JSON.stringify({
                    "id": this.id,
                    "name": this.name,
                    "rating": this.rating,
                    "category": this.category,
                    "tags": this.tags,
                    "languages": this.languages,
                    "duration": this.duration,
                    "release_date": this.releaseDate,
                    "description" : this.description,
                    "photo": this.photo
                }),
                mode: 'cors'
            })
            if (response.ok) {
                this.$router.push('/admin/dashboard/shows/' + this.id + '/add_venue')
            }
            else {
                this.showExists = true
            }
        }
    }
}

</script>