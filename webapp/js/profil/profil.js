
let vm = new Vue({
    el: '#profil',

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
