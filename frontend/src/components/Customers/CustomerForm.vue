<template>
  <div class="modal fade" id="customerForm" tabindex="-1">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit Customer</h5>
          <button
            type="button"
            class="btn btn-sm"
            data-bs-dismiss="modal"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="container">
            <form @submit.prevent="createCustomer">
              <div class="row">
                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">First Name</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="first_name"
                    placeholder="First Name"
                    required
                  />
                </div>

                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Middle Name</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="middle_name"
                    placeholder="Middle Name"
                  />
                </div>
                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Last Name</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="last_name"
                    placeholder="Last Name"
                  />
                </div>

                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Phone Number</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="phone"
                    placeholder="Phone Number"
                  />
                </div>

                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="productCodeType">Email</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="email"
                    placeholder="Email"
                  />
                </div>

                <div class="col-md-4 pb-4 pb-md-5">
                  <label for="">Address</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="address"
                    placeholder="Address"
                  />
                </div>

              </div>
              <div class="modal-footer">
                <button type="button" class="btn cbtn" data-bs-dismiss="modal">
                  Close
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
import { onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import {Modal} from 'bootstrap';

export default {
  setup() {
    const store = useStore();
    const first_name = ref();
    const middle_name = ref();
    const last_name = ref();
    const phone = ref();
    const email = ref();
    const address = ref();
    const customer_code = ref();
    let modal;

    onMounted(()=>{modal = new Modal('#customerForm',{keyboard:false})})

    const createCustomer = () => {
      let body = {
        first_name: first_name.value,
        middle_name: middle_name.value,
        last_name: last_name.value,
        phone: phone.value,
        email: email.value,
        address: address.value,
      };

      store.dispatch("createCustomer", body).then(() => {
        store.dispatch("getCustomers");
        modal.hide();
      });
    };

    return {
      first_name,
      middle_name,
      last_name,
      phone,
      email,
      address,
      createCustomer,
    };
  },
};
</script>
