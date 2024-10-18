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
                                        <i class="fa-solid fa-plus"></i> Add File</strong></h5>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true" class="text-danger"><i
                                            class="fa-regular fa-circle-xmark"></i></span>
                                </button>
                            </div>
                            <div class="modal-body">
                                <form @submit.prevent="addRecord()">
                                    <div class="form-group">
                                        <label>Select folder</label>
                                        <div class="row p-2 mb-2 ">
                                            <Multiselect id="select_id_folder" v-model="record.id_folder"
                                                placeholder="Select folder" :close-on-select="true"
                                                :searchable="true" :create-option="false" :options="folders" />
                                        </div>
                                        <span v-if="errors.id_folder" id="add_file_errors_id_folder" class="text-danger">{{ errors.id_folder }}<br></span>
                                    </div>
                                    <div class="form-group">
                                        <label>File Upload</label><br>
                                        <input type="file" ref="fileInput" id="file" @change="handleFileUpload" accept=".txt,.docx,.doc,.pdf" />
                                        <br>
                                        <span v-if="errors.file" id="add_file_errors_name" class="text-danger">{{ errors.file }}<br></span>
                                    </div>
                                    <button type="submit" class="mt-4 btn-pers" id="file_add_button"><i class="fa-solid fa-plus"></i> Add</button>
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
import Multiselect from '@vueform/multiselect'

export default {
    name: "AddRecord",
    props: {
        course_id: String,
        folders: Array,
    },
    setup() {

    },
    data() {
        return {
            selectedFile: null,
            record: {
                id_folder: null,
                file: null,
            },
            errors: {
                id_folder: null,
                file: null,
            }
        }
    },
    mounted() {
    },
    components: {
        Multiselect
    },
    computed: {
    },
    methods: {
        handleFileUpload(event) {
            this.record.file = event.target.files[0];
        },
        addRecord: async function () {
            this.errors = {
                id_folder: null,
                file: null,
            }
            if(this.record.file === null) {
                this.errors.file = 'File is required !'
            } else if(this.record.id_folder === null) {
                this.errors.id_folder = 'Folder selection is required !'
            } else {
                try {
                    const formData = new FormData();
                    for (let key in this.record) formData.append(key, this.record[key]);

                    await UserRequest.post('file/add/', formData, true);
                    this.$emitEvent('eventSuccess', 'File added successfully !');
                    var closePW = window.document.getElementById('addRecord');
                    closePW.click();
                    this.$refs.fileInput.value = '';
                    this.record = {
                        id_folder: null,
                        file: null,
                    };
                    this.errors = {
                        id_folder: null,
                        file: null,
                    }
                    this.$emitEvent('eventRegetDataRecords', '');
                }
                catch (error) {
                    this.errors.file = 'Error name.'
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
<style src="@vueform/multiselect/themes/default.css"></style>
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
