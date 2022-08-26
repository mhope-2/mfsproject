<template>
    <div>
        <Navbar/>
        <RouterView/>
    </div>
</template>
<script>
import Navbar from '../components/Navbar/Navbar.vue';
export default {
    components:{
        Navbar
    },
    setup() {
        
    },
}
</script>