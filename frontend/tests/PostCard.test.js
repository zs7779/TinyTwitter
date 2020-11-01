import { shallowMount } from '@vue/test-utils'
import PostCard from '../src/components/PostCard'
import PostBody from '../src/components/PostBody'
import mockData from './mock_data'


jest.mock('../src/components/utils', ()=>{
    return {
        getToken: () => null // null cause axios not called
    }
})



const factory = (post={}, verbose=false) => {
    return shallowMount(PostCard, {
        propsData: {
            post: {
                ...mockData.posts[0],
                ...post,
            },
            verbose
        },
    });
}


describe('PostCard render', () => {
    let wrapper;
    afterEach(() => {
        wrapper.destroy();
    });
    it('Render default', () => {
        wrapper = factory();
        expect(wrapper.html()).toMatchSnapshot();
    });
    it('Render verbose', () => {
        wrapper = factory({}, false);
        expect(wrapper.html()).toMatchSnapshot();
    });
    it('Render repost', () => {
        wrapper = factory({parent: mockData.posts[1]}, false);
        expect(wrapper.html()).toMatchSnapshot();
    });
})

describe('PostCard Events', () => {
    let wrapper;
    beforeEach(() => {
        wrapper = wrapper = factory({});
    });
    afterEach(() => {
        wrapper.destroy();
    });
    it('Action comment', () => {
        wrapper.findComponent(PostBody).vm.$emit('action-comment');
        expect(wrapper.emitted('action-post').length).toBe(1);
    });
    it('Action repost', () => {
        wrapper.findComponent(PostBody).vm.$emit('action-repost');
        expect(wrapper.emitted('action-post').length).toBe(1);
    });
    it('Action edit', () => {
        wrapper.findComponent(PostBody).vm.$emit('action-edit');
        expect(wrapper.emitted('action-post').length).toBe(1);
    });
    it('Action like', () => {
        const spy = jest.spyOn(wrapper.vm, 'onLike')
        wrapper.findComponent(PostBody).vm.$emit('action-like');
        expect(spy).toHaveBeenCalled();
    });
    it('Action delete', () => {
        const spy = jest.spyOn(wrapper.vm, 'onDelete')
        wrapper.findComponent(PostBody).vm.$emit('action-delete');
        expect(spy).toHaveBeenCalled();
    });
})