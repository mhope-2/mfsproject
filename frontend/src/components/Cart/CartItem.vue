<template>
        <div>
             <div class="cartItem mb-4 py-4  bg-white rounded">
                  <div class="row item px-4">
                    <div class="col-md-5 m-0">
                      <!-- <small>Product Name</small>
                      <br /> -->
                      <p class="m-0"
                        ><b>{{ data.item.name }}</b>
                      </p>
                    </div>

                    <div class="col-md-2 px-4 m-0 text-center">
                      <!-- <small>Quantity</small> -->
                      <input
                        type="number"
                        :min="1"
                        :max="
                          parseInt(data.item.quantity) -
                            parseInt(data.item.alert_quantity||5)
                        "
                        v-model="data.quantity"
                        @input="(event) => changeQuantity(event, data.item.id)"
                        class="form-control quantity"
                      />
                    </div>

                    <div class="col-md-2 p-0 text-center">
                      <!-- <small>Price</small>
                      <br /> -->
                      <p class="m-0">
                        <b>{{ parseFloat(data.item.unit_price).toFixed(2) }}</b>
                      </p>
                    </div>

                    <div class="col-md-2 p-0 text-center">
                      <!-- <small>Line Total</small>
                      <br /> -->
                      <p class="m-0">
                        <b>{{
                          (parseFloat(data.item.unit_price) * parseFloat(data.quantity)).toFixed(2)
                        }}</b>
                      </p>
                    </div>
                    <div class="col-md-1">
                      <button class="btn btn-sm" @click="removeFromCart(data.item)">
                        <i class="bi bi-x"></i>
                      </button>
                    </div>
                  </div>
                </div>
        </div>
</template>
<script>
import { toRefs, ref } from "vue";
import { useStore } from "vuex";

export default {
  props: {
    data: Object,
  },
  setup(props) {
    const { data } = toRefs(props);
    const total = ref();

    const store = useStore();
    const removeFromCart = (item) => {
      store.dispatch("removeFromCart", { item: item });
    };

    const changeQuantity = (event, id) => {
      if (event.target.value > props.data.item.branch_1_stock) {
        return (
          (props.data.quantity = props.data.item.branch_1_stock)
        );
      } else {
        store.dispatch("changeQuantity", { value: event.target.value, id });
        store.dispatch("calcTotal");
      }
    };

    return { data, removeFromCart, changeQuantity, total };
  },
};
</script>
