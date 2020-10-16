<template>
    <div>
        <post-feed :posts="posts" v-on="$listeners"></post-feed>
    </div>
</template>

<script>
import PostFeed from './PostFeed.vue'

export default{
    name: "user-profile-view",
    props: ['posts'],
    components: {
        PostFeed
    },
}
</script>

<style scoped>
</style>