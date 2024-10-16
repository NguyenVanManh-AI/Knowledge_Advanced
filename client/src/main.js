import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import router from './router/routes'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'jquery/src/jquery.js'
import 'bootstrap/dist/js/bootstrap.min.js'
import Paginate from "vuejs-paginate-next";
import storeConfigs from './store/store'
import { quillEditor } from "vue3-quill";
import Notifications from "vue3-vt-notifications";
import "tailwindcss/dist/tailwind.css";
import DisableAutocomplete from 'vue-disable-autocomplete';
import print from 'vue3-print-nb'
import Particles from "particles.vue3";
import '../node_modules/nprogress/nprogress.css'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import VueTippy from 'vue-tippy'
import 'tippy.js/dist/tippy.css';
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import 'floating-vue/dist/style.css'

import useEventBus from '@/composables/useEventBus'
const { emitEvent, onEvent } = useEventBus();

import { extractFileName, formatDate, formatDate2, getYouTubeEmbedUrl, extractIdFromSlug, removeStringFromFileLink, formatNumber } from './helper'

const app = createApp(App);
app.use(router);
app.use(VueAxios, axios)
app.use(storeConfigs)
app.use(Paginate)
app.use(quillEditor)
app.use(Notifications)
app.use(DisableAutocomplete)
app.use(print)
app.use(Particles)
app.use(VueDatePicker)
app.use(VueTippy)
app.use(VueSweetalert2)
app.config.globalProperties.$emitEvent = emitEvent
app.config.globalProperties.$onEvent = onEvent
app.config.globalProperties.$formatDate = formatDate
app.config.globalProperties.$formatDate2 = formatDate2
app.config.globalProperties.$getYouTubeEmbedUrl = getYouTubeEmbedUrl
app.config.globalProperties.$extractIdFromSlug = extractIdFromSlug
app.config.globalProperties.$removeStringFromFileLink = removeStringFromFileLink
app.config.globalProperties.$formatNumber = formatNumber
app.config.globalProperties.$extractFileName = extractFileName
app.mount('#app')
