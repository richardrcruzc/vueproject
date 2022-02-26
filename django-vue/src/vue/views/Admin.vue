<template>
    <div id="app" class="wrapper">
        <sidebar></sidebar>
        <div class="main-panel">
            <navbar></navbar>
            <div class="content">
                <router-view></router-view>
            </div>
            <footer class="footer">
                <div class="container-fluid">
                    <div class="copyright pull-right">
                        &copy;
                        {{ this_year }}
                        ARC by <a href="https://moe.gov.sg" target="_blank">MOE Singapore</a>
                    </div>
                </div>
            </footer>
        </div>
    </div>
</template>

<script>
import Sidebar from '../components/admin/Sidebar.vue'
import Navbar from '../components/admin/Navbar.vue'

export default {
    components: { Sidebar, Navbar },
    name: 'app',
    data () {
        return {
        }
    },
    computed: {
        this_year() {
            return new Date().getFullYear();
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
//@import '../node_modules/bulma/bulma.sass';
//@import './assets/sass/hms.scss';

</style>
