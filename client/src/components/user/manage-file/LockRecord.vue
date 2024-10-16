<template>
    <div>
        <div class="modal fade" id="lockRecord" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
            aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel"><i class="fa-solid fa-triangle-exclamation"></i>
                            Warning</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true" class="text-danger"><i class="fa-regular fa-circle-xmark"></i></span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-warning" role="alert">
                            <p>Cảnh báo : Khóa học này sẽ được chuyển sang trạng thái <strong>{{ recordSelected.is_delete == 0 ? 'Đã khóa' :
                                'Bình thường' }}</strong> trong hệ thống !</p>
                            <p>Tên khóa học : <strong>{{ recordSelected.course_name }}</strong> </p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-dismiss="modal" ref="closeButton"
                            id="close">Đóng</button>
                        <button type="button"
                            :class="{ 'btn': true, 'btn-outline-danger': recordSelected.is_block == 0, 'btn-outline-success': recordSelected.is_block == 1 }"
                            @click="functionLockRecord">
                            <i
                                :class="{ 'fa-solid': true, 'fa-lock': recordSelected.is_block == 0, 'fa-lock-open': recordSelected.is_block == 1 }"></i>
                            {{ recordSelected.is_block == 0 ? 'Khóa' : 'Mở khóa' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>

import UserRequest from '@/restful/UserRequest';

export default {
    name: "LockRecord",

    props: {
        recordSelected: Object
    },

    data() {
        return {
            dataSubmit: {
                is_block: '',
            }
        }
    },

    methods: {
        functionLockRecord: async function () {
            try {
                if (this.recordSelected.is_block == 0) this.dataSubmit.is_block = 1;
                else this.dataSubmit.is_block = 0;
                const { messages } = await UserRequest.get('admin/course/update-status/' + this.recordSelected.id, true);
                this.$emitEvent('eventSuccess', messages[0]);
                const closeButton = this.$refs.closeButton;
                closeButton.click();
                this.$emitEvent('eventUpdateIsBlockRecord', this.recordSelected.id);
            }
            catch (error) {
                if (error.errors) this.errors = error.errors;
                else for (let key in this.errors) this.errors[key] = null;
                if (error.messages) this.$emitEvent('eventError', error.messages[0]);
            }
        },
    }

}
</script>

<style scoped>
.modal-header .close {
    outline: none;
}

@media screen and (min-width: 1201px) {}

@media screen and (min-width: 993px) and (max-width: 1200px) {
    .modal-dialog {
        max-width: 400px;
        margin: 10px auto;
        font-size: 13px;;
    }

    .modal-header{
        padding: auto;
    }

    .modal-header .close {
        font-size: 20px;
    }

    .btn{
        font-size: 13px;
    }
}

@media screen and (min-width: 769px) and (max-width: 992px) {
    .modal-dialog {
        max-width: 350px;
        margin: 10px auto;
        font-size: 11px;;
    }

    .modal-header{
        padding: auto;
    }

    .modal-header .close {
        font-size: 18px;
    }

    .btn{
        font-size: 12px;
    }

    .modal-body{
        padding: 14px 14px 0 14px;
    }
}

@media screen and (min-width: 577px) and (max-width: 768px) {
    .modal-dialog {
        max-width: 320px;
        margin: 10px auto;
        font-size: 9px;;
    }

    .modal-header{
        padding: auto;
    }

    .modal-header .close {
        font-size: 11px;
    }

    .btn{
        font-size: 10px;
    }

    .modal-body{
        padding: 14px 14px 0 14px;
    }
    .alert{
        padding: 8px;
    }
}

@media screen and (min-width: 425px) and (max-width: 575px) {
    .modal-dialog {
        max-width: 275px;
        margin: 10px auto;
        font-size: 9px;;
    }

    .modal-header, .modal-footer{
        padding: 5px 5px;
    }

    .modal-header .close {
        font-size: 11px;
    }

    .btn{
        font-size: 8px;
    }

    .modal-body{
        padding: 12px 12px 0 12px;
    }

    .alert{
        padding: 8px;
    }
}

@media screen and (min-width: 375px) and (max-width: 424px) {
    .modal-dialog {
        max-width: 180px;
        margin: 10px auto;
        font-size: 7px;;
    }

    .modal-header, .modal-footer{
        padding: 5px 5px;
    }

    .modal-header .close {
        font-size: 9px;
    }

    .btn{
        font-size: 7px;
    }

    .modal-body{
        padding: 11px 11px 0 11px;
    }
    
    .alert{
        padding: 6px 10px;
    }
}
</style>