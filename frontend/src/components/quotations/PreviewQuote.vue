<template>
    <div class="modal fade" id="quotePreview" tabindex="-1" aria-labelledby="quotePreviewModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="quotePreviewModalLabel">Quotation Details</h5>
          <button type="button" class="btn btn-sm" data-bs-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body" v-if="quoteDetails">
          <p><small>Issued On {{new Date(quoteDetails.created_at).toDateString()}} by <i class="header">{{quoteDetails.quotation.issued_by}}</i></small> </p>
          <div class="row">
            <div class="col">
              <small>Quote No:</small>
              <p class="header">{{quoteDetails.quotation.quotation_no}}<small v-if="quoteDetails.quotation.unmatched"><i class="uil uil-arrow-right"></i> Unmatched</small></p>
            </div>
            <div class="col text-right">
                  <small>Customer:</small>
              <p class="text-capitalize">{{quoteDetails.quotation.customer_first_name +' '+quoteDetails.quotation.customer_last_name}}</p>
            </div>
          </div>

          <div class="table-res">
            <table class="table    table-borderless    quote-table pt-5">
                                <thead class="bg-light header">
                                    <tr>
                                        <th scope="col">No.</th>
                                        <th scope="col">Item</th>
                                        <th scope="col">SKU</th>
                                        <th scope="col">Unit Price</th>
                                        <th scope="col-2">Quantity</th>
                                        <th scope="col">Total</th>
                                    </tr>
                                </thead>
                                <tbody class="quote-semi-table">
                                    <tr class="border-bottom" v-for="(item,index) in quoteDetails.quotation_items" :key="index">
                                        <td><small>{{index+1}}</small></td>
                                        <td><small>{{item.product_details.product_description}}</small></td>
                                        <td><small>{{item.product_details.EAN_Code}}</small></td>
                                        <td><small>{{item.product_details .unit_price}}</small></td>
                                        <td><small>{{item.quantity}}</small></td>
                                        <td><small>{{parseFloat(item.product_details .unit_price).toFixed(2)*parseFloat(item.quantity).toFixed(2)}}</small></td>
                                    </tr>
                                </tbody>
                            </table>
                            <div class="row">
                              <div class="col"></div>
                              <div class="col text-end">
                                <small>Sub Total:</small>
                                <h4 class="mt-2"><small>GHs </small>{{subTotal.toFixed(2)}}</h4>
                                <small><i class="header">Tax Inclusive</i></small>
                              </div>
                            </div>
          </div>
      </div>
        <div class="modal-footer" v-if="quoteDetails">
        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn cbtn btn-sm" v-if="quoteDetails.quotation.unmatched" @click="generateInvoice(quoteDetails)">Generate Invoice</button>
        <button type="button" class="btn cbtn btn-sm" disabled v-else>Generate Invoice</button>
      </div>
    </div>
    </div>

    </div>
</template>
<script>
import { useStore } from 'vuex';
import {ref,watch} from 'vue';
import {useRouter} from 'vue-router'
export default {
    setup() {
      const router = useRouter();
      const store = useStore();
      const quoteDetails = ref();
      const subTotal = ref();
      watch(()=>store.getters.getQuoteToPreview,(newDetails)=>{
          quoteDetails.value = newDetails;
          let subArr=[];
          quoteDetails.value.quotation_items.forEach(item=> {
            subArr.push(parseFloat(item.product_details .unit_price)*parseFloat(item.quantity));
          });
          subTotal.value = subArr.reduce((a,b)=>a+b,0);
      });
              
        


        const generateInvoice = (quotation) =>{
            store.dispatch('setQuoteToInvoice',{quotation,token:getToken(),branch_id:1})
            store.dispatch('getCustomer',{})
        }
      
        watch(()=>store.getters.getSetQuoteToInvoice,(newCart)=>{
          $('#quotePreview').modal('hide');
          store.dispatch('setCartNoUpdate',newCart.updated).then(()=>{
            router.push({name:'Shop'});
          });
        })

      return {quoteDetails,subTotal,generateInvoice}
    },
}
</script>