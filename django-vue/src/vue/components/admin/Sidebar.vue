<template>
    <div class="sidebar" data-background-color="white" data-active-color="danger">
        <div class="logo">
            <a href="///" class="simple-text">
                ARC
            </a>
        </div>
        <div class="sidebar-wrapper">
            <ul class="nav">

                <router-link tag="li" to="/" exact><a><i class="ti-panel"></i><p>Dashboard</p></a></router-link>
                <router-link tag="li" to="/readings"><a><i class="ti-view-list-alt"></i><p>Reading Material</p></a></router-link>
                <router-link tag="li" to="/users"><a><i class="ti-user"></i><p>Users</p></a></router-link>
                <router-link tag="li" to="/logout"><a><i class="ti-close"></i><p>Logout</p></a></router-link>
            </ul>
        </div>
    </div>
</template>

<script>

export default {
    components: {  },
    name: 'app',
    data () {
        return {
        }
    },
	mounted() {

	},
	created() {

	},
	methods: {

	}
}
</script>

<style lang="scss">
//@import './assets/sass/hms.scss';

</style>
