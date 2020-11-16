<template>
    <div>
        <profile-card :user="user" @user-ok="updateUser($event)"></profile-card>
    </div>
</template>

<script>
import ProfileCard from './ProfileCard.vue'
import { URLS, PLACEHOLDERS, getToken } from './utils'

export default{
    name: "profile-view",
    props: ['username'],
    data() {
        return {
            user: PLACEHOLDERS.user(),
        }
    },
    methods: {
        getUserProfile() {
            const path_now = this.username;
            axios.get(`${URLS.users(this.username)}`).then(response => {
                if (path_now === this.username) {
                    this.user = response.data.user;
                }
            })
        },
        updateUser(editedUser) {
            if (editedUser.id === this.user.id)
                this.user = editedUser;
        },
    },
    watch: {
        $route() {
            this.getUserProfile();
        },
    },
    created() {
        this.getUserProfile();
    },
    components: {
        ProfileCard,
    },
}
</script>

<style scoped>
</style>