function aUser(user={}) {
    const base_user = {
        id: 1,
        username: 'user1'
    };
    return {...base_user, ...user};
};

function aPost(post) {
    const base_post = {
        author: aUser(),
        id: 1,
        text: "post text",
        create_time: null,
        comment_count: 0,
        repost_count: 0,
        like_count: 0,
        commented: 0,
        reposted: 0,
        liked: 0,
        comments: [],
        parent: null,
        root: null,
        is_comment: false,
    };
    return {...base_post, ...post};
};

const users = [
    aUser({id:0, username:'user0'}),
    aUser({id:1, username:'user1'}),
    aUser({id:2, username:'user2'})
];

const posts = [
    aPost({author:users[0], id:0, text:"post0"}),
    aPost({author:users[0], id:1, text:"post1"}),
    aPost({author:users[1], id:2, text:"post2"}),
    aPost({author:users[1], id:3, text:"post3"}),
    aPost({author:users[2], id:4, text:"post4"}),
    aPost({author:users[2], id:5, text:"post5"})
];

const comments = [
    aPost({author:users[0], id:10, text:"comment0", is_comment:true}),
    aPost({author:users[0], id:11, text:"comment1", is_comment:true}),
    aPost({author:users[1], id:12, text:"comment2", is_comment:true}),
    aPost({author:users[1], id:13, text:"comment3", is_comment:true}),
    aPost({author:users[2], id:14, text:"comment4", is_comment:true}),
    aPost({author:users[2], id:15, text:"comment5", is_comment:true})
];

export default {
    users,
    posts,
    comments
};