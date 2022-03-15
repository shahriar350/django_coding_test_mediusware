window.$ = window.jQuery = require('jquery');
import 'startbootstrap-sb-admin-2/js/sb-admin-2'
import Vue from 'vue';
import axios from 'axios'
import '../scss/main.scss'

window.Vue = Vue
Vue.use(require('vue-moment'));
Vue.component('create-product', require('./components/product/CreateProduct.vue').default)
Vue.component('list-product', require('./components/product/ListProduct.vue').default)
Vue.component('edit-product', require('./components/product/editProduct.vue').default)
Vue.prototype.$http = axios;
const main = new Vue({
    el: '#app'
})