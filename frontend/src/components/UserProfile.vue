<template>
    <div class="card p-3 mb-1 px-1 profile-card">
        <div class="position-relative">
            <img :src='avatar' :class="[editing ? 'editing' : '', 'avatar']">
            <div v-if='editing' class='edit-upload'>
                <input type="file" name="file" ref='fileUpload' @change="onFileUpload($event.target.files)" class="d-none" />
                <button type='button' title='Upload image' class="btn btn-transparent px-1 py-0 upload-button" @click="$refs.fileUpload.click()">
                    <b-icon icon="image"></b-icon> {{filename}}
                </button>
            </div>
        </div>
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h5 class="card-title my-0">{{ user.username }}</h5>
                <span class="small text-muted">@{{ user.username }}</span>
            </div>
            <div v-if="user.owner">
                <button v-if='!editing' type="button" class="btn btn-outline-primary rounded-pill" @click='doEdit(false)'>
                    Edit
                </button>
            </div>
            <div v-else>
                <button type="button" v-if="user.following" class="btn btn-primary rounded-pill" @click="doFollow">Following</button>
                <button type="button" v-else class="btn btn-outline-primary rounded-pill" @click="doFollow">Follow</button>
            </div>
        </div>
        <div v-if='editing'>
            <textarea rows=4 class="form-control" v-model="editBio"></textarea>
            <span class="mx-1">{{ charRemaining }}</span>
            <button class="btn btn-secondary btn-sm rounded-pill py-1 m-1" @click="doEdit(false)">
                Cancel
            </button>
            <button class="btn btn-primary btn-sm rounded-pill py-1 m-1" @click="doEdit(true)" :disabled="!bioIsValid">
                Save
            </button>
        </div>
        <p v-else>{{ user.bio }}</p>
        <div class="card-footer bg-transparent p-0">
            <span class="mx-1"><span class="font-weight-bold">{{user.following_count}}</span> Following</span>
            <span class="mx-1"><span class="font-weight-bold">{{user.follower_count}}</span> Followers</span>
        </div>
    </div>
</template>

<script>
import { URLS, PLACEHOLDERS, getToken } from './utils'

export default{
    name: "user-profile",
    props: {user: {
        type: Object,
        default(){ return PLACEHOLDERS.user(); },
    }},
    data() {
        return {
            avatar: "",
            editing: false,
            editBio: "",
            fileList: [],
        }
    },
    computed: {
        filename() {
            if (this.fileList.length === 0) return "";
            return this.fileList[0].name;
        },
        charRemaining() {
            this.editBio = this.editBio.substr(0, 1400);
            return `${this.editBio.length}/140`;
        },
        bioIsValid() {
            return this.editBio.length <= 140;
        },
    },
    methods: {
        doFollow() {
            const token = getToken(this.$root.userAuth);
            if (!token) return;
            axios.post(`${URLS.users(this.user.username)}`, {
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
                this.$emit('user-ok', user);
            });
        },
        onFileUpload(fileList) {
            if (!fileList[0].type.startsWith('image/')) {
                return;
            }
            if (fileList[0].size > 2097152) {
                return;
            }
            this.fileList = fileList;
        },
        sendAvatar() {
            axios.get(URLS.upload(), {
                params: {
                    avatar: true,
                    type: `.${this.fileList[0].name.split('.').pop()}`,
                }
            })
                .then(response => response.data)
                .then(s3 => {
                    let formData = new FormData();
                    formData.append('key', s3.fields.key);
                    formData.append('AWSAccessKeyId', s3.fields.AWSAccessKeyId);
                    formData.append('policy', s3.fields.policy);
                    formData.append('signature', s3.fields.signature);
                    formData.append('Content-Type', this.fileList[0].type);
                    formData.append('file', this.fileList[0], this.fileList[0].name);
                    
                    axios.post(s3.url, formData, {
                        headers: {
                            'content-type': "multipart/form-data",
                        }
                    }).then(response => {
                        this.avatar = s3.url + s3.fields.key;
                        // this.avatar = s3.url.replace('compress', 'bucket') + s3.fields.key;
                        this.sendText();
                    });
                });
        },
        sendText() {
            const token = getToken(this.$root.userAuth);
            if (!token) return;
            axios.patch(`${URLS.users(this.user.username)}`, {
                avatar: this.avatar,
                bio: this.editBio,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                const user = {
                    ...this.user,
                    avatar: this.avatar,
                    bio: this.editBio,
                }
                this.$emit('user-ok', user);
            });
        },
        doEdit(doSubmit) {
            if (doSubmit) {
                if (this.fileList.length > 0) {
                    this.sendAvatar();
                } else {
                    this.sendText();
                }
            } else {
                this.avatar = this.user.avatar;
            }
            this.editing = !this.editing;
            this.fileList = [];
        },
    },
    watch: {
        user() {
            this.avatar = this.user.avatar;
            this.editBio = this.user.bio;
        },
    },
}
</script>

<style scoped>
.avatar {
    width: 5em;
    height: 5em;
    border-radius: 50%;
}
.avatar.editing {
    border: 3px solid #9adaff;
    padding: 3px;
}
.edit-upload {
    position: absolute;
    top:3.5em;
    left:3.5em;
    border: 3px solid #9adaff;
    border-radius: 10px;
    background-color: white;
}
.upload-button:hover {
    color: #00a2ff;
}
textarea {
    border-color: #9adaff;
}
@media (max-width: 575.98px) {
    .profile-card{
        font-size: 0.8em;
    }
}
</style>