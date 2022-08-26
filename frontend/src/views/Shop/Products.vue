<template>
  <div class="p-4">
    <div class="mb-4">
      <input
        type="text"
        class="form-control form-control-sm"
        placeholder="Search Products"
        v-model="query"
      />
    </div>
    <button class="btn showCart" @click="changeDispState()">
      <span class="rounded-3" v-if="count>0">{{count}}</span>
      <h4 class="m-0">
        <i class="bi bi-bag-fill" v-if="!showCart"></i>
        <i class="bi bi-x-lg" v-else></i>
      </h4>
    </button>

    <div
      class="pagination mb-4 d-flex justify-content-end"
      v-if="products.length>1"
    >
      <button class="btn me-2 btn-sm" :disabled="page<=1">
        <i class="bi bi-chevron-left" @click="getNextProducts(page-1)"></i>
      </button>
      <button class="btn btn-sm" @click="getNextProducts(page+1)">
        <i class="bi bi-chevron-right"></i>
      </button>
    </div>
    <div class="row" v-if="products.length>1">
      <div
        v-for="(product,index) in products"
        :key="index"
        class="col-md-2 m-0"
      >
        <ProductCard :data="product" />
      </div>
    </div>
    <div class="text-center" v-else>
      <p>No Products to Display</p>
    </div>
    <div class="pagination d-flex justify-content-end" v-if="products.length>1">
      <button class="btn me-2 btn-sm" :disabled="page<=1">
        <i class="bi bi-chevron-left" @click="getNextProducts(page-1)"></i>
      </button>
      <button class="btn btn-sm" @click="getNextProducts(page+1)">
        <i class="bi bi-chevron-right"></i>
      </button>
    </div>
  </div>
  <Cart :showCart="showCart" />
</template>


<script>
import {ref,watch} from 'vue';
import {useStore} from 'vuex';
import ProductCard from '../../components/Products/ProductCard.vue';
import Cart from '../../components/Cart/Cart.vue';
import { search } from '../../composables/searchEngine';
export default {
    components:{
        ProductCard,
        Cart
    },
    setup() {
        const products = ref([]);
        const store = useStore();
        const page = ref(1);
        const count = ref(store.getters.getCart.length);
        const showCart = ref(false);
        const query = ref('')
        store.dispatch('getProducts',page.value);
        watch(()=>store.getters.getProducts,(newProducts)=>{
            products.value = newProducts;
        })
    //Cart Count
        watch(()=>[...store.getters.getCart],(newCart)=>{
            count.value = newCart.length;
        })
    //ShowCart
        watch(()=>store.getters.isCartShown,(dispState)=>{
            showCart.value = dispState;
        })
        const changeDispState = () =>{
            store.dispatch('showCart');
        }
        const getNextProducts = (newPage)=>{
            page.value = newPage;
            store.dispatch('getProducts',page.value);
        }
        //search
        watch(
        () => query.value,
        async (newQuery) => {
            if (newQuery.length >= 1) {
            products.value = await search(newQuery, store.getters.getProducts);
            if (products.value.length === 0) {
                store.dispatch("searchProduct", {
                keyword: newQuery,
                branch_id: 1,
                });
            }
            } else {
                products.value = store.getters.getProducts;
            }
        }
        );
        watch(
            () => store.getters.getSearchedProductData,
            (newSearchedProduct) => {
                products.value = newSearchedProduct;
            }
        );
        return {products,page,getNextProducts,count,showCart,changeDispState,query}
    },
}
</script>