
let cred = {
  methods: {
    usr_cred: function() {
      let actual = window.location.href.split(address)[1]
      if (localStorage.usr_token && this.checktime("usr_token")) {
        let location = localStorage.location ?  localStorage.location  : redirect
        let page = location.charAt(1).toUpperCase() + location.slice(2);
        if (actual != location) {
          localStorage.location = location;
          localStorage.page = page;
          window.location.href = location;
        }
      } else {
        if (actual != "/" && actual != "/index" && actual != "/login")
          window.location.href = "/login";
      }
    },

    api_cred: function() {
      if (localStorage.api_token && this.checktime("api_token"))
        return;
      this.ajaxRequest = true;
      data = {
         "pass" : "password"
       };
      url = method + "://" + api + "/login/"
      axios.post(url, data)
           .then(
             response => {
               if (response.data.status == 200)
               {
                 localStorage.api_token = response.data.data.token;
                 localStorage.api_token_exp = this.time(response.data.data.exp);
               }
             });
     },
     time: function(exp = null){
       if (exp == null)
          return Math.round(new Date().getTime()/1000);
       time = Math.round(new Date(exp).getTime()/1000);
       return (time)
     },
     checktime: function(str)  {
       if (localStorage[str+"_exp"] < this.time() - 500) {
          localStorage.removeItem(str);
          localStorage.removeItem(str + "_exp");
          return false;
       }
       return true;
     },
     get_headers: function() {
       res = {}
       this.api_cred();
       res["token"] = localStorage.api_token;
       if (localStorage.usr_token && this.checktime("usr_token"))
         res["usr_token"] = localStorage.usr_token;
       return res;
     }
   }
};

let apimsg = {
  data: function() {
    return {
      msg: null,
      type: "hide"
    }
  },
  methods: {
    check: function (data, callback){
      if (data.status != 200){
        this.type = "error"
        this.msg = data.error;
        return;
      }
      this.type = "succes"
      this.msg = "redirecting ..."
      return callback(data.data);
    },

    set: function (msg, type) {
      this.type = type
      this.msg = msg;
    },
    hide: function(){
      this.type = "hide";

    }
  },
  template: `<div class="txt-center">
                <div :class=type class="message"> {{ msg }}
                  <div class="cross" :class=type v-on:click=hide>x</div>
                </div>
            </div>`
}

let leftnav = {
  data: function() {
    return {
      type: 'open',
      email: localStorage.email,
      page: localStorage.page,
      open: true
    }
  },
  methods: {
    changeopen: function() {
      this.open = !this.open;
      this.type = this.open ? 'open' : 'close';
    },
    points: function() {
      var template = 'Points';
      this.opentemplate(template)
    },
    share: function() {
      var template = 'Share';
      this.opentemplate(template)
    },
    opentemplate: function(template) {
      var old = this.disableall();
      this.activate(template, old);
      vm.$refs.modal.changeopen(template);
    },
    activate: function(template, old) {
      if (template == old)
        return this.disableall;

      for (i in this.$refs) {
        elem = this.$refs[i];
        for (i2 in elem.classList)
          if (elem.classList[i2] == 'nav-second' && elem.innerHTML == template)
            elem.classList.add('nav-second-active');
      }
    },
    disableall: function() {
      for (i in this.$refs){
        elem = this.$refs[i];
        for (i2 in elem.classList)
          if (elem.classList[i2] == 'nav-second-active') {
            elem.classList.remove('nav-second-active');
            return elem.innerHTML;
          }
      }
      return null;
    }
  },
  mounted: function () {
    this.$nextTick(function () {
      let elem = null;
      let page = this.page.replace('-', ' ');
      let add = false;
      let cont = false;
      for (i in this.$refs){
        elem = this.$refs[i];
        if (add){
          for (i2 in elem.classList) {
            if (elem.classList[i2] == 'nav-second') {
              elem.classList.add('display');
              cont = true;
            }
          }
          if (cont == false) {
              add = false;
            }
        }
        if (elem.innerHTML == page){
          elem.classList.add('nav-active');
          add = true;
        }
      }
    })
  },
  template: `
            <div class="nav" :class=type>
                <img v-if="!open"  class="menu-close" v-on:click=changeopen src="imgs/menu.png">
                <img v-if="open" class="menu-open"  v-on:click=changeopen src="imgs/back.png">
                <div test class="overflow">
                  <img class="img-nav" src="imgs/logo_v2.png" alt="">
                  <p>{{ email }}</p>
                  <div class="sep"></div>
                  <div ref="link1" class="nav-text" >Mon profil</div>
                  <div ref="link2" class="nav-text">Map</div>
                  <div ref="link3" class="nav-text nav-second" v-on:click=points>Points</div>
                  <div ref="link5" class="nav-text nav-second" v-on:click=share>Share</div>
                  <div ref="link4" class="nav-text" v-on:click="user.methods.logout">Logout</div>
                  <div class="w3copyright-agile in-nav">
              			<p>Wellcheck© 2020.<br>All Rights Reserved.</p>
            		  </div>
                </div>
             </div>`
}

let mod = {
  data: function() {
    return {
      type: 'hide',
      open: false,
      name: null,
      element: {},
      comp: null
    }
  },
  components: {compPoints, compShare},
  methods: {
    changeopen: function(name) {
      if (name == this.name || this.name == null) {
        this.open = !this.open;
        this.change()
      }
      if (this.open)
        this.name = name;
        this.comp = 'comp' + name;

    },
    open: function() {
      this.open = true;
      this.change()
    },
    close: function() {
      this.open = false;
      this.change()
    },
    change: function() {
      if (this.open) {
        this.type = '';
        vm.$refs.main.classList.add('blur');
      }
      else {
        this.type = 'hide';
        this.name = null;
        vm.$refs.main.classList.remove('blur');
        vm.$refs.nav.disableall();
      }
    }
  },
  template: `
  <div class='back' :class='type' v-on:click=close>
    <div class='base'>
      <div class='title-base'>
        {{ this.name }}
      </div>
      <component v-bind:is=this.comp></component>
    </div>
  </div>
  `
  }



let user = {
  methods: {
    register: function(data) {
      this.ajaxRequest = true;
      url = method + "://" + api + "/signup/";
      localStorage.email = data.data["email"];
      axios.post(url, data.data, { headers: data.headers})
        .then(response => vm.$refs.extern.check(response.data, this.storecred))
        .catch(error => console.log(error));

    },

    login: function(data) {
      this.ajaxRequest = true;
      url = method + "://" + api + "/signin/";
      localStorage.email = data.data["email"];
      axios.post(url, data.data, { headers: data.headers})
        .then(response => vm.$refs.extern.check(response.data, this.storecred))
        .catch(error => console.log(error));
    },

    logout: function() {
      localStorage.removeItem("usr_token");
      localStorage.removeItem("usr_token_exp");
      cred.methods.usr_cred();
    },

    storecred: function(data) {
      localStorage.usr_token = data.token;
      localStorage.usr_token_exp = cred.methods.time(data.exp);
      let location = localStorage.location ?  localStorage.location  : redirect
      let page = location.charAt(1).toUpperCase() + location.slice(2);
      localStorage.location = location;
      localStorage.page = page;
      window.location.href = location;
    }
  }
}
