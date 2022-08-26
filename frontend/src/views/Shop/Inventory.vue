<template>
  <div class="p-5 inventory page">


    <ProductForm />
    <EditProduct :product="sProduct"/>
    <!--<BulkImport />-->


    <button
      v-if="selected && selected.length >= 1"
      class="btn cbtn deleteSelected"
      @click="deleteProducts()"
    >
      <span>{{ selected.length }}</span>
      <i class="uil uil-trash-alt"></i>
    </button>

    <div class="row mt-2 mb-4">
      <div class="col btn-cluster text-end">
        <button
          class="btn cbtn me-3"
          data-bs-toggle="modal"
          data-bs-target="#productForm"
        >
          <i class="bi bi-plus"></i> Add Product
        </button>


      </div>
    </div>


    <div class="mt-3 mb-3">
      <input
        type="text"
        class="form-control"
        v-model="query"
        placeholder="Search Products"
      />
    </div>

        <div class="pagination d-flex justify-content-end" v-if="products.length>1">
            <button class="btn me-2 btn-sm" :disabled="page<=1"><i class="bi bi-chevron-left" @click="getNextProducts(page-1)"></i></button>
            <button class="btn btn-sm" @click="getNextProducts(page+1)"><i class="bi bi-chevron-right"></i></button>
        </div>

    <div
      class="mt-5 inProducts table-res"
      v-if="products && products.length >= 1"
    >
      <table class="table table-borderless quote-table pt-5">
        <thead>
                    <tr class="border-bottom">
                        <th></th>
                        <th scope="col mx-3" readonly></th>
                        <th scope="col">Product Name</th>
                        <th scope="col">Price Per Unit</th>
                        <th scope="col">Unit Type</th>
                        <th scope="col">Bar Code</th>
                        <th scope="col">In Stock</th>
                        <th></th>
                    </tr>
                    </thead>

                    <tbody class="quote-semi-table">
                    <tr class="py-5 border-bottom" v-for="(item, index) in products" :key="index" :class="{'table-warning':parseInt(item.quantity)<= parseInt(25) && parseInt(item.quantity) > parseInt(item.alert_quantity||5),'table-danger':parseInt(item.quantity)<=parseInt(item.alert_quantity||5)}">
                    <th class="py-4">
                        <div class="">
                        <i class="uil uil-exclamation-circle" v-if="parseInt(item.quantity)<= parseInt(item.alert_quantity||5)" title="Out Stock"></i>
                        <i class="uil uil-arrow-circle-down" v-else-if="parseInt(item.quantity)<= parseInt(25) && parseInt(item.quantity) > parseInt(item.alert_quantity||5)" title="Low Stock"></i>
                        </div>
                    </th>
                    <th class="mt-1">
                    <input
                        type="checkbox"
                        :value="item.id"
                        v-model="selectedItems"
                        class="mt-4 mx-3"
                    />
                    </th>
                    <th class="py-4 col-md-4">
                    <p class="mt-2">
                        {{ item.name }}
                    </p>
                    </th>

                    <td class="py-4">
                    <p class="price">GHS {{ parseFloat(item.unit_price).toFixed(2) }}</p>
                    </td>

                    <td class="py-4">
                    <p>
                        {{ item.unit }}
                    </p>
                    </td>
                    <td class="py-4">
                    <p>
                        {{ item.barcode }}
                    </p>
                    </td>

                    <td class="py-4">
                    <p>{{ item.quantity }}</p>
                    </td>

                    <td>
                    <div
                        class="
                        mt-2
                        d-flex
                        flex-row
                        justify-content-center
                        align-items-center
                        actions
                        "
                    >
                        <span class=" btn btn-sm p-2 me-2"
                            data-bs-toggle="modal"
                            data-bs-target="#editProductForm"
                            @click="setEdit(item)"
                        ><i class="bi bi-pencil-square"></i></span>
                        <span class="btn btn-sm p-2"
                        @click="deleteProduct(item.id)"><i class="bi bi-trash3" ></i></span>
                    </div>
                    </td>
                </tr>
        </tbody>
      </table>
    </div>

    <div v-else-if="products.length <= 0" class="p-5 text-center">
      <h2><i class="uil uil-silent-squint"></i></h2>
      <p><small>No Product To Show </small></p>
    </div>

    <div class="pagination d-flex justify-content-end" v-if="products.length>1">
            <button class="btn me-2 btn-sm" :disabled="page<=1"><i class="bi bi-chevron-left" @click="getNextProducts(page-1)"></i></button>
            <button class="btn btn-sm" @click="getNextProducts(page+1)"><i class="bi bi-chevron-right"></i></button>
    </div>

  </div>
</template>
<script>
import ProductForm from "../../components/Products/Inventory/ProductForm.vue";
// import BulkImport from "../../components/Products/Inventory/BulkImport.vue";
import { ref, watch } from "vue";
import { useStore } from "vuex";
import EditProduct from "../../components/Products/Inventory/EditProduct.vue";
// import { search } from "../../composables/searchEngine";
import { useRoute } from "vue-router";
import Swal from "sweetalert2";
export default {
  components: {
    ProductForm,
    // BulkImport,
    EditProduct
  },
  setup() {
    const store = useStore();
    const products = ref([]);
    const query = ref("");
    const route = useRoute();
    const selected = ref();
    const selectedItems = ref([]);
    const page = ref(1);
    const sProduct = ref();
    //Get All Products
    store.dispatch('getProducts',page.value)
    watch(
      () => store.getters.getSelectedDelete,
      (newItems) => {
        selected.value = newItems;
      }
    );
    
    const deleteProducts = () => {
      if (selected.value.length >= 1) {
        Swal.fire({
          title: "Do you want to Delete Selected Products?",
          showCancelButton: true,
          confirmButtonText: "Proceed",
        }).then((result) => {
          /* Read more about isConfirmed, isDenied below */
          if (result.isConfirmed) {
            store
              .dispatch("deleteSelectedProduct", {
                product: selected.value,
              })
              .then(() => {
                selected.value = "";
                store.dispatch("getProductsByBranch", page.value);
              });
          } else {
          }
        });
      }
    };
    watch(
      () => store.getters.getProducts,
      (newProducts) => {
        products.value = newProducts;
      }
    );
    //Goto
    const goTo = (pageNumber) => {
      store.dispatch("getProductsByBranch", {
        page: pageNumber,
        branch_id:1
      });
    };
    //Search Quotes
    watch(
      () => query.value,
      (newQuery) => {
        if (newQuery.length >= 1) {
          products.value = search(newQuery, store.getters.getProducts);
          if (products.value.length === 0) {
            store.dispatch("searchProduct", {
              keyword: newQuery,
              branch_id: 1
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
    watch(()=>selectedItems.value,(newItems)=>{
        console.log(newItems)
    })
    const setEdit = (item)=>{
            sProduct.value = item;
    }
    const deleteProduct = (id) =>{
                     Swal.fire({
              title: 'Do you want to Delete this Product?',
              showCancelButton: true,
              confirmButtonText: 'Proceed',
            }).then((result) => {
              /* Read more about isConfirmed, isDenied below */
              if (result.isConfirmed) {
                  store.dispatch("deleteProduct", {
                    id: id,
                    branch_id: 1,
                  }).then(()=>{
                  store
                  .dispatch("getProducts",page.value)
                  });
                Swal.fire('Product Deleted Successfully!', '', 'success')
              } else{
              }
            })
    }
    
    const getNextProducts = (newPage)=>{
            page.value = newPage;
            store.dispatch('getProducts',page.value);
        }
    return {
      products,
      goTo,
      query,
      selectedItems,
      deleteProducts,
      selected,
      sProduct,
      setEdit,
      deleteProduct,
      page,
      getNextProducts
    };
  },
};
</script>
