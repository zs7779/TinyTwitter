<template>
    <div class="post-feed">
        <slot></slot>
        <transition-group name="list">
            <post-card
                v-for="post in posts"
                v-bind:key="post.id" v-bind:post="post"
                v-on="$listeners">
            </post-card>
        </transition-group>
    </div>
</template>

<script>
import PostCard from './PostCard.vue'

export default{
    name: "post-feed",
    props: {
        posts: Array,
    },
    components: {
        PostCard,
    },
}
</script>

<style scoped>
</style>