<template>
    <div class="card p-3 mb-1 px-1 profile-card">
        <img :src='user.avatar' class='avatar'>
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h5 class="card-title my-0">{{ user.username }}</h5>
                <span class="small text-muted">@{{ user.id }}</span>
            </div>
            <div v-if="user.owner">
                <button v-if='!editing' type="button" class="btn btn-outline-primary rounded-pill" @click='doEdit(false)'>
                    Edit
                </button>
            </div>
            <div v-else>
                <button type="button" v-if="user.following" class="btn btn-primary rounded-pill" @click="doFollow">Following</button>
                <button type="button" v-else class="btn btn-outline-primary rounded-pill" @click="doFollow">Follow</button>
            </div>
        </div>
        <div v-if='editing'>
            <textarea rows=4 class="form-control" v-model="editBio"></textarea>
            <span class="mx-1">{{ charRemaining }}</span>
            <button class="btn btn-secondary btn-sm rounded-pill py-1 m-1" @click="doEdit(false)">
                Cancel
            </button>
            <button class="btn btn-primary btn-sm rounded-pill py-1 m-1" @click="doEdit(true)" :disabled="!bioIsValid">
                Post
            </button>
        </div>
        <p v-else>{{ user.bio }}</p>
        <div class="card-footer bg-transparent p-0">
            <span class="mx-1"><span class="font-weight-bold">{{user.following_count}}</span> Following</span>
            <span class="mx-1"><span class="font-weight-bold">{{user.follower_count}}</span> Followers</span>
        </div>
    </div>
</template>

<script>
import { URLs, PLACEHOLDERs, getToken } from './utils'

export default{
    name: "user-profile",
    props: {user: {
        type: Object,
        default(){ return PLACEHOLDERs.user(); },
    }},
    data() {
        return {
            editing: false,
            editBio: "",
        }
    },
    methods: {
        doFollow() {
            const token = getToken(this.$root.userAuth);
            if (!token) return;
            axios.post(`${URLs.users(this.user.username)}`, {
                follow: !this.user.following,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                const user = {
                    ...this.user,
                    follower_count: this.user.following ? this.user.follower_count - 1 : this.user.follower_count + 1,
                    following: !this.user.following,
                }
                this.$emit('user-ok', user);
            });
        },
        doEdit(doSubmit) {
            if (doSubmit) {
                const token = getToken(this.$root.userAuth);
                if (!token) return;
                axios.patch(`${URLs.users(this.user.username)}`, {
                    bio: this.editBio,
                }, {
                    headers: {
                        'X-CSRFTOKEN': token,
                    },
                }).then(response => {
                    const user = {
                        ...this.user,
                        bio: this.editBio,
                    }
                    this.$emit('user-ok', user);
                    this.editing = !this.editing;
                });
            } else {
                this.editing = !this.editing;
            }
        },
    },
    computed: {
        charRemaining() {
            this.editBio = this.editBio.substr(0, 1400);
            return `${this.editBio.length}/140`;
        },
        bioIsValid() {
            return this.editBio.length <= 140;
        },
    },
    watch: {
        user() {
            this.editBio = this.user.bio;
        },
    },
}
</script>

<style scoped>
.avatar {
    width: 5em;
    height: 5em;
    border-radius: 50%;
}
@media (max-width: 575.98px) {
    .profile-card{
        font-size: 0.8em;
    }
}
</style>