<template>
<div class="modal fade" id="editProductForm" tabindex="-1">
  <div class="modal-dialog modal-xl">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Edit Product</h5>
        <button type="button" class="btn btn-sm" data-bs-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <div class="container p-5">

        <form @submit.prevent="updateProduct()">
                <div class="row ">
                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="productName">Product Name</label>
                  <input type="text" class="form-control" v-model="name" placeholder="Product Name" required />
                </div>
                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="productDesc">Product Description</label>
                  <input type="text" class="form-control" v-model="product_description" placeholder="Product Description" required />
                </div>

               <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Barcode</label>
                  <input type="text" class="form-control" v-model="barcode" placeholder="Barcode" required />
                </div>

                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Brand</label>
                  <input type="text" class="form-control" v-model="brand" placeholder="Brand" />
                </div>

                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Unit</label>
                  <select class="form-control" v-model="unit" required>
                    <option value="PK">Pack</option>
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
import{ref,toRefs,watch,onMounted} from 'vue';
import {useStore} from 'vuex'
import {useRoute} from "vue-router";
import {Modal} from 'bootstrap';
export default {
  props:{
    product:Object
  },
  setup(props) {
    const toEdit = ref('');
    const {product} = toRefs(props)
    const name = ref();
    const brand= ref();
    const unit = ref();
    const barcode = ref();
    const description = ref();
    const cost = ref();
    const unit_price = ref();
    const quantity = ref();
    let editProduct;
    const store = useStore();
    const route = useRoute();
    
    onMounted(()=>{editProduct = new Modal('#editProductForm',{keyboard:false})});
    watch(()=>product.value,(newProduct)=>{
      toEdit.value = newProduct;
      barcode.value  = newProduct.barcode ;
      brand.value  = newProduct.brand ;
      name.value  = newProduct.name;
      description.value = newProduct.description;
      unit_price.value  = newProduct.unit_price ;
      unit.value =  newProduct.unit;
      quantity.value = newProduct.quantity;
    })
    
    const updateProduct= (e)=>{
          const product = {
          "name" :name.value ,
          "brand" :brand.value,
          "unit" : unit.value,
          "barcode" :barcode.value,
          "unit_price" :unit_price.value,
          "quantity": quantity.value,
          "description": description.value,      
    }
    
  store.dispatch('updateProduct',{product,id:toEdit.value.id}).then(()=>{
       editProduct.hide()
      store.dispatch("getProducts",1);
  });
  
}
    return {
              barcode,
              quantity,
              brand,
              name,
              description,
              unit_price,
              unit,
              updateProduct
    }
  },
}
</script>