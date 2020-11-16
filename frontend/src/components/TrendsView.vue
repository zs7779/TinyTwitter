<template>
    <div>
        <transition-group name="fade">
            <div v-if='users.length > 0' key="trendusers" class="card m-3 trend-panel">
                <h5 class="px-3 py-2 m-0">You might like</h5>
                <trend-card
                    v-for="user in users"
                    :key="'u-'+user.id" :trend="user"
                    v-on="$listeners">
                </trend-card>
            </div>
            <div v-if='posts.length > 0 || hashtags.length > 0' key="trendothers"
                class="card m-3 trend-panel"
            >
                <h5 class="px-3 py-2 m-0">What's happening</h5>
                <trend-card
                    v-for="hashtag in hashtags"
                    :key="'h-'+hashtag.id" :trend="hashtag"
                    v-on="$listeners">
                </trend-card>
                <trend-card
                    v-for="post in posts"
                    :key="'p-'+post.id" :trend="post"
                    v-on="$listeners">
                </trend-card>
            </div>
        </transition-group>
    </div>
</template>

<script>
import TrendCard from './TrendCard.vue'
import { URLS, PLACEHOLDERS } from './utils'

export default{
    name: "trends-view",
    props: ['users', 'posts', 'hashtags'],
    components: {
        TrendCard,
    },
}
</script>

<style scoped>
.card {
    background-color: rgb(246, 250, 255);
    border: none;
}
.trend-panel {
    border-radius: 20px;
}
.trend-panel div {
    border-top: 1px solid rgb(236, 236, 236);
}
</style>