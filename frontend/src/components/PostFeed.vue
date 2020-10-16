<template>
    <div class="post-feed">
        <slot></slot>
        <transition-group name="list">
            <post-card
                v-for="post in posts"
                :key="post.id" :post="post"
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