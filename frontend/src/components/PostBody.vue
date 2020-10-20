<template>
    <div>
        <router-link :to='{name: "post", params: {username: post.author.username, postID: post.id}}' tag='div' class="card-text card-view">
            <h6 class="card-title mb-1">
                <router-link :to="{ name: 'user', params: {username: post.author.username} }">{{ post.author.username }}</router-link>
                <span class="small text-muted">at {{ post.create_time }} said:</span>
            </h6>
            <p>{{ post.text }}</p>
            <slot></slot>
        </router-link>
    </div>
</template>

<script>
export default{
    props: ['post'],
}
</script>

<style scoped>
</style>