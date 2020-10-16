<template>
    <div>
        <post-card :post="post" v-on="$listeners"></post-card>
    </div>
</template>

<script>
import PostCard from './PostCard.vue'

export default{
    name: "user-post-view",
    props: ['post'],
    components: {
        PostCard
    },
}
</script>

<style scoped>
</style>