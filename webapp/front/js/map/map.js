Vue.component('compModDevices', compModDevices);
Vue.component('compModShare', compModShare);
Vue.component('compModAdd_a_device', compModAdd_a_device);


let vm = new Vue({
    el: '#map',

    data: function(){
      return {
        email: localStorage.email,
        markers: null
      }
    },

    components: {msg, leftnav, mod},

    methods:{
      datestr: function(timestamp) {
        let date = new Date(parseInt(timestamp));
        let day = ("00" + date.getDate())
        day = day.substr(day.length - 2);
        let month = ("0" + (date.getMonth() + 1))
        month = month.substr(day.length - 2);
        let str = day + '.' + month + '.' + date.getFullYear();
        return str;
      },
      update: function(){
        var test;
        var last_data;
        for (var i = 0; i < this.markers['proprietary'].length; i++){
          test = this.markers['proprietary'][i]["test"]
          last_data = this.markers['proprietary'][i]["data"][0]
          this.markers['proprietary'][i]["marker"]
            = new google.maps.Marker({
                position: new google.maps.LatLng(last_data['data']['pos']['lat'], last_data['data']['pos']['lon']),
                title:this.markers['proprietary'][i]["name"],
                map: test == true && (localStorage.testmode == "false" || localStorage.testmode == void 0) ? null :  map,
                data: {'id': this.markers['proprietary'][i]['id'], 'order': i},
                icon: {
                    url: test == true ? "./imgs/float_test.svg" : "./imgs/float.svg", // url
                    scaledSize: new google.maps.Size(35, 35), // scaled size
                    origin: new google.maps.Point(0,0), // origin

                }
          });
          this.markers['proprietary'][i]['note'] = 3
          this.markers['proprietary'][i]["infos"] = new google.maps.InfoWindow({
            content: `<div class="inf-content" style="font-size: 15px;">
              <div class="container">
                <div class="row">
                  <div class="col-12 col-sm-6" style="margin-top: 5px;">
                    Name: ` + this.markers['proprietary'][i]['name'] + `
                  </div>
                  <div class="col-12 col-sm-6" style="margin-top: 5px;">
                    Surname: ` + this.markers['proprietary'][i]['surname'] + `
                  </div>
                  <div class="col-12 col-sm-6" style="font-size: 11px;margin-top: 5px;">
                    Since: ` + this.datestr(this.markers['proprietary'][i]['date']) + `
                  </div>
                  <div class="col-12 col-sm-6" style="font-size: 11px;margin-top: 5px;">
                    Last report: ` + (this.markers['proprietary'][i]['data'].length > 0 ? this.datestr(this.markers['proprietary'][i]['data'][0]["date"]) : '/' ) + `
                  </div>
                  <div class="col-12 col-sm-12" style="text-align: center; margin-top: 5px;">
                  Note: ` + (this.markers['proprietary'][i]["data"][0]['note'] ? this.markers['proprietary'][i]["data"][0]['note'] : '_' ) + ` / 10
                  <div class="notebarholder">
                    <div class="notebar" style=" ` + (
                        this.markers['proprietary'][i]["data"][0]['note'] ?
                        this.markers['proprietary'][i]["data"][0]['note'] > 7 ? 'background-color: #03ba00; width: ' + (this.markers['proprietary'][i]["data"][0]['note'] / 19 * 10) + '%;' :
                        this.markers['proprietary'][i]["data"][0]['note'] > 4 ? 'background-color: #ff970f; width: ' + (this.markers['proprietary'][i]["data"][0]['note'] / 19 * 10) + '%;' :
                        'background-color: red; width: ' + (this.markers['proprietary'][i]["data"][0]['note'] / 19 * 10) + '%;' : 'width: 0%' ) + `">
                    </div>
                  </div>
                  </div>

                </div>
              </div>
            </div>`,
            map: map
          });
        }
        setTimeout(() => {this.setmarkers()}, 500);
        for (var i = 0; i< this.markers['shared'].length; i++){

        }

      },

      testpointer: function(print){
        for (var i = 0; i < this.markers['proprietary'].length; i++){
          if (this.markers['proprietary'][i]['test'] == true ) {
            if (print == false){
              this.markers['proprietary'][i]["marker"].setMap(null);
              this.markers['proprietary'][i]["infos"].close()
            } else {
              this.markers['proprietary'][i]["marker"].setMap(map);
            }
          }
        }
      },

      moveto: function(id, marker = null, force = false){
        var done = false;
        if (marker != null){
          done = true
        }
        for (var i = 0; !done && i < this.markers['proprietary'].length; i++){
          if (this.markers['proprietary'][i]['id'] == id){
            marker = this.markers['proprietary'][i]
            done = true;
          }
        }
        for (var i = 0; !done && i < this.markers['shared'].length; i++){
          if (this.markers['shared'][i]['id'] == id){
            marker = this.markers['shared'][i];
            done = true;
          }
        }
        if (done == true) {
          if (force == true){
            if (map.getZoom() < 8){
              map.setZoom(8);
            }
            map.panTo(marker['marker'].getPosition());
          }


          for (var i = 0; i < this.markers['shared'].length; i++){
            this.markers['shared'][i]['infos'].close();
          }
          for (var i = 0; i < this.markers['proprietary'].length; i++){
            this.markers['proprietary'][i]['infos'].close();
          }
          marker['infos'].open(map, marker['marker']);
          let center = map.getCenter();
          let pos = {'lat': center.lat(), 'lng': center.lng(), 'zoom': map.getZoom()};
          localStorage.position = JSON.stringify(pos);
        }
      },

      setmarkers: function(){
        for (var i = 0; i < this.markers['proprietary'].length; i++){
          this.markers['proprietary'][i]["marker"].addListener('click', function() {
            vm.moveto(this.data['id']);
          }, false);
        }
      },

      infos: function(res) {
        let data = {}
        data['headers'] = cred.methods.get_headers()
        data['data'] = {}
        if (res == void 0 || res['data_added'] == void 0){
          user.methods.send('points/infos', data, this.store);
        } else {
          user.methods.send('points/infos', data, this.storebis);
        }
      },
      storebis: function(data){
          if (data != '') {
            localStorage.points = JSON.stringify(data['points']);
            this.markers = data['points'];
            this.update();
          }
      },
      store: function(data) {
        if (data != '') {
          localStorage.points = JSON.stringify(data['points']);
          this.markers = data['points'];
          this.update();
          for (var i = 0; i < this.markers['proprietary'].length; i++){
            if (this.markers['proprietary'][i]['test'] == true && this.markers['proprietary'][i]['data'].length == 0){
              let data = {}
              data['headers'] = cred.methods.get_headers()
              data['data'] = {
                "data": {
                	"data": {

                  },
                	"pos": {"lon": map.getCenter().lng(), "lat": map.getCenter().lat()}
                },
                "point_id": this.markers['proprietary'][i]['id'],
                "sig_id": -1
              };
              user.methods.send('data/add', data, this.infos);
            }
          }
        }
      },
   },
   mounted(){
     cred.methods.api_cred()
     cred.methods.usr_cred()
     this.infos();
   }
})
