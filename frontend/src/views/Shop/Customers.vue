<template>
  <div class="p-5 page customers">
    <div class="tab-content" id="nav-tabContent">
      <div>
        <div class="text-end mb-4">
          <button class="btn btn-sm" data-bs-toggle="modal" data-bs-target="#customerForm">Add Customer</button>
        </div>
        <div>
          <input
            type="text"
            class="form-control"
            placeholder="Enter Customer Name ..."
            v-model="query"
          />
        </div>
        <div b v-if="customers" class="mt-4">
                <table class="table  pt-5">
                    <thead class="header">
                        <tr class="border-bottom">
                        <th scope="col">First Name</th>
                        <th scope="col">Last Name</th>
                        <th scope="col" class="d-none d-md-table-cell">Address</th>
                        <th scope="col" class="d-none d-md-table-cell">Customer Code</th>
                        <th scope="col">Phone</th>
                        <th scope="col">Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                      <tr v-for="(customer, index) in customers" :key="index">
                            <th scope="row" class="py-4">
                            {{ customer.first_name }}
                            </th>
                            <td class="py-4">
                            {{ customer.last_name||"" }}
                            </td>
                            <td class="py-4 d-none d-md-table-cell">
                            {{ customer.address }}
                            </td>
                            <td class="py-4 d-none d-md-table-cell">
                            {{ customer.customer_code }}
                            </td>

                            <td class="py-4">
                            {{
                                customer.phone
                                ? customer.phone.replace(customer.phone.substring(4, 8), "*****")
                                : "055****928"
                            }}
                            </td>

                            <td class="py-4">
                            <div class=" d-flex flex-row text-end">
                                <span
                                class="btn btn-sm me-2"
                                @click="editCustomer(customer)" data-bs-toggle="modal" data-bs-target="#editCustomer"
                                ><i class="bi bi-pencil-square"></i></span>
                                <span
                                class="btn btn-sm"
                                data-toggle="modal"
                                data-target="#deleteUser"
                                @click="deleteCustomer(customer.id)"
                                ><i class="bi bi-trash3"></i
                                ></span>
                            </div>
                            </td>                      
                      </tr>
                    </tbody>
                </table>
        </div>
      <div class="text-center p-3 text-secondary" v-else><p>No Customers to display.</p></div>

      </div>
    </div>
    <CustomerForm/>
    <EditCustomer :customer="sCustomer"/>
  </div>
</template>
<script>
import { onUpdated, ref, watch } from "vue";
import { useStore } from "vuex";
// import { search } from "../../composables/searchEngine";
import CustomerForm from "../../components/Customers/CustomerForm.vue";
import EditCustomer from "../../components/Customers/EditCustomer.vue";
import Swal from "sweetalert2";

export default {
  components: {
    CustomerForm,
    EditCustomer
},
  setup() {
    const store = useStore();
    const customers = ref();
    const sCustomer = ref({});
    const query = ref('');
    let modal;
 

    store.dispatch("getCustomers");
    watch(
      () => store.getters.getCustomers,
      (newCustomers) => {
        customers.value = newCustomers;
      }
    );


    watch(
      () => query.value,
      (newQuery) => {
        console.log('e')
        if (newQuery.length >= 1) {
          customers.value = search(newQuery, store.getters.getCustomers);
        } else {
          customers.value = store.getters.getCustomers;
        }
      }
    );

    const editCustomer = (data) =>{
      sCustomer.value = data;
    }

    const deleteCustomer = (id)=>{
       Swal.fire({
          title: "Do you want to this customer?",
          showCancelButton: true,
          confirmButtonText: "Proceed",
        }).then((result) => {
          /* Read more about isConfirmed, isDenied below */
          if (result.isConfirmed) {
            store
              .dispatch("deleteCustomer", id)
              .then(() => {
                store.dispatch("getCustomers");
              });
          } else {
          }
        });
    }

    return { customers,query,editCustomer, sCustomer,deleteCustomer};
  },
};
</script>
