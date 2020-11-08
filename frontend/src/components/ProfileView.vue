<template>
    <div>
        <user-profile :user="user" @user-ok="updateUser($event)"></user-profile>
    </div>
</template>

<script>
import UserProfile from './UserProfile.vue'
import { URLs, PLACEHOLDERs, getToken } from './utils'

export default{
    name: "profile-view",
    props: ['username'],
    data() {
        return {
            user: PLACEHOLDERs.user(),
        }
    },
    methods: {
        getUserProfile() {
            axios.get(`${URLs.users(this.username)}`).then(response => {
                this.user = response.data.user;
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