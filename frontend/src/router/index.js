import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [{
    path: "/",
    name: "FrontPage",
    component: () =>
      import( /* webpackChunkName: "FrontPage" */ "../views/FrontPage.vue")
  },
  {
    path: "/register",
    name: "register",
    component: () =>
      import( /* webpackChunkName: "Register" */ "../views/Register.vue")
  },
  {
    path: '/profiles/create',
    name: 'AddUserProfile',
    component: () => import( /* webpackChunkName: "AddUserProfile" */ '../views/AddUserProfile.vue')
  },
  {
    path: '/profiles/:id',
    name: 'UserProfile',
    component: () => import( /* webpackChunkName: "UserDetail" */ '../views/UserProfile.vue')

  },
  {
    path: '/profiles/:id/update',
    name: 'UpdateUserProfile',
    component: () => import( /* webpackChunkName: "UpdateUserProfile" */ '../views/UpdateUserProfile.vue')
  },

];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  if (to.fullPath == "/register") {
    if (!localStorage.getItem("token")) {
      next();
    } else {
      next("/");
    }
  } else if (to.path == '/') {
    next()
  } else {
    if (!localStorage.getItem("token")) {
      next("/register");
    } else {
      next();
    }
  }
});

export default router;