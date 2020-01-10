let msg = {
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
      this.redirect()
      return callback(data.data);
    },
    redirect: function(succes = true) {
      this.type = succes ? "succes" : "error"
      this.msg = "redirecting ..."
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
