Vue.component('compModPoints', compModPoints);
Vue.component('compModShare', compModShare);

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
