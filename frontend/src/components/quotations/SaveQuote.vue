<template>
  <div
    class="modal fade"
    id="saveQuote"
    tabindex="-1"
    aria-labelledby="saveQuoteLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="saveQuote">Save Quote</h5>
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="">
            <div class="py-4">
              <div class="row">
                <div class="col-md-10">
                  <label for=""><small>Client Name</small></label>
                  <input
                    list="browsers"
                    id="myBrowser"
                    name="myBrowser"
                    class="form-control form-control-sm"
                    v-model="customer"
                    @change="setCustomer(customer)"
                    required
                  />
                  <datalist id="browsers">
                    <option
                      class="text-capitalize"
                      v-for="(customer, index) in customers"
                      :key="index"
                      :value="customer.first_name + ' ' + customer.last_name"
                    />
                  </datalist>
                </div>
                <div class="col-md-2">
                  <br />
                  <button
                    class="btn cbtn btn-sm mt-2"
                    data-toggle="modal"
                    data-target="#customerForm"
                    :disabled="newCsRg"
                  >
                    <i class="uil uil-focus-add"></i> New Customer
                  </button>
                </div>
              </div>
            </div>
            <div style="overflow-x:auto">

            <table
              class="table table responsive table-borderless quote-table pt-5"
            >
              <thead>
                <tr class="border-bottom">
                  <th scope="col">No.</th>
                  <th scope="col">EAN</th>
                  <th scope="col">Item</th>
                  <th scope="col">Unit Type</th>
                  <th scope="col-2">Quantity</th>
                  <th scope="col">Selling Price</th>
                  <th scope="col">Total</th>
                  <th></th>
                </tr>
              </thead>
              <tbody class="quote-semi-table">
                <tr v-for="(item, index) in cart" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ item.item.barcode}}</td>
                  <td>{{ item.item.product_description }}</td>
                  <td>{{ item.item.unit }}</td>
                  <td class="col-2">
                    <input
                      type="number"
                      :min="1"
                      :max="
                        parseInt(item.item.quantity) -
                        parseInt(item.item.alert_quantity||5)
                      "
                      :value="item.quantity"
                      @input="(event) => changeQuantity(event, item.item.id)"
                      class="form-control quantity"
                    />
                  </td>
                  <td>{{ parseFloat(item.item.unit_price ).toFixed(2)}}</td>
                  <td>
                    {{
                      (parseFloat(item.item.unit_price) *
                      parseFloat(item.quantity)).toFixed(2)
                    }}
                  </td>
                  <td>
                    <span
                      class="badge badge-secondary badge-pill p-2"
                      @click="removeItemFromQuote(item)"
                      ><i class="bi bi-trash3"></i></span>
                  </td>
                </tr>
              </tbody>
            </table>
            </div>

            <div class="row mb-3">
              <div class="col"></div>
              <div class="col text-right">
                <small>Total:</small>
                <h4><small>GHs </small>{{ parseFloat(total).toFixed(2) }}</h4>
                <small class="text-secondary">Tax Inclusive</small>
              </div>
            </div>
            <div class="modal-footer" v-if="customer && cart.length >= 1">
              <button type="button" class="btn cbtn" data-dismiss="modal">
                Close
              </button>
              <button
                type="submit"
                @click="saveQuote"
                class="btn btn-secondary"
                v-if="dispBind"
                :disabled="!newCsRg"
              >
                Save And Exit
              </button>
              <button
                class="btn cbtn-alt"
                @click="proceedInvoice"
                v-if="dispBind"
                :disabled="!newCsRg"
              >
                Proceed
              </button>
            </div>
            <div class="modal-footer" v-else>
              <button type="button" class="btn cbtn" data-dismiss="modal">
                Close
              </button>
              <button
                type="submit"
                class="btn btn-secondary"
                v-if="dispBind"
                disabled
              >
                Save And Exit
              </button>
              <button
                class="btn cbtn-alt"
                @click="proceedInvoice"
                v-if="dispBind"
                disabled
              >
                Proceed
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, watch, watchEffect } from "vue";
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import { useToast } from "vue-toastification";

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();
    const cart = ref(store.getters.getCart);
    const customers = ref();
    const customer = ref("");
    const total = ref(store.getters.getTotal.total);
    const newCsRg = ref();
    const user = ref(store.getters.user);
    const dispBind = ref(true);
    const toast = useToast();
    const inputCustomer = ref();

    if (route.name == "Invoice") {
      dispBind.value = false;
      customer.value =
        store.getters.getSCustomer.first_name +
        " " +
        store.getters.getSCustomer.last_name;
    } else {
      dispBind.value = true;
    }

    watch(
      () => [...store.getters.getCart],
      (newCart) => {
        cart.value = newCart;
      }
    );
    watch(
      () => store.getters.getTotal.total,
      (newTotal) => {
        total.value = parseFloat(newTotal).toFixed(2);
      }
    );

    store.dispatch("getCustomers", getToken());

    //watch Customers
    watch(
      () => [...store.getters.getCustomers],
      (newCustomers) => {
        customers.value = newCustomers;
      }
    );

    //Bind Value
    watch(
      () => customer.value,
      (newCustomer) => {
        if (newCustomer) {
          newCsRg.value = true;
        } else {
          newCsRg.value = false;
        }
      }
    );

    //Set Customer
    const setCustomer = (customer) => {
      let newCustomer;
      customers.value.map((selectedCustomer) => {
        if (
          customer ===
          `${selectedCustomer.first_name + " " + selectedCustomer.last_name}`
        ) {
          newCustomer = selectedCustomer;
        }
      });
      inputCustomer.value = newCustomer;
      store.dispatch("setQuoteCustomer", {
        customer: newCustomer,
        token: getToken(),
      });
    };

    //saveQuotation
    const saveQuote = () => {
      store
        .dispatch("saveQuote", {
          cart: cart.value,
          customer: inputCustomer.value,
          token: getToken(),
          user_id: user.value.id,
        })
        .then(() => {
          $("#saveQuote").modal("hide");
          store.dispatch("clearCart");
        });
    };

    //Proceed
    const proceedInvoice = () => {
      if (cart.value && cart.value.length >= 1) {
        $("#saveQuote").modal("hide");
        if (inputCustomer.value) {
          router.push({
            name: "Invoice",
            params: { customer: JSON.stringify(inputCustomer.value) },
          });
          toast.success("Quotation Created");
        } else {
           toast.error("Quotation creation failed");
          router.push({ name: "Invoice" });
        }
      }
    };

    //Change In quantity
    const changeQuantity = (event, id) => {
      store.dispatch("changeQuantity", { value: event.target.value, id });
      store.dispatch("calcTotal");
    };

    const removeItemFromQuote = (item) => {
      store.dispatch("removeFromCart", item);
    };

    return {
      cart,
      saveQuote,
      customers,
      customer,
      proceedInvoice,
      total,
      newCsRg,
      inputCustomer,
      changeQuantity,
      setCustomer,
      removeItemFromQuote,
      dispBind,
    };
  },
};
</script>
