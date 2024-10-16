<template>
    <div class="account_setting">
        <div>
            <h1>Messages</h1>
            <!-- {{ latestNotify.id }} - {{ latestNotify.data.id_from }} - {{ latestNotify.data.id_to }} - {{ latestNotify.data.content }} - {{ latestNotify.data.created_at }} -->
            <div v-for="(message, index) in messages" :key="index">
                <p  :class="{'send':this.user.id == message.data.id_from,'receive':this.user.id == message.data.id_to}">{{ message.data.content }}</p>
            </div>
            <br>
            <input v-model="newMessage" placeholder="Add a message">
            <button class="btn btn-primary" @click="addMessage">Add Message</button>
        </div>
    </div>
</template>

<script>
import useEventBus from '@/composables/useEventBus';
const { emitEvent } = useEventBus();

import { addDoc, updateDoc, deleteDoc, doc, serverTimestamp, query, orderBy, limit, onSnapshot } from 'firebase/firestore';
import { notifiesRef } from '@/firebase';

export default {
    name: "RealtimeChat",
    data() {
        return {
            user: {
                id: null,
                email: null,
                role: null,
                line_user_id: null,
                channel_id: null,
                name: null,
                phone: null,
                avatar: null,
                address: null,
                gender: null,
                date_of_birth: null,
                is_block: null,
                is_delete: null,
                email_verified_at: null,
                created_at: null,
                updated_at: null,
                expires_in: null,
                token_type: null,
                access_token: null,
            },
            messages: [],
            id_to_user: null,
            latestNotify: { // muốn sử dụng chi tiết thì phải khai báo đủ các property 
                id: null,
                data: {
                    id_from : null,
                    id_to : null,
                    content : null,
                    created_at: null,
                }
            },
            newMessage: '',
        }
    },
    setup() {
        document.title = "Realtime Chat | Knowledge";
    },
    async mounted() {
        this.user = JSON.parse(localStorage.getItem('user'));
        this.id_to_user = this.$route.params.id_to_user;
        emitEvent('eventTitleHeader', 'Realtime Chat');
        // this.getNotifies();
    },
    created() {
        this.getNotifies();
    },
    components: {

    },
    methods: {
        getNotifies() {
            const latestNotifyQuery = query(
                notifiesRef,
                orderBy('created_at', 'desc'),
                limit(1)
            );
            onSnapshot(latestNotifyQuery, (snapshot) => {
                if (!snapshot.empty) {
                    const doc = snapshot.docs[0];
                    this.latestNotify = {
                        id: doc.id,
                        data: doc.data()
                    };

                    // check
                    // Kiểm tra xem tin nhắn đã tồn tại trong mảng messages chưa
                    const exists = this.messages.some(message => message.id === this.latestNotify.id);

                    if (!exists) {
                        // nhắn đến người kia 
                        if(this.latestNotify.data.id_from == this.user.id && this.latestNotify.data.id_to == this.id_to_user) {
                            this.messages.push(this.latestNotify);
                        }
                        // người kia nhắn cho mình 
                        if(this.latestNotify.data.id_from == this.id_to_user && this.latestNotify.data.id_to == this.user.id) {
                            this.messages.push(this.latestNotify);
                        }
                    }
                    
                } else {
                    this.notifies = [];
                }
            });
        },
        async addMessage() {
            if (this.newMessage.trim() !== '') {
                try {
                    await addDoc(notifiesRef, {
                        id_from: this.user.id,
                        id_to: this.id_to_user,
                        content: this.newMessage,
                        created_at: serverTimestamp() // Lấy thời gian hiện tại từ Firebase
                    });
                    this.newMessage = '';
                } catch (error) {
                    console.error("Error adding document: ", error);
                }
            }
        },
        async updateMessage(id) {
            const newText = prompt('Enter new text:');
            if (newText) {
                const messageDoc = doc(notifiesRef, id);
                await updateDoc(messageDoc, { text: newText });
            }
        },
        async deleteMessage(id) {
            const messageDoc = doc(notifiesRef, id);
            await deleteDoc(messageDoc);
        }
    },
}

</script>
<style scoped>
.send {
    display: flex;
    justify-content: end;
}

.receive {
    display: flex;
    justify-content: start;
}

@media screen and (min-width: 1201px) {

    .col-5,
    .col-2 {
        padding-right: 30px;
    }
}

@media screen and (min-width: 993px) and (max-width: 1200px) {
    .minAvatar {
        width: 150px;
        height: 150px;
    }

    .minAvatar .preview {
        width: 130px;
        height: 130px;
    }

    .col-5,
    .col-2 {
        padding-right: 2%;
    }
}

@media screen and (min-width: 769px) and (max-width: 992px) {
    .innerContent>div {
        padding: 8px 11px;
        font-size: 15px;
    }

    .minAvatar {
        width: 110px;
        height: 110px;
    }

    .minAvatar .preview {
        width: 100px;
        height: 100px;
    }

    .contact-info .col-12 {
        padding-right: 20px;
        padding-left: 3px;
    }

    .col-5,
    .col-2 {
        padding-right: 2%;
        padding-left: 1%;
        font-size: 14px;
    }

    .form-control,
    .groupCheckbox,
    .input-group-text {
        font-size: 13px !important;
    }

    .btn-pers {
        font-size: 11px;
    }
}

@media screen and (min-width: 577px) and (max-width: 768px) {
    .contact-info {
        flex-direction: column;
    }

    .innerContent>div {
        padding: 8px 11px;
        font-size: 13px;
    }

    .minAvatar {
        width: 150px;
        height: 150px;
    }

    .minAvatar .preview {
        width: 130px;
        height: 130px;
    }

    .contact-info .col-12 {
        padding-right: 20px;
        padding-left: 3px;
    }

    .col-5,
    .col-2 {
        padding: 0 5%;
        font-size: 13px;
        max-width: 100% !important;
    }

    .col-2 {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }

    .form-control,
    .groupCheckbox,
    .input-group-text {
        font-size: 13px !important;
    }

    .btn-pers {
        font-size: 11px;
    }
}

@media screen and (min-width: 375px) and (max-width: 576px) {
    .contact-info {
        flex-direction: column;
    }

    .innerContent>div {
        padding: 8px 11px;
        font-size: 12px;
    }

    .minAvatar {
        width: 150px;
        height: 150px;
    }

    .minAvatar .preview {
        width: 130px;
        height: 130px;
    }

    .contact-info .col-12 {
        padding-right: 20px;
        padding-left: 3px;
    }

    .col-5,
    .col-2 {
        padding: 0 5%;
        font-size: 13px;
        max-width: 100% !important;
    }

    .col-2 {
        display: flex;
        justify-content: center;
        margin-top: 25px;
    }

    .form-control,
    .groupCheckbox,
    .input-group-text {
        font-size: 12px !important;
    }

    .btn-pers {
        font-size: 11px;
    }
}
</style>