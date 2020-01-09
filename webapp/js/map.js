let vm = new Vue({
    el: '#map',

    data: {
      email: localStorage.email,
    },

    components: {apimsg, leftnav, mod},

    methods:{
   },
   mounted(){
        cred.methods.api_cred()
        cred.methods.usr_cred()
   }
})
