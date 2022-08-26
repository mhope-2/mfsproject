<template>
  <div class="main">  
    <RouterView />
  </div>
</template>
<script>
    import {watch} from 'vue';
    import {useStore} from 'vuex';
    import { useRouter } from 'vue-router';
    export default {
      setup() {
          const store = useStore();
          const router = useRouter();

          watch(()=>store.getters.getToken,(token)=>{
            if(token){
              store.dispatch('getUserByToken',token);
            }
          })

          watch(()=>store.getters.getUser,(user)=>{
            if(user){
              //Persisting Route After Auth
              var previousRoute = localStorage.getItem('prevRT');
                //Check Previous Page
              if(previousRoute && previousRoute.length>1 && previousRoute != "undefined") router.push({name: previousRoute});
              else router.push({name:'shop'});
              }
          })
          return{}
      },
    }
</script>
