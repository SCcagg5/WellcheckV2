let compModDevices = {
  data: function() {
    return {
      points: [],
      limit: 0
    }
  },

  filters:{
    tostr: function(timestamp) {
      let date = new Date(parseInt(timestamp));
      let day = ("00" + date.getDate())
      day = day.substr(day.length - 2);
      let month = ("0" + (date.getMonth() + 1))
      month = month.substr(day.length - 2);
      let str = day + '.' + month + '.' + date.getFullYear();
      return str;
    }
  },

  methods:{
    addPoint: function () {
      vm.$refs.nav.modale('Add_a_device');
      let data = {}
      data['note'] = "Add your Wellcheck device";
      vm.$refs.modal.loaddata(data);
    }
  },
  template: `
  <div>
  <form class="insidecomp">
    <div class="container">
      <div class="row">
        <div class="col-md-12 col-sm-12">
          <div class="container">
            <div class="row">
            <div v-if="points.proprietary.length > 0" class="col-12">
              <div class="col-sm-12 col-12 margin5px" for="input2">{{ points.proprietary.length > 1 ? "Your devices (" + points.proprietary.length + ")" : "Your device" }}</div>
              </br>
              <div class="col-md-1 hidesms"></div>
              <ul class='list-group col-12 sm-modalelist' style="overflow-x: hidden">
                  <li v-for="point in points.proprietary" class="list-group-item list-group-item-action">
                    <div class="row">
                      <div class="ml-0 mr-0" style="width: 40px; height: auto; color: grey"> {{point.id}} </div>
                      <div class="ml-0 mr-0"style="text-align: left"> {{ point.surname }} </div>
                      <div class="ml-auto mr-0 datelist"> Added {{ point.date | tostr }} </div>

                      <div v-if="point.data.length > 0 && point.data[0].date > limit " class="ml-3 mr-3" style="text-align: right"> Online &#10004; </div>
                      <div v-if="point.data.length == 0 || point.data[0].date < limit" class="ml-3 mr-3 errorbtn" style="text-align: right"> Offline &#10006; </div>
                    </div>
                  </li>
                </ul>
                </br>
              </div>
              <div v-if="points.shared.length > 0" class="col-12">
                <div class="col-sm-12 col-12 margin5px" for="input2">{{ points.shared.length > 1 ? "Shared with you (" + points.shared.length + ")" : "Shared with you" }}</div>
                </br>
                <div class="col-md-1 hidesms"></div>
                <ul class='list-group col-12 sm-modalelist' style="overflow-x: hidden">
                    <li v-for="point in points.shared" class="list-group-item list-group-item-action">
                      <div class="row">
                        <div class="ml-0 mr-0" style="width: 40px; height: auto; color: grey"> {{point.id}} </div>
                        <div class="ml-0 mr-0"style="text-align: left"> {{ point.surname }} </div>
                        <div class="ml-auto mr-0 datelist"> Shared {{ point.date | tostr }} </div>

                        <div v-if="point.data.length > 0 && point.data[0].date > limit " class="ml-3 mr-3" style="text-align: right"> Online &#10004; </div>
                        <div v-if="point.data.length == 0 || point.data[0].date < limit" class="ml-3 mr-3 errorbtn " style="text-align: right"> Offline &#10006; </div>
                      </div>
                    </li>
                  </ul>
                  </br>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
    <br><br>
      <div style="width:160px" class="wc-button" v-on:click=addPoint> Add a device </div>
  </div>
  `,
  beforeMount(){
    this.points = JSON.parse(localStorage.points);
    this.limit = Math.round(new Date().getTime() - 3600000);
  }
};

let compModAdd_a_device = {
  data: function() {
    return {
      key: void 0,
      uid: void 0
    }
  },
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
        this.refresh()
      }
    },

    refresh: function(){
      vm.$refs.nav.modale('Devices');
      let data = {}
      vm.$refs.modal.loaddata(data);
    },

    adddevice: function(){
      let data = {}
      data['headers'] = cred.methods.get_headers()
      data['data'] = {"id_sig": this.uid}
      user.methods.send('point/add', data, this.infos);
    }
  },
  template: `
  <div>
    <form class="insidecomp">
      <div class="container">
        <div class="row">
          <div class="col-md-12 col-sm-12">
            <div class="container">
              <div class="row">
                <div class="hidemd col-sm-12 col-4 margin5px" for="uid">Device UID</div>
                <div class="col-md-3 hidesm"></div>
                <input class="form-control compinput col-md-6  col-sm-12 col-8" id="uid" type="text" placeholder="XXX-XXX-XXX" v-model="uid">
              </div>
            </div>
            <div class="sepinput"></div>
            <div class="container">
              <div class="row">
                <div class="hidemd col-sm-12 col-4 margin5px" for="key">Device key</div>
                <div class="col-md-3 hidesm"></div>
                <input class="form-control compinput col-md-6  col-sm-12 col-8" id="key" type="text" placeholder="XXX" v-model="key">
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
    <br><br>
    <div class="wc-button" v-on:click="adddevice()"> Let's go </div>
  </div>
  `
};
