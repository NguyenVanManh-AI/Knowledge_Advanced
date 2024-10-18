import { createRouter, createWebHistory } from 'vue-router'
import NProgress from 'nprogress';
import useEventBus from '@/composables/useEventBus'
const { emitEvent } = useEventBus();

// admin

// user 
import UserLogin from '@/components/user/auth/UserLogin'
import UserMain from '@/components/user/UserMain'
import ManageFolder from '@/components/user/manage-folder/ManageFolder'
import ManageFile from '@/components/user/manage-file/ManageFile'
import SearchPage from '@/components/user/chat/SearchPage'

// import ManageContent from '@/components/user/manage-content/ManageContent'
// import ManageBroadcast from '@/components/user/manage-broadcast/ManageBroadcast'
// import StatisticalChannel from '@/components/user/statistical-channel/StatisticalChannel'
// import RealtimeChat from '@/components/user/chat/RealtimeChat'

// home

// other 
import CommonNotFound from '@/components/common/CommonNotFound'

// middleware authUser
const authUser = (to, from, next) => {
    const user = localStorage.getItem('user');
    if (user) next();
    else {
        next({ name: 'UserLogin' });
        emitEvent('eventError', 'You need to login !');
    }
};

// // middleware authAdmin
// const authAdmin = (to, from, next) => {
//     const admin = localStorage.getItem('admin');
//     if (admin) next();
//     else {
//         next({ name: 'AdminLogin' });
//         emitEvent('eventError', 'You need to login !');
//     }
// };

// check user logged 
const loggedUser = (to, from, next) => {
    const user = localStorage.getItem('user');
    if (user) next({ name: 'ManageFile' });
    else next();
};

// // check amdin logged 
// const loggedAdmin = (to, from, next) => {
//     const user = localStorage.getItem('admin');
//     if (user) next({ name: 'ManageManager' });
//     else next();
// };

const routes = [

    { path: '/login', component: UserLogin, name: 'UserLogin', beforeEnter: loggedUser },
    // { path: '/reset-password', component: UserResetPassword, name: 'UserResetPassword', beforeEnter: loggedUser },
    {
        path: '/dashboard',
        component: UserMain,
        name: 'UserMain',
        beforeEnter: authUser,
        children: [
            { path: 'manage-folder', name: 'ManageFolder', component: ManageFolder },
            { path: 'manage-file', name: 'ManageFile', component: ManageFile },
            { path: 'search', name: 'SearchPage', component: SearchPage },
            // { path: 'manage-content', name: 'ManageContent', component: ManageContent },
            // { path: 'manage-broadcast', name: 'ManageBroadcast', component: ManageBroadcast },
            // { path: 'statistical-channel', name: 'StatisticalChannel', component: StatisticalChannel },
            // { path: 'realtime-chat/:id_to_user', name: 'RealtimeChat', component: RealtimeChat },
        ]
    },
    // {
    //     path: '/admin',
    //     component: AdminMain,
    //     name: 'AdminMain',
    //     children: [
    //         { path: 'login', name: 'AdminLogin', component: AdminLogin, beforeEnter: loggedAdmin },
    //         {
    //             path: '',
    //             name: 'AdminDashboard',
    //             component: AdminDashboard,
    //             beforeEnter: authAdmin,
    //             children: [{ path: 'manage-manager', name: 'ManageManager', component: ManageManager }]
    //         }
    //     ]
    // },
    { path: '/:CommonNotFound(.*)*', component: CommonNotFound, name: 'CommonNotFound' }
];

const router = createRouter({
    history: createWebHistory(),
    base: process.env.BASE_URL,
    routes: routes
})

router.beforeResolve((to, from, next) => {
    // Nếu đây không phải là lần tải trang đầu tiên.
    if (to.name) {
        // Bắt đầu thanh tiến trình tuyến đường.
        NProgress.start()
    }
    next()
})

router.afterEach(() => {
    // Hoàn thành hoạt ảnh của thanh tiến trình tuyến đường.
    NProgress.done()
})

export default router
