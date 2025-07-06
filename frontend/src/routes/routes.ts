import LoginFormVue from '@/auth/LoginForm.vue'
import RegisterFormVue from '@/auth/RegisterForm.vue'
import JobListVue from '@/jobs/JobList.vue'
import MyJobsLikedVue from '@/jobs/MyJobsLiked.vue'
import MyJobsSeenVue from '@/jobs/MyJobsSeen.vue'
import HomeViewVue from '@/pages/HomeView.vue'
import type { RouteRecordRaw } from 'vue-router'
import AccountPage from '../pages/AccountPage.vue'
import MyJobsAppliedVue from '../jobs/MyJobsApplied.vue'
import JobDetails from '../jobs/JobDetails.vue'
import ForgotPassword from '../auth/ForgotPassword.vue'
import ResetPassword from '../auth/ResetPassword.vue'
import MyJobsView from '../jobs/MyJobsView.vue'
import About from '@/pages/About.vue'

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: HomeViewVue,
  },
  {
    path: '/about',
    name: 'about',
    component: About,
  },
  {
    path: '/login',
    component: LoginFormVue,
    props: true,
  },
  {
    path: '/register',
    component: RegisterFormVue,
    props: true,
  },
  {
    path: '/account',
    component: AccountPage,
    props: true,
  },
  {
    path: '/forgot',
    component: ForgotPassword,
    props: true,
  },
  {
    path: '/auth/reset-password',
    component: ResetPassword,
    props: true,
  },
  {
    path: '/offers',
    component: JobListVue,
    props: true,
  },
  {
    path: '/jobDetails/:jobId',
    component: JobDetails,
    props: true,
  },
  {
    path: '/myJobs',
    component: MyJobsView,
    props: true,
    children: [
      {
        path: 'liked',
        name: 'myJobsLiked',
        component: MyJobsLikedVue,
      },
      {
        path: 'seen',
        name: 'myJobsSeen',
        component: MyJobsSeenVue,
      },
      {
        path: 'applied',
        name: 'myJobsApplied',
        component: MyJobsAppliedVue,
      },
    ],
  },
]
