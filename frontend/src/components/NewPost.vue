<template>
    <div>
        <slot></slot>
        <b-modal id='new-post' title=''
            @ok.prevent="doSubmitPost"
            @show="checkToken"
            @hidden="doClear"
        >
            <textarea rows=4 class="form-control border-0" v-model="postText" placeholder="Say something..."></textarea>
            <input type="file" name="file" ref='fileUpload' @change="onFileUpload($event.target.files)" class="d-none" />
            <template v-slot:modal-footer="{ ok }">
                <div class="d-flex justify-content-between w-100">
                    <button type='button' title='Upload image' class="btn btn-transparent upload-button p-0" @click="$refs.fileUpload.click()">
                        <b-icon icon="image"></b-icon> {{ filename }}
                    </button>
                    <span v-if='errorMessage.length > 0' class="">{{ errorMessage }}</span>
                    <div>
                        <span class="mx-1">{{ charRemaining }}</span>
                        <b-button size="sm" variant="primary" @click="ok()" :disabled="!postIsValid" class="rounded-pill py-0">
                            Post
                        </b-button>
                    </div>
                </div>
            </template>
        </b-modal>
    </div>
</template>

<script>
import { URLS, getToken, printError } from './utils'

export default{
    name: "new-post",
    props: ['postParams'],
    data() {
        return {
            postText: '',
            postMedia: null,
            fileList: [],
            errorMessage: '',
            token: null,
        };
    },
    computed: {
        filename() {
            if (this.fileList.length === 0) return "";
            return this.fileList[0].name;
        },
        charRemaining() {
            this.postText = this.postText.substr(0, 700);
            return `${this.postText.length}/140`;
        },
        postIsValid() {
            return (this.postText.length > 0) && (this.postText.length <= 140);
        },
        postMethod() {
            if (this.postParams.oldPost) return axios.patch;
            return axios.post;
        },
        postURL() {
            if (this.postParams.oldPost) return `${URLS.usersPosts(this.postParams.oldPost.author.username, this.postParams.oldPost.id)}`;
            if (this.postParams.isComment) return `${URLS.usersPosts(this.postParams.rootPost.author.username, this.postParams.rootPost.id)}`;
            return `${URLS.posts()}`;
        },
    },
    methods: {
        onFileUpload(fileList) {
            if (!fileList[0].type.startsWith('image/')) {
                return;
            }
            if (fileList[0].size > 5242880) {
                return;
            }
            this.fileList = fileList;
        },
        sendFile() {
            if (this.fileList.length == 0) return;

            axios.get(URLS.upload(), {
                params: {
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
                        this.postMedia = s3.url + s3.fields.key;
                        // this.postMedia = s3.url.replace('compress', 'bucket') + s3.fields.key;
                        this.sendText();
                    });
                });
        },
        sendText() {
            this.postMethod(this.postURL, {
                text: this.postText,
                media: this.postMedia,
                parent_id: this.postParams.parentPost ? this.postParams.parentPost.id : null,
            }, {
                headers: {
                    'X-CSRFTOKEN': this.token,
                },
            }).then(response => {
                if (this.postParams.isComment) {
                    this.$emit('comment-ok', response.data.comment);
                } else if (this.postParams.oldPost) {
                    this.$emit('edit-ok', {
                        ...this.postParams.oldPost,
                        text: this.postText,
                    });
                }
                else this.$emit('post-ok', response.data.post);
                this.$bvModal.hide('new-post');
            })
        },
        doSubmitPost() {
            if (this.postText.length == 0 || this.postText.length >= 140) return;

            if (this.fileList.length > 0) {
                this.sendFile();
            } else {
                this.sendText();
            }
        },
        doClear() {
            this.$emit('action-clear');
            this.postText = "";
            this.postMedia = null;
            this.fileList = [];
            this.token = null;
        },
        checkToken(event) {
            if (!this.token) {
                this.token = getToken(this.$root.userAuth);
            }
        },
    },
    watch: {
        postParams() {
            if (this.postParams.oldPost) this.postText = this.postParams.oldPost.text;
        }
    },
    created() {
        if (this.postParams.oldPost) this.postText = this.postParams.oldPost.text;
    }
}
</script>

<style scoped>
.upload-button:hover {
    color: #00a2ff;
}
</style>