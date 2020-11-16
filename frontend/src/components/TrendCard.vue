<template>
    <div class="p-3 trend-card">
        <div v-if='trend.username' class="d-flex justify-content-between align-items-center">
            <router-link :to="routerPath" tag='div'>
                <img :src='trend.avatar' class="avatar">
                <span class="text-dark font-weight-bold">{{ trend.username }}</span>
            </router-link>
            <button v-if='trend.following' type="button" class="btn btn-primary rounded-pill my-2" @click='doFollow'>Following</button>
            <button v-else type="button" class="btn btn-outline-primary rounded-pill my-2" @click='doFollow'>Follow</button>
        </div>
        <div v-if='trend.author'>
            <router-link :to="routerPath" tag='div'>
                <img :src='trend.author.avatar' class='avatar avatar-small'> {{ trend.author.username }}
                <span class="d-block small text-muted">{{ trend.text }}</span>
            </router-link>
        </div>
        <div v-if='trend.num_posts'>
            <router-link :to="routerPath" tag='div'>
                <span class="d-block font-weight-bold text-muted">#{{ trend.text }}</span>
                <span class="d-block small text-muted">{{ trend.num_posts }} Posts</span>
            </router-link>
        </div>
    </div>
</template>

<script>
import { URLS, getToken } from './utils'

export default{
    name: "trend-card",
    props: ['trend'],
    computed: {
        routerPath() {
            if (this.trend.username) return {
                name: 'user', params: {username: this.trend.username}
            };
            if (this.trend.author) return {
                name: "post", params: {username: this.trend.author.username, postID: this.trend.id}
            };
            if (this.trend.num_posts) return `/hashtags/${this.trend.text}`;
        },
    },
    methods: {
        doFollow() {
            const token = getToken(this.$root.userAuth);
            if (!token) return;
            axios.post(`${URLS.users(this.trend.username)}`, {
                follow: !this.trend.following,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                const user = {
                    ...this.trend,
                    follower_count: this.trend.following ? this.trend.follower_count - 1 : this.trend.follower_count + 1,
                    following: !this.trend.following,
                }
                this.$emit('user-ok', user);
            });
        },
    },
}
</script>

<style scoped>
.trend-card:hover {
    background-color: rgb(237, 245, 253);
}
.avatar {
    width: 2.5em;
    height: 2.5em;
    border-radius: 50%;
}
.avatar-small {
    width: 1em;
    height: 1em;
}
a {
    text-decoration: none;
}
button {
    font-size: 0.7em;
}
</style>