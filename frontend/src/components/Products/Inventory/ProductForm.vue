<template>
  <div class="modal fade" id="productForm" tabindex="-1">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Product Form</h5>
          <button type="button" class="btn btn-sm" data-bs-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="container p-5">
            <form @submit.prevent="createProduct">
               <div class="row ">
                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="productName">Product Name</label>
                  <input type="text" class="form-control" v-model="name" placeholder="Product Name" required />
                </div>
                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="productDesc">Product Description</label>
                  <input type="text" class="form-control" v-model="description" placeholder="Product Description" required />
                </div>
              
               <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Barcode</label>
                  <input type="text" class="form-control" v-model="barcode" placeholder="Barcode"  />
                </div>

                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Brand</label>
                  <input type="text" class="form-control" v-model="brand" placeholder="Brand" />
                </div>

                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Unit Price</label>
                  <input type="text" class="form-control" v-model="unit_price" placeholder="Unit Price" />
                </div>

                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Quantity</label>
                  <input type="text" class="form-control" v-model="quantity" placeholder="Quantity" />
                </div>

                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Unit</label>
                  <select class="form-control" v-model="unit" required>
                    <option value="PCK">Pack</option>
                    <option value="PCS">Pieces</option>
                  </select>
                </div>
              </div>

              <div class="modal-footer">
                <button type="button" class="btn cbtn" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn cbtn-alt">Save changes</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { onMounted, ref, toRefs, watch } from "vue";
import { useStore } from "vuex";
import {useRoute} from "vue-router";
import {Modal} from 'bootstrap';
export default {
  props:{
    page:Number
  },
  setup(props) {
    const {page} = toRefs(props)
    const name = ref();
    const brand= ref();
    const unit = ref();
    const barcode = ref();
    const description = ref();
    const unit_price = ref();
    const quantity = ref();
    const store = useStore();
    const route = useRoute();
    let productForm;
    onMounted(()=>{productForm = new Modal('#productForm',{keyboard:false})});
    const createProduct = () => {
      const product = {
          "name": name.value ,
          "brand": brand.value,
          "unit" : unit.value,
          "barcode": barcode.value,
          "description": description.value,
          "unit_price" :unit_price.value,
          "quantity": quantity.value,
      };
      store.dispatch("createProduct", product ).then(() => {
        productForm.hide()
        store.dispatch("getProducts", page.value);
      });
    };
    return {
              name,
              quantity,
              brand,
              barcode,
              description,
              unit_price,
              unit,
      createProduct,
    };
  },
};
</script>