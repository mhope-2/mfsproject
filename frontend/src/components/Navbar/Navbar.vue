<template>
    <nav class="navbar navbar-expand-lg px-4">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">mfs project</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item mx-2">
                    <router-link to="/shop/products" class="nav-link"><i class="bi bi-bag-check-fill"></i> Shop</router-link>
                </li>
                <li class="nav-item mx-2">
                     <router-link to="/shop/invoices" class="nav-link"><i class="bi bi-file-earmark-spreadsheet-fill"></i> Invoices</router-link>
                </li>
                <li class="nav-item mx-2">
                     <router-link to="/shop/customers" class="nav-link"><i class="bi bi-person-heart"></i> Customers</router-link>
                </li>
                 <li class="nav-item mx-2">
                     <router-link to="/shop/inventory" class="nav-link"><i class="bi bi-box-seam-fill"></i> Inventory</router-link>
                </li>
                <li class="nav-item dropdown">
                <a class="nav-link" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <UserIcon/>
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><router-link class="dropdown-item" href="#" to="/users">Settings</router-link></li>
                    <li><a class="dropdown-item" href="/">Logout</a></li>
                </ul>
                </li>
            </ul>
            </div>
        </div>
    </nav>
</template>
<script>
import UserIcon from './UserIcon.vue';
export default {
    components:{
        UserIcon
    },
    setup() {
        
    },
}
</script>