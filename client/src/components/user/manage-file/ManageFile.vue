<template>
    <div id="main">
        <div>
            <h3 class="titleChannel"> <i class="fa-solid fa-folder-tree"></i> Manage folders</h3>
        </div>
        <div class="ml-2 mt-2">
            <div class="mt-3">
                <div class="row m-0 pb-2 d-flex justify-content-end" id="search-sort">
                    <div class="col-1 pl-0" id="page">
                        <select id="file_per_page" content="Pagination" v-tippy class="form-control" v-model="big_search.per_page">
                            <option value="5">5</option>
                            <option value="10">10</option>
                            <option value="15">15</option>
                            <option value="20">20</option>
                        </select>
                    </div>
                    <div class="col-2 pl-0">
                        <select id="file_sort_by" content="Sắp xếp theo" v-tippy class="form-control " v-model="big_search.order_by">
                            <option value="id">ID</option>
                            <option value="name">Name</option>
                        </select>
                    </div>
                    <div class="col-2 pl-0">
                        <select id="file_sort_direction" content="Kiểu sắp xếp" v-tippy class="form-control " v-model="big_search.order_direction">
                            <option value="asc">Ascending</option>
                            <option value="desc">Descending</option>
                        </select>
                    </div>
                    <div class="col-2 pl-0">
                        <select content="Search by folder" v-tippy class="form-control " v-model="big_search.id_folder">
                            <option value="" >Search by folder</option>
                            <option :value="folder.value" v-for="(folder, index) in folders" :key="index">{{ folder.label }}</option>
                        </select>
                    </div> 
                    <div class="col-3 pl-0">
                        <div content="Search by file name" v-tippy class="input-group">
                            <div class="input-group-prepend">
                                <div class="input-group-text"><i class="fa-solid fa-magnifying-glass"></i></div>
                            </div>
                            <input v-model="search" type="text" class="form-control " id="file_input_search"
                                placeholder="Search by file name">
                        </div>
                    </div>
                    <button type="button" data-toggle="modal" data-target="#addRecord" class="btn btn-outline-success btn-sm"><i class="fa-solid fa-plus"></i> Create File</button>
                </div>
                <div v-if="isLoading">
                    <TableLoading :cols="8" :rows="9"></TableLoading>
                </div>
                <div v-if="!isLoading" class="tableData">
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th scope="col" class="w-10">#</th>
                                <th scope="col" class="w-10"><i class="fa-solid fa-signature"></i> ID</th>
                                <th scope="col" class="w-30"><i class="fa-solid fa-signature"></i> File Name</th>
                                <th scope="col" class="w-30"><i class="fa-solid fa-share-nodes"></i> Cypher</th>
                                <th scope="col" class="w-30"><i class="fa-solid fa-user-pen"></i> Action</th>
                            </tr>
                        </thead>
                        <tbody id="table_body_file">
                            <tr v-for="(record, index) in records" :key="index">
                                <th class="table-cell text-center" scope="row">#{{ (big_search.page - 1) * big_search.per_page + index +
                                    1 }}</th>
                                <td class="table-cell displaytext break text-center">{{ record.id }}</td>
                                <td class="table-cell displaytext break">{{ truncatedTitle(record.name) }}</td>
                                <td class="table-cell displaytext break"><textarea class="form-control" rows="3" v-model="record.content"></textarea></td>
                                <!-- <td class="table-cell text-center">{{ this.$formatDate2(record.created_at) }}</td> -->
                                <!-- <td class="table-cell text-center">{{ this.$formatDate2(record.updated_at) }}</td> -->
                                <td class="table-cell text-center">
                                    <div class="action">
                                        <div>
                                            <button data-toggle="modal" data-target="#updateRecord"
                                        v-tippy="{ content: 'Edit' }" class="updateRecord"
                                            @click="selectedRecord(record)">
                                            <i class="fa-solid fa-pen-to-square"></i>
                                        </button>
                                        <button data-toggle="modal" data-target="#deleteRecord"
                                            v-tippy="{ content: 'Delete'}"
                                            class="deleteRecord" @click="selectedRecord(record)">
                                            <i class="fa-solid fa-trash"></i>
                                        </button>
                                        </div>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div id="divpaginate" class="mt-2">
                    <paginate v-if="paginateVisible" :page-count="last_page" :page-range="3" :margin-pages="2"
                        :click-handler="clickCallback" :initial-page="big_search.page" :prev-text="'Prev'"
                        :next-text="'Next'" :container-class="'pagination'" :page-class="'page-item'">
                    </paginate>
                </div>
                <DeleteRecord :course_id="course_id" :recordSelected="recordSelected"></DeleteRecord>
                <!-- <LockRecord :recordSelected="recordSelected"></LockRecord>
                <ViewRecord :recordSelected="recordSelected"></ViewRecord> -->
                <AddRecord :course_id="course_id" :folders=folders></AddRecord>
                <UpdateRecord :recordSelected="recordSelected" :course_id="course_id"></UpdateRecord>
            </div>
        </div>
    </div>
</template>
<script>
import UserRequest from '@/restful/UserRequest';
import Paginate from 'vuejs-paginate-next';
import config from '@/config';
import TableLoading from '@/components/common/TableLoading'
import _ from 'lodash';
import DeleteRecord from '@/components/user/manage-file/DeleteRecord.vue'
// import LockRecord from '@/components/user/manage-file/LockRecord.vue'
// import ViewRecord from '@/components/user/manage-file/ViewRecord.vue'
import AddRecord from '@/components/user/manage-file/AddRecord.vue'
import UpdateRecord from '@/components/user/manage-file/UpdateRecord.vue'
// import UpdateInformationChannel from '@/components/user/member-account/UpdateInformationChannel.vue'

export default {
    name: "ManageFile",
    components: {
        paginate: Paginate,
        TableLoading,
        DeleteRecord,
        // LockRecord,
        // ViewRecord,
        AddRecord,
        UpdateRecord,
        // UpdateInformationChannel
    },
    setup() {
        document.title = "Manage File | Knowledge"
    },
    data() {
        return {
            course_id: null,
            config: config,
            total: 0,
            last_page: 1,
            paginateVisible: true,
            search:'',
            big_search: {
                per_page: 10,
                page: 1,
                id_folder: null,
                order_by: 'id',
                order_direction: 'desc',
            },
            query: '',
            records: [],
            folders: [],
            recordSelected: {
                id: null,
                chapter_name: null,
                course_id: null,
                position: null,
                created_at: null,
                updated_at: null,
            },
            isLoading: false,
            isDeleteChangeMany: 0,
			user: {
				id: null,
				email: null,
				user_name: null,
				role: null,
				is_delete: null,
				is_block: null,
				name: null,
				phone: null,
				email_verified_at: null,
				created_at: null,
				updated_at: null,
				access_token: null,
				token_type: null,
				expires_in: null,
			},
        }
    },
    mounted() {
        this.$emitEvent('eventTitleHeader', 'Manage File');
        this.$emitEvent('eventActiveTab', '');
        this.getListFolder();

        const queryString = window.location.search;
        const searchParams = new URLSearchParams(queryString);
        this.search = searchParams.get('search') || '';
        this.big_search = {
            per_page: parseInt(searchParams.get('per_page')) || 10,
            page: searchParams.get('page') || 1,
            order_by: searchParams.get('order_by') || 'id',
            order_direction: searchParams.get('order_direction') || 'desc',
            id_folder: searchParams.get('id_folder') || '', // null
        }
        this.getDataRecords();
        this.$onEvent('eventRegetDataRecords', () => {
            this.getDataRecords();
        });
        this.$onEvent('eventUpdateIsDeleteRecord', (id_record) => {
            this.records.forEach(record => {
                if (record.id == id_record) {
                    if (record.is_delete == 0) record.is_delete = 1;
                    else record.is_delete = 0;
                }
            });
        });
        this.$onEvent('eventUpdateIsBlockRecord', (id_record) => {
            this.records.forEach(record => {
                if (record.id == id_record) {
                    if (record.is_block == 0) record.is_block = 1;
                    else record.is_block = 0;
                }
            });
        });
    },

    methods: {
        gotoManageLesson: function(record) {
            // this.$router.push({ name: 'ManageLesson', params: { slug_name_course: record.course_slug + '-id-record-' + record.id } });
            this.$router.push({ name: 'ManageLesson', params: { slug_name_chapter: '-id-record-' + record.id } });
        },
        reRenderPaginate: function () {
            if (this.big_search.page > this.last_page) this.big_search.page = this.last_page;
            this.paginateVisible = false;
            this.$nextTick(() => { this.paginateVisible = true; });
        },
        getListFolder: async function () {
            try {
                const { data } = await UserRequest.post('folder/')
                console.log(data);
                var data_folders = data;
                data_folders.forEach((folder) => {
                    var option = { value: folder.id, label: `${folder.name}`}
                    this.folders.push(option);
                });
            }
            catch (error) {
                this.errors.name = 'Error name.'
                console.log(error);
                this.$emitEvent('eventError', 'Error something !');
            }
        },
        getDataRecords: async function () {
            this.isLoading = true;
            this.query = `?search=${this.search}&page=${this.big_search.page}&per_page=${this.big_search.per_page}&order_by=${this.big_search.order_by}&order_direction=${this.big_search.order_direction}&id_folder=${this.big_search.id_folder}`;
            // window.history.pushState({}, null, this.query);
            window.history.replaceState({}, null, this.query);
            try {
                var submit_search = {
                    search : this.search,
                    page : this.big_search.page,
                    per_page: this.big_search.per_page,
                    order_by : this.big_search.order_by,
                    order_direction : this.big_search.order_direction,
                    id_folder : this.big_search.id_folder
                }
                const { files, total, total_pages } = await UserRequest.post('file/', submit_search)
                this.records = files;
                console.log(files);
                this.total = total;
                this.last_page = total_pages;
                this.isLoading = false;
            }
            catch (error) {
                console.log(error);
                this.$emitEvent('eventError', error.messages[0]);
                this.isLoading = false;
            }
            this.reRenderPaginate();
        },
        truncatedTitle(title) {
            const maxLength = 150;
            if (title.length > maxLength) return title.slice(0, maxLength) + '...';
            else return title;
        },

        clickCallback: function (pageNum) {
            this.big_search.page = pageNum;
        },

        selectedRecord: async function (record) {
            this.$emitEvent('eventSelectedRecord', record);
            this.recordSelected = record;
        },

    },
    watch: {
        big_search: {
            handler: function () {
                this.getDataRecords();
            },
            deep: true
        },
        search: {
            handler: _.debounce(function () {
                this.getDataRecords();
            }, 500),
        },
    }
}
</script>

<style scoped>
.div_microphone {
    cursor: pointer;
}

.titleChannel {
    font-size: 19px;
    color: var(--user-color);
}

tr th {
    color: var(--user-color);
}

.colorTitle {
    color: gray;
}

.tableData {
    min-height: 20vh;
    overflow-y: scroll;
}

.coverCourse {
    display: flex;
    align-items: center;
    align-content: center;
}

.deleteRecord .fa-trash:hover {
    transition: all 0.5s ease;
    color: red;
}

.deleteRecord .fa-trash-arrow-up:hover {
    transition: all 0.5s ease;
    color: green;
}

.deleteRecord {
    transition: all 0.5s ease;
    font-size: 20px;
}

.viewRecord, .updateRecord {
    transition: all 0.5s ease;
    font-size: 20px;
}

.viewRecord i:hover {
    transition: all 0.5s ease;
    font-size: 20px;
    color: #007BFF;
}

.updateRecord i:hover {
    transition: all 0.5s ease;
    font-size: 20px;
    color: #007BFF;
}

.lockRecord {
    transition: all 0.5s ease;
    font-size: 20px;
}

.lockRecord .fa-lock:hover {
    transition: all 0.5s ease;
    color: red;
}

.lockRecord .fa-lock-open:hover {
    transition: all 0.5s ease;
    color: green;
}

.coverCourse img {
    border-radius: 6px;
}

.nameMember {
    margin-left: 10px;
}

#main {
    padding: 10px 20px;
    min-width: 375px !important;
}

#page {
    margin-right: auto;
    min-width: 78px;
}

table {
    font-size: 12px;
}

table img {
    width: 200px; 
    /* height:200px; */
    object-fit: cover;
}

.table-cell {
    font-weight: bold;
    vertical-align: middle;
}

table button {
    padding: 1px 3px;
    margin-right: 2px;
}

table thead th {
    vertical-align: middle;
    text-align: center;
}

.action {
    display: flex;
    align-items: center;
    justify-content: center;
}

.form-control{
    height: calc(1.5em + .5rem + 2px);
    padding: .25rem .5rem;
    font-size: .875rem;
    border-radius: 0.2rem;
    line-height: 1.5;
}

@media screen and (min-width: 1201px) {
    table {
        max-width: 100%;
        vertical-align: middle;
    }

    .coverCourse {
        min-width: 150px;
    }

    .displaytext {
        min-width: 150px;
        overflow: hidden;
        -webkit-line-clamp: 3 !important;
        -webkit-box-orient: vertical;
    }

    table img {
        min-width: 60px;
        min-height: 60px;
        /* max-width: 60px; */
        /* max-height: 60px; */
        object-fit: cover;
    }

    td .fa-solid {
        font-size: 20px;
    }

}

@media screen and (min-width: 993px) and (max-width: 1200px) {
    table {
        max-width: 100%;
        vertical-align: middle;
    }

    .coverCourse {
        min-width: 120px;
    }

    .displaytext {
        min-width: 100px;
        overflow: hidden;
        -webkit-line-clamp: 3 !important;
        -webkit-box-orient: vertical;

    }

    .break {
        word-break: break-all;
    }

    table {
        font-size: 11px;
    }

    .fa-solid {
        font-size: 15px;
    }

    table img {
        min-width: 50px;
        min-height: 50px;
        /* max-width: 50px;
        max-height: 50px; */
        object-fit: cover;
    }

    .table td,
    .table th {
        padding: 8px;
    }

    .form-control,
    .pagination {
        font-size: 12px !important;
    }

    #main {
        padding: 1% 1%;
        margin: 0;
    }
}

@media screen and (min-width: 769px) and (max-width: 992px) {
    .titleChannel {
        font-size: 15px;
    }

    .colorTitle {
        font-size: 14px;
    }

    table {
        max-width: 100%;
        vertical-align: middle;
    }

    .coverCourse {
        min-width: 140px;
    }

    .displaytext {
        min-width: 110px;
        overflow: hidden;
        -webkit-line-clamp: 3 !important;
        -webkit-box-orient: vertical;

    }

    .break {
        word-break: break-all;
    }

    table {
        font-size: 11px;
    }

    .fa-solid {
        font-size: 16px;
    }

    table img {
        min-width: 50px;
        min-height: 50px;
        max-width: 50px;
        max-height: 50px;
        object-fit: cover;
    }

    .table td,
    .table th {
        padding: 8px;
    }

    .form-control,
    .pagination {
        font-size: 12px !important;
    }

    #main {
        padding: 1% 1%;
        margin: 0;
    }

    .col-1,
    .col-2,
    .col-3 {
        padding-left: 0;
        padding-right: 10px;
    }

    .btn {
        padding: 0px 4px;
        margin-top: 3px;
    }

    .input-group-text {
        padding: 0 8px;
    }
}

@media screen and (min-width: 577px) and (max-width: 768px) {

    .titleChannel,
    .colorTitle {
        font-size: 13px;
    }

    table {
        max-width: 100%;
        vertical-align: middle;
    }

    .coverCourse {
        min-width: 100px;
    }

    .displaytext {
        min-width: 90px;
        overflow: hidden;
        -webkit-line-clamp: 3 !important;
        -webkit-box-orient: vertical;

    }

    .break {
        word-break: break-all;
    }

    table {
        font-size: 11px;
    }

    .fa-solid {
        font-size: 13px;
    }

    table img {
        min-width: 40px;
        min-height: 40px;
        max-width: 40px;
        max-height: 40px;
        object-fit: cover;
    }

    .table td,
    .table th {
        padding: 5px;
    }

    .form-control,
    .pagination {
        font-size: 12px !important;
    }

    #page {
        min-width: 45px;
    }
    
    .form-control {
        padding: 1px 1px;
    }

    #main {
        padding: 1% 1%;
        margin: 0;
    }

    .col-1,
    .col-2,
    .col-3 {
        padding-right: 5px;
    }

    .btn {
        padding: 0px 4px;
        margin-top: 3px;
    }

    .input-group-text {
        padding: 0 4px;
    }

    .input-group-prepend {
        font-size: 12px;

    }
}

@media screen and (min-width: 425px) and (max-width: 576px) {

    .titleChannel,
    .colorTitle {
        font-size: 12px;
    }

    table {
        max-width: 100%;
        vertical-align: middle;
    }

    .nameMember {
        margin-left: 8px;
    }

    .coverCourse {
        min-width: 100px;
    }

    .displaytext {
        min-width: 70px;
        overflow: hidden;
        -webkit-line-clamp: 3 !important;
        -webkit-box-orient: vertical;

    }

    .break {
        word-break: break-all;
    }

    table {
        font-size: 10px;
    }

    .fa-solid {
        font-size: 10px;
    }

    table img {
        min-width: 40px;
        min-height: 40px;
        max-width: 40px;
        max-height: 40px;
        object-fit: cover;
    }

    .table td,
    .table th {
        padding: 4px;
    }

    .form-control,
    .pagination {
        font-size: 10px !important;
    }

    .form-control {
        padding: 1px 1px;
        height: 25px;
    }

    #page {
        min-width: 45px;
    }

    #main {
        padding: 1% 1%;
        margin: 0;
    }

    .col-1,
    .col-2,
    .col-3 {
        padding-right: 5px;
    }

    .btn {
        padding: 0px 4px;
    }

    .input-group-text {
        padding: 0 0.5px;
    }

    .input-group-prepend {
        font-size: 11px;

    }
}

@media screen and (min-width: 375px) and (max-width: 424px) {
    .titleChannel,
    .colorTitle {
        font-size: 11px;
    }

    table {
        max-width: 100%;
        vertical-align: middle;
    }

    .nameMember {
        margin-left: 8px;
    }

    .coverCourse {
        min-width: 80px;
    }

    .displaytext {
        min-width: 70px;
        overflow: hidden;
        -webkit-line-clamp: 3 !important;
        -webkit-box-orient: vertical;

    }

    .break {
        word-break: break-all;
    }

    table {
        font-size: 9px;
    }

    .fa-solid {
        font-size: 10px;
    }

    table img {
        min-width: 40px;
        min-height: 40px;
        max-width: 40px;
        max-height: 40px;
        object-fit: cover;
    }

    .table td,
    .table th {
        padding: 4px;
    }

    .form-control,
    .pagination {
        font-size: 9px !important;
    }

    .form-control {
        padding: 0.5px 0;
        height: 25px;
    }

    #page {
        min-width: 40px;
    }

    #main {
        padding: 1% 1%;
        margin: 0;
    }

    .col-1,
    .col-2,
    .col-3 {
        padding-right: 0;
    }

    .btn {
        padding: 0px 4px;
    }

    .input-group-text {
        padding: 0 0.5px;
    }

    .input-group-prepend {
        font-size: 10px;

    }

    #main .ml-2{
        margin-left: 3px !important;
    }
}
</style>
