Vue.component('compPoints', compPoints);
Vue.component('compShare', compShare);

let vm = new Vue({
    el: '#map',

    data: {
      email: localStorage.email,
    },

    components: {msg, leftnav, mod},

    methods:{
   },
   mounted(){
        cred.methods.api_cred()
        cred.methods.usr_cred()
   }
})
