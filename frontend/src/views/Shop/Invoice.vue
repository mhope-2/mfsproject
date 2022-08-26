<template>
    <div class="p-4">
        <div class="px-4 mb-4"><button class="btn">View Cart</button></div>
        <form @submit.prevent="createInvoice()">
            <div class="row">
                <div class="col-md-7 px-5 border-end">
                    <div class="inputGroup">
                        <label for=""><small class="header">Select Customer</small></label>
                        <select class="form-select form-select-sm mt-3" aria-label="Default select example" v-model="sCustomer">
                            <option value="" selected>Select a Customer</option>
                            <option v-for="(customer,index) in customers" :key="index" :value="customer" class="text-capitalize">{{customer.first_name+' '+customer.last_name}}</option>
                        </select>
                    </div>

                    <div class="row mt-4" v-if="sCustomer">
                        <div class="col-md-6">
                            <label><small class="header">Customer</small></label>
                            <p>{{sCustomer.first_name+' '+sCustomer.last_name}}</p>
                        </div>
                    </div>

                    <div class="paymentTabs mt-4">
                            <p><small class="header">Payment Options</small></p>
                            <div class="row text-secondary">
                                <div class="inputGroup col-md-3">
                                    <input type="radio" id="cash" name="payment" v-model="mode" value="csh">
                                    <label class="card p-3 rounded-3" for="cash"><p class="m-0"><i class="bi bi-cash"></i> Cash</p></label>
                                </div>
                                <div class="inputGroup col-md-3">
                                    <input type="radio" id="mobile" name="payment" v-model="mode" value="momo">
                                    <label class="card p-3 rounded-3" for="mobile"><p class="m-0"><i class="bi bi-phone-fill"></i> Mobile Money</p></label>
                                </div>
                                <div class="inputGroup col-md-3">
                                    <input type="radio" id="bank" name="payment" v-model="mode" value="bnk">
                                    <label class="card p-3 rounded-3" for="bank"><p class="m-0"><i class="bi bi-bank2"></i> Bank Transfer</p></label>
                                </div>
                       </div>
                    </div>
                    <div class="mt-5">
                        <label for="" class="header">Additional Notes</label>
                        <textarea class="form-control" name="" id=""  rows="5" v-model="sales_rep_note"></textarea>
                    </div>
                </div>
                <div class="col-md-5 px-5">
                    <p class="header">Payment Breakdown</p>
                    <div class="row">
                    <div class="col">
                        <small class="header"> Sub Total </small>
                        <h4><small>GHs</small> {{ total.subTotal.toFixed(2) }}</h4>
                    </div>


                    <div class="col">
                        <small class="header"> Amount Due </small>
                        <h4><small>GHs</small> {{ total.total.toFixed(2)  }}</h4>
                    </div>
                    </div>
                    <hr />

                    <div>
                    </div>
                    <div class="row">

                    <div class="col">
                        <p><small class="header">Amount Received</small></p>
                        {{amountDue}}
                    </div>
                    </div>

                    <div class="mt-4 mb-3">
                        <button class="btn w-100">Generate Invoice</button>
                    </div>

      
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import {useStore} from 'vuex';
    import {ref,watch} from 'vue';
    import Cart from './Cart.vue';
    import { useRouter } from 'vue-router';
    export default {
        components:{
            Cart
        },
        setup() {
            const store = useStore();
            const customers = ref([]);
            const sCustomer = ref('');
            const router = useRouter();
            const total = ref(store.getters.getTotal);
            const mode = ref('csh');
            const cshAmt = ref(0);
            const momoAmt = ref(0);
            const bnkAmt = ref(0);
            const sales_rep_note = ref('');

            if(store.getters.getCart.length<1){
                router.push('products');
            }

            //Amount
            const amountDue = ref(0);


            store.dispatch('getCustomers');
            
            watch(()=>store.getters.getCustomers,(newCustomers)=>{
                customers.value = newCustomers;
            })

            watch(() => store.getters.getTotal, () => {
                    total.value = store.getters.getTotal;
            }
            );

            watch(()=>mode.value, (newMode)=>{


            })
        
        const createInvoice = async () => {

                await store.dispatch("saveQuote", {
                        cart: store.getters.getCart,
                        customer: sCustomer.value,
                        user_id: store.getters.getUser.id,
                        });


                        switch(mode.value){
                                case 'csh':
                                    cshAmt.value = store.getters.getTotal.total;
                                    momoAmt.value=0
                                    bnkAmt.value=0
                                    break;
                                case 'momo':
                                    cshAmt.value=0
                                    momoAmt.value = store.getters.getTotal.total;
                                    bnkAmt.value=0
                                    break;
                                case 'bnk':
                                    momoAmt.value=0
                                    bnkAmt.value = store.getters.getTotal.total;
                                    cshAmt.value=0
                                    break;
                                default:
                                    throw new Error('Case Not Found')
                            }
            store.dispatch("createInvoice", {
                branch_id: 1,
                cart: store.getters.getCart,
                user_id: store.getters.getUser.id,
                customer: sCustomer.value,
                quotation_no:
                    store.getters.getSetQuoteToInvoice &&
                    store.getters.getSetQuoteToInvoice.updated.length >= 1
                    ? store.getters.getSetQuoteToInvoice.quotation.quotation
                        .quotation_no
                    : store.getters.getTempQuote,
                business_name: sCustomer.business_name,
                cash: parseFloat(cshAmt.value),
                mobile_money: parseFloat(momoAmt.value),
                bank_transfer: parseFloat(bnkAmt.value),
                credit_line: 0,
                netTotal: total.value.total,
                discount: 0,
                amount_received:
                    parseFloat(cshAmt.value) +
                    parseFloat(bnkAmt.value) +
                    parseFloat(momoAmt.value) +
                    parseFloat(0),
                change: 0,
                covid_levy_value: 0,
                vat_value: 0,
                sales_rep_note: sales_rep_note.value,
                });

                setTimeout(function () {
                router.push({ name: "printInvoice" });
                store.dispatch("clearCart");
                store.dispatch("clearSetQuoteInvoice");
                }, 3000);
          
        }
            return{customers,sCustomer,amountDue,total,createInvoice,mode,sales_rep_note}
        },
    }
</script>