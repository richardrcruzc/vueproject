var app = new Vue({
  el: '#sidebar',
  data: {
    showSidebar: false,
    type: {
        type: String,
        default: 'sidebar',
        validator: (value) => {
          let acceptedValues = ['sidebar', 'navbar']
          return acceptedValues.indexOf(value) !== -1
        }
      },
  },
  mounted: function () {
  },
  computed: {
      sidebarClasses () {
        if (this.type === 'sidebar') {
          return 'sidebar'
        } else {
          return 'collapse navbar-collapse off-canvas-sidebar'
        }
      },
  },
  methods: {
    displaySidebar: function(shownValue) {
        this.showSidebar = shownValue;
    },
    toggleSidebar: function() {
        this.showSidebar = !this.showSidebar;
    }
  }
})