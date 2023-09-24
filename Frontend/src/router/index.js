import HomePage from "../components/HomePage.vue";
import Login from "../components/LoginPage.vue";
import CreateAccount from '../components/CreateAccount.vue';
import UserDashboard from '../components/UserDashboard.vue';
import AdminLogin from "../components/AdminLogin.vue";
import AdminDashboard from "../components/AdminDashboard.vue";
import AdminVenues from "../components/AdminVenues.vue";
import AdminShows from "../components/AdminShows.vue";
import AddVenue from "../components/AddVenue.vue";
import ModifyVenue from "../components/ModifyVenue.vue";
import AddShow from "../components/AddShow.vue";
import AddHostingVenue from "../components/AddHostingVenue.vue";
import AdminHostingVenues from "../components/AdminHostingVenues.vue";
import ModifyShow from "../components/ModifyShow.vue";
import ModifyHostingVenue from "../components/ModifyHostingVenue.vue";
import SearchResults from "../components/SearchResults.vue";
import VenueHomePage from "../components/VenueHomePage.vue";
import BookTicket from "../components/BookTicket.vue";
import ConfirmBooking from "../components/ConfirmBooking.vue";

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  base: '/',
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/search/:keyword',
      name: 'search',
      component: SearchResults
    },
    {
      path: '/venues/:name',
      name: 'venueHomePage',
      component: VenueHomePage
    },
    {
      path: '/user/login',
      name: 'userLogin',
      component: Login
    },
    {
      path: '/user/create',
      name: 'createAccount',
      component: CreateAccount
    },
    {
      path: '/user/dashboard',
      name: 'userDashboard',
      component: UserDashboard
    },
    {
      path: '/book_ticket/:showName/',
      component: BookTicket,
      beforeEnter: (to, from, next) => {
        if(sessionStorage.email){
          next();
        }
        else {
          next({name: 'userLogin'});
        }
      },
    },
    {
      path: '/book_ticket/:showName/:date/:hostedShowId',
      component: ConfirmBooking,
      beforeEnter: (to, from, next) => {
        if(sessionStorage.email){
          next();
        }
        else {
          next({name: 'userLogin'});
        }
      },
    },
    {
      path: '/admin/login',
      name: 'adminLogin',
      component: AdminLogin
    },
    {
      path: '/admin/dashboard',
      component: AdminDashboard,
      beforeEnter: (to, from) => {
        if(sessionStorage.roles.includes('admin')){
          return true
        }
        else {
          return false
        }
      },
      children: [
        {
          path: 'venues',
          name: 'adminVenues',
          component: AdminVenues
        },
        {
          path: 'shows',
          name: 'adminShows',
          component: AdminShows
        },
        {
          path: 'venues/create',
          name: 'addVenue',
          component: AddVenue
        },
        {
          path: 'venues/:id/modify',
          name: ' modifyVenue',
          component: ModifyVenue
        },
        {
          path: 'shows/create',
          name: 'addShow',
          component: AddShow
        },
        {
          path: 'shows/:id/modify',
          name: 'modifyShow',
          component: ModifyShow
        },
        {
          path: 'shows/:id/add_venue',
          name: 'addHostingVenue',
          component: AddHostingVenue
        },
        {
          path: 'shows/:id/venues',
          name: 'adminHostingVenue',
          component: AdminHostingVenues
        },
        {
          path: 'shows/:id/modify_venue',
          name: 'modifyHostingVenue',
          component: ModifyHostingVenue
        }
      ]
    }
  ]
})


export default router
