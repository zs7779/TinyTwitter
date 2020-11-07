<template>
    <div class="card p-3 mb-1 px-1 profile-card">
        <img :src='user.avatar' class='avatar'>
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h5 class="card-title my-0">{{ user.username }}</h5>
                <span class="small text-muted">@{{ user.id }}</span>
            </div>
            <div v-if="user.owner">
                <button type="button" class="btn btn-outline-primary rounded-pill" @click.prevent>
                    Edit
                </button>
            </div>
            <div v-else>
                <button type="button" v-if="user.following" class="btn btn-primary rounded-pill" @click="onFollow">Following</button>
                <button type="button" v-else class="btn btn-outline-primary rounded-pill" @click="onFollow">Follow</button>
            </div>
        </div>
        <p>{{ user.bio }}</p>
        <div class="card-footer bg-transparent p-0">
            <span class="mx-1"><span class="font-weight-bold">{{user.following_count}}</span> Following</span>
            <span class="mx-1"><span class="font-weight-bold">{{user.follower_count}}</span> Followers</span>
        </div>
    </div>
</template>

<script>
import { PLACEHOLDERs } from './utils'

export default{
    name: "user-profile",
    props: {user: {
        type: Object,
        default(){ return PLACEHOLDERs.user(); },
    }},
    methods: {
        onFollow() {
            // can be argued weither to emit user object
            this.$emit("action-follow");
        }
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