<template>
    <div>
        <user-profile :user="user" @action-follow="doFollow()"></user-profile>
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
        doFollow() {
            const token = getToken(this.$root.userAuth);
            if (!token) return;
            axios.post(`${URLs.users(this.user.username)}`, {
                follow: !this.user.following,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                const user = {
                    ...this.user,
                    follower_count: this.user.following ? this.user.follower_count - 1 : this.user.follower_count + 1,
                    following: !this.user.following,
                }
                this.updateUser(user);
            })
        },
    },
    watch: {
        username() {
            if (this.username !== this.user.username)
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