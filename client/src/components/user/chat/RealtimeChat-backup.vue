<template>
    <div class="account_setting">
        <iframe width="420" height="315" src="https://www.youtube.com/embed/2F1OqIihjTQ" frameborder="0"
            allowfullscreen></iframe>
        <br>
        <div>
            <h1>Messages</h1>
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Text</th>
                        <th scope="col">Update</th>
                        <th scope="col">Delete</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(message, index) in messages" :key="message.id">
                        <th scope="row">{{ index }}</th>
                        <td>{{ message.data.text }}</td>
                        <td><button class="btn btn-primary" @click="updateMessage(message.id)">Update</button></td>
                        <td><button class="btn btn-primary" @click="deleteMessage(message.id)">Delete</button></td>
                    </tr>
                </tbody>
            </table>
            <input v-model="newMessage" placeholder="Add a message">
            <button class="btn btn-primary" @click="addMessage">Add Message</button>
        </div>
    </div>
</template>

<script>
import useEventBus from '@/composables/useEventBus';
const { emitEvent } = useEventBus();

import { onSnapshot, addDoc, updateDoc, deleteDoc, doc } from 'firebase/firestore';
import { messagesRef } from '@/firebase';

export default {
    name: "RealtimeChat",
    data() {
        return {
            messages: [],
            newMessage: ''
        }
    },
    setup() {
        document.title = "Realtime Chat | Knowledge";
    },
    async mounted() {
        emitEvent('eventTitleHeader', 'Realtime Chat');
    },
    created() {
        this.getMessages();
    },
    components: {
        
    },
    methods: {
        getMessages() {
            onSnapshot(messagesRef, (snapshot) => {
                this.messages = snapshot.docs.map(doc => ({
                    id: doc.id,
                    data: doc.data()
                }));
            });
        },
        async addMessage() {
            if (this.newMessage.trim() !== '') {
                await addDoc(messagesRef, { text: this.newMessage });
                this.newMessage = '';
            }
        },
        async updateMessage(id) {
            const newText = prompt('Enter new text:');
            if (newText) {
                const messageDoc = doc(messagesRef, id);
                await updateDoc(messageDoc, { text: newText });
            }
        },
        async deleteMessage(id) {
            const messageDoc = doc(messagesRef, id);
            await deleteDoc(messageDoc);
        }
    },
}

</script>
<style scoped>
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