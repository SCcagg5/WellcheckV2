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
      let location = localStorage.location ?  localStorage.location  : redirect;
      loc.methods.redirect(location);
    }
  }
}
