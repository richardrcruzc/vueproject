<template>
    <nav id="sidebar" class="navbar navbar-default">
        <div class="container-fluid">
            <div class="navbar-header">
                <div :class="{bordered: showSidebar}">
                <button type="button" class="navbar-toggle" :class="{toggled: showSidebar}"
                        @click="toggleSidebar">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar bar1"></span>
                    <span class="icon-bar bar2"></span>
                    <span class="icon-bar bar3"></span>
                </button>
                <div class="collapse navbar-collapse" :class="showSidebar ? 'in' : 'arc-collapse'">
                    <ul class="nav navbar-nav">
                        <router-link tag="li" to="/" exact><a><i class="ti-panel"></i><p>Dashboard</p></a></router-link>
                        <router-link tag="li" to="/readings"><a><i class="ti-view-list-alt"></i><p>Reading Material</p></a></router-link>
                        <router-link tag="li" to="/users"><a><i class="ti-user"></i><p>Users</p></a></router-link>
                        <router-link tag="li" to="/logout"><a><i class="ti-close"></i><p>Logout</p></a></router-link>
                    </ul>
                </div>
                </div>
                <a class="navbar-brand" href="#">Page Title</a>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'app',
    data () {
        return {
            showSidebar: false,
        }
    },
    computed: {
    },
	mounted() {

	},
	created() {

	},
	methods: {
        toggleSidebar() {
            this.showSidebar = !this.showSidebar;
        }
	}
}
</script>