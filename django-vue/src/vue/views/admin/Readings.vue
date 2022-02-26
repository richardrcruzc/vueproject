<template>
<div class="container-fluid">
    <div class="row">
        <div class="col-md-12">
            <div class="card card-plain">
                <router-link :to="{ name: 'Reading', params: { action: 'add'} }" class="pull-right btn btn-fill btn-wd" style="margin-bottom: 20px;">Add new readings</router-link>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-md-12 card">
            <div class="card-header">
                <div class="category">Extended tables</div>
            </div>
            <div class="card-content row">
                <div class="col-sm-12">
                    <el-table class="table table-striped table-no-bordered table-hover" :data="tableData" border style="width: 100%">
                        <el-table-column v-for="(column, index) in tableColumns"
                             :min-width="column.minWidth"
                             :prop="column.prop"
                             :label="column.label"
                             :key="index"
                             sortable>
                        </el-table-column>

                        <el-table-column :min-width="120" label="Actions">
                            <template slot-scope="props">
                                <a class="btn btn-simple btn-xs btn-info btn-icon like" @click="handleLike(props.$index, props.row)"><i class="ti-heart"></i></a>
                                <a class="btn btn-simple btn-xs btn-warning btn-icon edit" @click="handleEdit(props.$index, props.row)"><i class="ti-pencil-alt"></i></a>
                                <a class="btn btn-simple btn-xs btn-danger btn-icon remove"  @click="handleDelete(props.$index, props.row)"><i class="ti-close"></i></a>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
                <div class="col-sm-6 pagination-info">
                    <p class="category">Showing {{from + 1}} to {{to}} of {{total}} entries</p>
                </div>
                <div class="col-sm-6">
                    <p-pagination class="pull-right"
                        v-model="pagination.currentPage"
                        :per-page="pagination.perPage"
                        :total="pagination.total">
                    </p-pagination>
                </div>

                <div class="clearfix"></div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import PPagination from '../../components/admin/Pagination.vue'
export default {
    name: 'app',
    components: { PPagination },
    data () {
        return {
            inProgress: false,
            pagination: {
                currentPage: 1,
                perPage: 10,
                total: 0
            },
            tableColumns: [
            {
                prop: 'difficulty',
                label: 'Difficulty',
                minWidth: 200
            },
            {
                prop: 'excerpt',
                label: 'Reading',
                minWidth: 250
            },
            {
                prop: 'questions',
                label: 'Questions',
                minWidth: 100
            },
            {
                prop: 'updated',
                label: 'Last Updated',
                minWidth: 120
            },
            {
                prop: 'created',
                label: 'Created',
                minWidth: 120
            }],
            tableData: [],
            readings: [],
        }
    },
    computed: {
        from() {
            return this.pagination.perPage * (this.pagination.currentPage - 1)
        },
        to() {
            let highBound = this.from + this.pagination.perPage
            if (this.total < highBound) {
                highBound = this.total
            }
            return highBound
        },
        total() {
            return this.pagination.length
        }
    },
	mounted() {
        this.fetch_readings(1);
	},
	created() {

	},
	methods: {
        get_excerpt(str, max_len=50) {
            if (str.leng <= max_len) {
                return str;
	        }

            return str.substring(0, max_len-3) + '...';
        },
        fetch_readings(reqPage) {
            let self = this;

            self.pagination.requestPage = reqPage
            self.inProgress = true
            axios.get('/api/reading/list', {
                params: {
                    page: reqPage
                }
            })
            .then(function (response) {
                if (response.data.status === 0) {
                    let readingData = response.data.data.reading;
                    let paginationData = response.data.data.pagination;

                    self.tableData.length = 0;
                    for (let i=0; i < readingData.length; i++) {
                        self.tableData.push({
                            id: readingData[i].id,
                            excerpt: readingData[i].excerpt,
                            reading: readingData[i].reading,
                            questions: readingData[i].questions,
                            difficulty: readingData[i].difficulty,
                            updated: readingData[i].updated,
                            created: readingData[i].created
                        }
                        );
                    }
                    console.log(paginationData);
                    self.pagination.total = paginationData.total_items;
                    //self.pagination.currentPage = paginationData.number;
                    self.pagination.perPage = paginationData.per_page;
                }

                self.inProgress = false
            })
            .catch(function (error) {
                console.log(error);
                self.inProgress = false;
            });
        }
	},
	watch: {
	    'pagination.currentPage' (value) {
	        this.fetch_readings(this.pagination.currentPage);
	    }
	}
}
</script>