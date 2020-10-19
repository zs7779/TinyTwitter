<template>
    <div class="card p-3 mb-2">
        <h5 class="card-title">{{ user.username }}</h5>
        <div class="row justify-content-between mx-1">
            <div>
                <span class="small text-muted">@{{ user.id }}</span>
            </div>
            <div v-if="user.owner===false">
                <button type="button" v-if="user.following" class="btn btn-primary rounded-pill" @click="onFollow">Following</button>
                <button type="button" v-else class="btn btn-outline-primary rounded-pill" @click="onFollow">Follow</button>
            </div>
        </div>

        <div class="card-footer bg-transparent p-0">
            <p class="mx-1">{{ user.bio }}</p>
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
        default(){return PLACEHOLDERs.user;},
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
</style>