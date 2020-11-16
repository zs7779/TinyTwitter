const URLS = {
    posts: (postID='') => `/api/posts/${postID}`,
    users: (userID='') => `/api/users/${userID}`,
    usersPosts: (userID='', postID='') => `/api/users/${userID}/posts/${postID}`,
    hashtags: (hashtag='') => `/api/hashtags/${hashtag}`,
    currentUser: (path='') => `/api/current_user/${path}`,
    upload: () => '/api/upload',
};


const CONSTS = {
    fileSizeLimit: 5242880,
};


const PLACEHOLDERS = {
    user: () => { return {id: -1, username: 'username'}; },
    post: () => {
        return {
            id: -1,
            author: {id: -1, username: 'username'},
            text: "",
            medias: [],
            parent: null,
            create_time: null,
            is_comment: false,
            root_post: null,
            comment_count: null,
            repost_count: null,
            like_count: null,
            commented: 0,
            reposted: 0,
            liked: 0,
            owner: false,
            comments: [],
        };
    },
    posts: () => [],
    postParams: () => {
        return {
            oldPost: null,
            parentPost: null,
            isComment: false,
            rootPost: null,
        };
    },
}


function printError(error) {
    if (error.response) {
      console.log(error.response.data);
      console.log(error.response.status);
      console.log(error.response.headers);
    } else if (error.request) {
      console.log(error.request);
    } else {
      console.log('Error', error.message);
    }
}


function getToken(userAuth) {
    const csrftoken = Cookies.get('csrftoken');
    if (userAuth && csrftoken) {
        return csrftoken;
    }
    window.location.href = "/login/";
    return false;
}


export {
    URLS,
    CONSTS,
    PLACEHOLDERS,
    printError,
    getToken,
}