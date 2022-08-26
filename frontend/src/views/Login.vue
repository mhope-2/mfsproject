<template>
  <div class="row h-100 w-100">
        <div class="col-md-5 p-5 hero">
          <h5>mfs project</h5>
        </div>
        <div class="p-5 col-md-7 d-flex justify-content-center align-items-center">
            <form @submit.prevent="login" class="w-50">
                <div class="pb-3">
                  <h4>Login</h4>
                  <p class="text-secondary"><small>User Authentication</small></p>
                </div>
                <div class="my-4">
                    <label for="" class="mb-3">Username</label>
                    <input class="form-control" type="text" placeholder="Username" v-model="username" aria-label=".form-control-sm example"/>
                </div>
                <div class="mb-4">
                    <label for="" class="mb-3">Password</label>
                    <input class="form-control" type="password" placeholder="Password" v-model="pass" aria-label=".form-control-sm example"/>
                </div>
                <div>
                    <button class="btn btn w-100"><i class="bi bi-shield-lock-fill"></i> Login</button>
                </div>
            </form>
        </div>
  </div>
</template>

<script>
import {ref,onBeforeMount} from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";

export default {
  components: {

  },
  setup() {
        //Import Router
        const router = useRouter();
        
        //Import Vuex Store
        const store = useStore();

        //Username and Password
        const username = ref("");
        const pass = ref("");

        const login = async () => {
          store.dispatch('authenticate',{username:username.value,password:pass.value});

          // if (localStorage.getItem("prevRT") && localStorage.getItem("prevRT") !== "undefined") {
          //   router.push({ name: localStorage.getItem("prevRT") });
          // } else {
          //   router.push({ name: "shop" });
          // }
        };

      onBeforeMount(()=>{
        const token = localStorage.getItem('key');
        store.dispatch('getUserByToken',token);
      })

    return {
      username,
      pass,
      login,
    };
  },
};
</script>
