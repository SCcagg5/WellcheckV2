
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
