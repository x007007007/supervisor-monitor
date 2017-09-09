import Vue from 'vue'
import Router from 'vue-router'
import VueI18n from 'vue-i18n'

import Index from '@/pages/index'

Vue.use(VueI18n)
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    }
  ]
})
