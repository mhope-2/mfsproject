<template>
    <span class="text-uppercase userIcon rounded-3">{{user.first_name.charAt(0)}}</span>
</template>
<script>
import {ref,watch} from 'vue';
import {useStore} from 'vuex';
export default {
    setup() {
        const store = useStore();
        const user = ref(store.getters.getUser);


        watch(()=>store.getters.getUser,(newUser)=>{
            user.value = newUser;
            console.log(user.value)
        })

        return {user}
    },
}
</script>