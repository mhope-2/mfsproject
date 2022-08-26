<template>
  <div class="p-2" @click="addToCart(data)">
    <div
      class="card rounded-4 p-4"
      :class="{'lowCard':parseInt(data.quantity)<= parseInt(25) && parseInt(data.quantity) > parseInt(data.alert_quantity||5),'outCard':parseInt(data.quantity)<=parseInt(data.alert_quantity||5)}"
    >
      <div class="row mb-3">
        <div class="col">
          <div
            class="pb-2"
            v-if="parseInt(data.quantity) >= parseInt(data.alert_quantity || 5)"
            data-toggle="tooltip"
            data-placement="top"
            title="Instock"
          >

            <i class="bi bi-award"></i>
          </div> 
          <div class="pb-2" v-else>
            <i class="bi bi-exclamation-diamond"></i>
          </div>
        </div>
        <div class="col text-end unit">
          <span>{{ data.unit }}</span>
        </div>
      </div>

      <small class="name">{{ data.barcode }}</small>
      <h5 class="mt-2">{{ data.name }}</h5>
      <div class="d-flex justify-content-between mt-3">
        <small class="price m-0"> GHS {{ parseFloat(data.unit_price).toFixed(2) }} </small>
      </div>
    </div>
  </div>
</template>
<script>
import { toRefs } from "vue";
import { useStore } from "vuex";
export default {
  props: {
    data: Object,
  },
  setup(props) {
    const { data } = toRefs(props);
    const store = useStore();
    
        //Add To Cart
    const addToCart = async (item) => {
      if (item.quantity <= item.alert_quantity) {
        toast.warning(`${item.name} is out of stock`);
      } else {
        store.dispatch("addToCart", item);
      }
    };

    return { data, addToCart };
  },
};
</script>
