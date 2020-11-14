<template>
    <div>
        <user-profile :user="user" @user-ok="updateUser($event)"></user-profile>
    </div>
</template>

<script>
import UserProfile from './UserProfile.vue'
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
        UserProfile,
    },
}
</script>

<style scoped>
</style>