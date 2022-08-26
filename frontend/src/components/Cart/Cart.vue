<template>
  <div class="cart p-5 row" :style="{left:(showCart)?'0%':'100%'}">
    <div class="col-md-8 pe-5 border-end">
        <div class="w-100 d-flex justify-content-between">
          <h2 class="d-inline">Cart</h2>
          <button v-on:click="clearCart()" class="btn btn-sm">
            <i class="bi bi-trash3"></i>
          </button>
        </div>
        <div class="row  headers px-4 my-4">
          <small class="col-md-5">Product Name</small>
          <small class="col-md-2 text-center">Quantity</small>
          <small class="col-md-2 text-center">Price</small>
          <small class="col-md-2 text-center">Line Total</small>
          <small class="col-md-1"></small>
        </div>
    
        <div class="cartItems">
          <div v-if="cartItems.length >= 1">
            <div v-for="item in cartItems" :key="item.id">
              <CartItem :data="item" />
            </div>
          </div>
          <div v-else class="text-center">
            <p>Cart is Empty</p>
          </div>
        </div>
    </div>
    <div class="col-md-4 p-5">
      <div v-if="cartItems.length >= 1">
        <div>
          <p class="m-0">Total:</p>
          <h2 class="mb-3"><small>GHs </small>{{ total.toFixed(2) }}</h2>
        </div>
        <button class="cbtn-alt btn btn-block mx-auto" @click="proceedCheckout()">
          Proceed
        </button>
      </div>
      <div v-else>
        <button class="cbtn-alt btn btn-block mx-auto" disabled>Proceed</button>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref, toRefs, watch } from "vue";
import { useStore } from "vuex";
import CartItem from "./CartItem.vue";
import { useRouter } from 'vue-router';

export default {
  components: {
    CartItem,
  },
  props:{
    showCart:Boolean
  },
  setup(props) {
    const store = useStore();
    const cartItems = ref();
    const total = ref();
    const {showCart} = toRefs(props)
    const router = useRouter()

    cartItems.value = store.getters.getCart;
    total.value = store.getters.getTotal.total;

    watch(
      () => [...cartItems.value],
      (cartItems, prevCartItems) => {
        store.dispatch("calcTotal").then(() => {});
      }
    );

    watch(
      () => store.getters.getTotal,
      (newTotal) => {
        total.value = newTotal.total;
      }
    );
    
    watch(
      () => store.getters.getCart,
      (newCart) => {
        cartItems.value = newCart;
      }
    );

    //clear cart
    const clearCart = () => {
      store.dispatch("clearCart");
      
      //Clear Set quote To Invoice;
      store.dispatch('clearSetQuoteInvoice');
      
      cartItems.value = store.getters.getCart;
    };


    //Proceed to Checkout
    const proceedCheckout=()=>{
        router.push('invoice');
        store.dispatch('showCart');
    }



    return { cartItems, clearCart, total, proceedCheckout,showCart};
  },
};
</script>
