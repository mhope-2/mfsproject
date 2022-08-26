<template>
  <div
    class="modal fade"
    id="inPreviewModal"
    tabindex="-1"
    aria-labelledby="inPreviewModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="inPreviewModalLabel">Invoice</h5>
          <button
            type="button"
            class="btn"
            data-bs-dismiss="modal"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body" v-if="sInvoice">
          <div class="row">
            <div class="col-md-4">
              <small class="header">
                Invoice No. <i class="uil uil-arrow-right"></i> Quotation
                No.</small
              >
              <p>
                <b>{{ sInvoice.invoice.invoice_no }}</b>
                <i class="bi bi-arrow-up-right header"></i>
                {{ sInvoice.invoice.quotation_no }}
              </p>
            </div>


            <div class="col">
              <small class="header"> Date of Issue</small>
              <p>{{ new Date(sInvoice.invoice.created_at).toDateString() }}</p>
            </div>
            <!-- <div class="col">
              <small class="header"> Date of Issue</small>
              <p>{{ new Date(sInvoice.invoice.created_at).toDateString() }}</p>
            </div> -->
            <div class="col">
              <small class="header">Issued By</small>
              <p>{{ sInvoice.invoice.issued_by }}</p>
            </div>

            <div class="col">
              <small class="header">Payment Status</small>
              <p v-if="sInvoice.invoice.partial_payment">Partially Paid</p>
              <p v-else>Fully Paid</p>
            </div>
          </div>

          <table class="table table-borderless quote-table pt-5">
            <thead class="bg-light">
              <tr>
                <th scope="col">Item</th>
                <th scope="col">SKU</th>
                <th scope="col">Unit Price</th>
                <th scope="col-2">Quantity</th>
                <th scope="col">Total</th>
              </tr>
            </thead>
            <tbody class="quote-semi-table">
              <tr
                class="border-bottom"
                v-for="(item, index) in sInvoice.invoice_items"
                :key="index"
              >
                <td>
                  <small>{{
                    item.product_details.name +
                    " " +
                    item.product_details.product_description
                  }}</small>
                </td>
                <td>
                  <small>{{ item.product_details.EAN_Code }}</small>
                </td>
                <td>
                  <small>{{ item.product_details.unit_price }}</small>
                </td>
                <td>
                  <small>{{ item.quantity }}</small>
                </td>
                <td>
                  <small>{{
                    parseFloat(item.product_details.unit_price).toFixed(2) *
                    parseFloat(item.quantity).toFixed(2)
                  }}</small>
                </td>
              </tr>
            </tbody>
          </table>

          <div class="my-3" v-if="sInvoice && sInvoice.invoice.sales_rep_note">
            <p class="header m-0"><small><i class="bi bi-chat-square-dots-fill"></i> Sales Rep Note</small></p>
            <div class="card rounded-2 p-2 mt-2">
                <p class="p-0 m-0">{{sInvoice.invoice.sales_rep_note}}</p>
            </div>
          </div>

          <div class="row">
            <div class="col">
              <small class="header">Customer Details</small>
              <p class="text-capitalize">
                {{
                  sInvoice.invoice.customer_first_name +
                  " " +
                  sInvoice.invoice.customer_last_name
                }}
              </p>
            </div>
            <div class="col text-end">
              <small class="header">Net Total</small>
              <p class="">
                GHs {{ parseFloat(sInvoice.invoice.net_total).toFixed(2) }}
              </p>
              <div v-if="sInvoice.invoice.partial_payment">
                <small>Credit</small>
                <p>{{ sInvoice.invoice.credit_line }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="text-center" v-else><p>...Loading</p></div>
        <div class="modal-footer" v-if="sInvoice">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            Close
          </button>
          <button type="button" class="btn cbtn" @click="printPreview">
            Print
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { watch, ref, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import {Modal} from 'bootstrap'
export default {
  setup() {
    const store = useStore();
    const sInvoice = ref();
    const router = useRouter();
    const branch = ref();
    let myModal;

    onMounted(()=>{  myModal = new Modal('#inPreviewModal', {keyboard:false})})

    watch(
      () => store.getters.invoiceToPreview,
      (newInvoice) => {
        sInvoice.value = newInvoice;
      }
    );


    watch(()=>store.getters.getBranchByID,(newBranch)=>{
       branch.value = newBranch;
    })

    const printPreview = () => {
      store.dispatch("setToPrint", sInvoice.value);
      myModal.hide()
      router.push({ name: "printInvoice" });
    };


  

    return { sInvoice, printPreview };
  },
};
</script>