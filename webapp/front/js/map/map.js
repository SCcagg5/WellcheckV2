Vue.component('compModDevices', compModDevices);
Vue.component('compModShare', compModShare);
Vue.component('compModAdd_a_device', compModAdd_a_device);


let vm = new Vue({
    el: '#map',

    data: {
      email: localStorage.email,
    },

    components: {msg, leftnav, mod},

    methods:{
      infos: function() {
        let data = {}
        data['headers'] = cred.methods.get_headers()
        data['data'] = {}
        user.methods.send('points/infos', data, this.store);
      },

      store: function(data) {
        if (data != '') {
          localStorage.points = JSON.stringify(data['points']);
        }
      }
   },
   mounted(){
     cred.methods.api_cred()
     cred.methods.usr_cred()
     this.infos();
   }
})
