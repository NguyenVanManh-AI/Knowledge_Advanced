<template>
    <div>
        <div id="big">
            <div class="bigContainer">
                <div class="modal fade" id="addRecord" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
                    aria-hidden="true">
                    <div class="modal-dialog" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="exampleModalLabel"><strong>
                                        <i class="fa-solid fa-plus"></i> Add Folder</strong></h5>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true" class="text-danger"><i
                                            class="fa-regular fa-circle-xmark"></i></span>
                                </button>
                            </div>
                            <div class="modal-body">
                                <form @submit.prevent="addRecord()">
                                    <div class="form-group">
                                        <label><i class="fa-solid fa-folder"></i> Folder name</label>
                                        <input name="add_folder_name" v-model="record.name" type="text" class="form-control form-control-sm" id="exampleInputEmail1"
                                            aria-describedby="emailHelp" placeholder="Name Folder">
                                        <span v-if="errors.name" class="text-danger" id="add_folder_errors_name">{{ errors.name }}<br></span>
                                    </div>
                                    <button type="submit" class="mt-4 btn-pers" id="folder_add_button"><i class="fa-solid fa-plus"></i> Add</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import UserRequest from '@/restful/UserRequest';

export default {
    name: "AddRecord",
    props: {
        course_id: String,
    },
    setup() {

    },
    data() {
        return {
            previewImageSrc: null,
            updateImage: false,
            record: {
                name: '',
            },
            errors: {
                name: null,
            }
        }
    },
    mounted() {
    },
    components: {
    },
    computed: {
    },
    methods: {
        addRecord: async function () {
            if(this.record.name === '') {
                this.errors.name = 'Folder name cannot be empty !'
            } else {
                try {
                    await UserRequest.post('folder/add/', this.record, true);
                    this.$emitEvent('eventSuccess', 'Folder added successfully !');
                    var closePW = window.document.getElementById('addRecord');
                    closePW.click();
                    this.record = {
                        name: null,
                    };
                    this.errors.name = null;
                    this.$emitEvent('eventRegetDataRecords', '');
                }
                catch (error) {
                    this.errors.name = 'Error name.'
                    console.log(error);
                    this.$emitEvent('eventError', 'Error something !');
                }
            }
        },
    },
    watch: {

    },
}
</script>

<style scoped>
/* image upload */
.big-container-image {
    display: flex;
    align-items: center;
    align-content: center;
    /* height: 100%; */
}

.inner-image-upload {
    height: 50%;
    width: 100%;
}

.min-image-upload {
    background-color: #e9ecef;
    position: relative;
    text-align: center;
    /* width: 170px; */
    height: 170px;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.5s ease;
    width: 100%;
}

.min-image-upload .preview {
    /* width: 150px; */
    height: 150px;
    object-fit: cover;
    border-radius: 6px;
    cursor: default;
    width: 100%;
}

.min-image-upload:hover {
    transition: all 0.5s ease;
    background: #E8F5E9;
}

.input-file {
    opacity: 0;
    top: 0px;
    left: 0px;
    position: absolute;
    cursor: pointer;
    /* width: 150px; */
    height: 150px;
    width: 100%;
}

.box-preview {
    position: relative;
}

.iconClound {
    cursor: pointer;
    font-size: 60px;
    color: var(--user-color);
}

.close-img {
    position: absolute;
    top: -6px;
    right: -6px;
    width: 16px;
}

/* image upload */


/*  */
.modal-dialog {
    max-width: 800px;
}

/*  */


.modal.fade.show {
    padding-left: 0px;
}

.modal-content {
    /* margin-top: 100px; */
    border-radius: 10px;
}

.bigContainer .input-form {
    height: 40px;
    width: 100%;
    position: relative;
}

.bigContainer .input-form input {
    height: 100%;
    width: 100%;
    border: none;
    font-size: 17px;
    border-bottom: 2px solid silver;
    outline: none !important;
}

.input-form input:focus~label,
.input-form input:valid~label {
    transform: translateY(-20px);
    font-size: 15px;
    color: var(--user-color);
}

.input-form .underline.fix2:before {
    position: absolute;
    content: "";
    height: 100%;
    width: 100%;
    background: var(--user-color);
    transform: scaleX(0);
    transform-origin: center;
    transition: transform 0.3s ease;
}

.bigContainer .input-form label {
    position: absolute;
    bottom: 0px;
    left: 0;
    color: grey;
    pointer-events: none;
    transition: all 0.3s ease;
}

.input-form .underline {
    position: absolute;
    height: 2px;
    width: 100%;
    bottom: 0;
}

.input-form .underline:before {
    position: absolute;
    content: "";
    height: 100%;
    width: 100%;
    background: var(--user-color);
    transform: scaleX(0);
    transform-origin: center;
    transition: transform 0.3s ease;
}

.input-form input:focus~.underline:before,
.input-form input:valid~.underline:before {
    transform: scaleX(1);
}

@import url('https://fonts.googleapis.com/css2?family=Reem+Kufi+Ink');

#big {
    display: flex;
    position: relative;
}

.btn-pers {
    position: relative;
    left: 50%;
    padding: 1em 2.5em;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-weight: 700;
    color: #000;
    background-color: #fff;
    border: none;
    border-radius: 45px;
    box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease 0s;
    cursor: pointer;
    outline: none;
    transform: translateX(-50%);
}

.btn-pers:hover {
    background-color: var(--user-color);
    box-shadow: var(--btn-hover);
    color: #fff;
    transform: translate(-50%, -7px);
}

.btn-pers:active {
    transform: translate(-50%, -1px);
}

#inputPassword {
    padding-right: 26px;
}
</style>
