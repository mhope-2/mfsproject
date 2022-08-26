import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue';
import store from '../store/index';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/shop',
      name: 'shop',
      meta:{auth:true},
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Shop.vue'),
      redirect:'/shop/products',
      children:[
        {
        path:'/shop/cart',
        name:'cart',
        meta:{auth:true},
        component:()=>import('../views/Shop/Products.vue')
        },
        {
          path:'/shop/invoice',
          name:'invoice',
          meta:{auth:true},
          component:()=>import('../views/Shop/Invoice.vue')
        },
        {
          path:'/shop/products',
          name:'products',
          meta:{auth:true},
          component:()=>import('../views/Shop/Products.vue')
        },
        {
          path: '/shop/invoices',
          name: 'invoices',
          meta:{auth:true},
          component: ()=>import('../views/Shop/Invoices.vue')
        },
        {
          path: '/shop/customers',
          name: 'customers',
          meta:{auth:true},
          component: ()=>import('../views/Shop/Customers.vue')
        },
        {
          path: '/shop/print',
          name: 'printInvoice',
          meta:{auth:true},
          component: ()=>import('../views/Shop/PrintInvoice.vue')
        },
        {
          path: '/shop/quotations',
          name: 'quotations',
          meta:{auth:true},
          component: ()=>import('../views/Shop/Quotations.vue')
        },
        {
          path: '/shop/inventory',
          name: 'inventory',
          meta:{auth:true},
          component: ()=>import('../views/Shop/Inventory.vue')
        },
        {
          path: '/users',
          name: 'users',
          meta:{auth:true},
          component: ()=>import('../views/Users.vue')
        }
      ]
    },
  ]
})


router.beforeEach(async(to,from,next)=>{
  const user = await store.getters.getUser;
  if (to.name !== 'login' && !user) next({ name: 'login' })
  else{
    if(to.name !== 'login') localStorage.setItem('prevRT',to.name)
    next()
  }
  
})

export default router;