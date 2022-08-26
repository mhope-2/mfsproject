<template>
  <!-- Modal -->
  <div class="modal fade" id="editCustomer" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="editCustomerLabel">Edit Customer</h5>
          <button type="button" class="btn btn-sm" data-bs-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        </div>
        <div class="modal-body">
             <div class="container">
    <h1 class="mb-5 pt-5">Edit Customer</h1>
            <form @submit.prevent="updateCustomer">
              <div class="row">
                <div class="col-4 pb-5">
                  <label for="">First Name</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="first_name"
                    placeholder="First Name"
                  />
                </div>
                <div class="col-4 pb-5">
                  <label for="">Middle Name</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="middle_name"
                    placeholder="Middle Name"
                  />
                </div>
                <div class="col-4 pb-5">
                  <label for="">Last Name</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="last_name"
                    placeholder="Last Name"
                  />
                </div>
                <div class="col-4 pb-5">
                  <label for="">Phone Number</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="phone"
                    placeholder="Phone Number"
                  />
                </div>

                <div class="col-4 pb-5">
                  <label for="productCodeType">Email</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="email"
                    placeholder="Email"
                  />
                </div>

                <div class="col-4 pb-5">
                  <label for="">Address</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="address"
                    placeholder="Address"
                  />
                </div>

                <div class="col-4 pb-5">
                  <label for="">Customer Code</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="customer_code"
                    placeholder="Customer Code"
                  />
                </div>

                <div class="col pb-5">
                  <label for="">Description</label>
                  <textarea
                    cols="30"
                    type="text"
                    v-model="description"
                    class="form-control"
                    placeholder="Description"
                  />
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn cbtn" data-bs-dismiss="modal">
                  Cancel
                </button>
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
import {Modal} from 'bootstrap';
export default {
  props:{
    customer:Object
  },
  setup(props) {
    const store = useStore();
    const {customer} = toRefs(props);
    const first_name = ref();
    const middle_name = ref();
    const last_name = ref();
    const phone = ref();
    const email = ref();
    const address = ref();
    const customer_code = ref();
    const description = ref();
    let editModal;

    onMounted(()=>{editModal=new Modal('#editCustomer',{keyboard:false})});


    watch(()=>customer.value,(newCustomer)=>{
      if(newCustomer.first_name !== (undefined || null)){
        customer.value = newCustomer;
        first_name.value = customer.value.first_name,
        middle_name.value = customer.value.middle_name,
        last_name.value = customer.value.last_name,
        phone.value = customer.value.phone,
        email.value = customer.value.email,
        address.value = customer.value.address,
        customer_code.value = customer.value.customer_code,
        description.value = customer.value.description;
      }
    })



    const updateCustomer = () => {
      let body = {
        first_name: first_name.value,
        middle_name: middle_name.value,
        last_name: last_name.value,
        phone: phone.value,
        email: email.value,
        address: address.value,
        credit_limit: credit_limit.value,
        customer_code: customer_code.value,
        description: description.value,
      };

      store
        .dispatch("updateCustomer", {
          id: customer.value.id,
          body,
        })
        .then(() => {
          editModal.hide()
          store.dispatch("getCustomers");
        });
    };


    return {
      first_name,
      middle_name,
      last_name,
      phone,
      email,
      address,
      description,
      updateCustomer,
      customer,
    };
  },
};
</script>
