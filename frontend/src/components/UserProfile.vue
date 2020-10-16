<template>
    <div class="card p-3 mb-2">
        <h5 class="card-title">{{ user.username }}</h5>
        <div class="row justify-content-between mx-1">
            <div>
                <span class="small text-muted">@{{ user.id }}</span>
            </div>
            <div v-if="user.owner===false">
                <button type="button" v-if="user.following" class="btn btn-primary rounded-pill" v-on:click="onFollow">Following</button>
                <button type="button" v-else class="btn btn-outline-primary rounded-pill" v-on:click="onFollow">Follow</button>
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
import { URLs, getToken } from './utils'

export default{
    name: "user-profile",
    props: ["user"],
    methods: {
        onFollow: function() {
            const token = getToken();
            if (!token) return;
            axios.post(`${URLs.users}${this.user.username}`, {
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
                this.$emit("user-ok", user);
            })
        }
    },
}
</script>

<style scoped>
</style>