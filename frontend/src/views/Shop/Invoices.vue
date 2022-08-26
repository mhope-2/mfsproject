<template>
    <div class="p-5">
        <div class="text-end mb-4"><router-link to="/shop/quotations" class="btn btn-sm"><i class="bi bi-file-earmark-ruled-fill"></i> Quotations</router-link></div>
        <div>
            <div class="inputGroup mb-4">
                <input type="text" class="form-control form-control-sm" placeholder="Search" v-model="query">
            </div>
        </div>
        <div class="pagination d-flex justify-content-end" v-if="invoices">
            <button class="btn me-2 btn-sm" :disabled="page<=1"><i class="bi bi-chevron-left" @click="getNextInvoices(page-1)"></i></button>
            <button class="btn btn-sm" @click="getNextInvoices(page+1)"><i class="bi bi-chevron-right"></i></button> 
        </div>
        <div>
            <table class="table">
            <thead class="header">
                <tr class="border-bottom">
                <th scope="col">Invoice No.</th>
                <th scope="col">Quotation No.</th>
                <th scope="col">Customer</th>
                <th scope="col">Payment Status</th>
                <th scope="col">Net Total</th>
                <th scope="col">Date Of Issue</th>
                <th></th>
                </tr>
            </thead>
            <tbody>
                <tr class="py-5 border-bottom" v-for="(invoice,index) in invoices" :key="index" @click="setPreview(invoice.id)" data-bs-toggle="modal" data-bs-target="#inPreviewModal">
                    <th class="py-4">
                    <p>
                        <b>{{ invoice.invoice_no }}</b>
                    </p>
                    </th>

                    <td class="py-4 d-none d-md-table-cell">
                    <p>{{ invoice.quotation_no }}</p>
                    </td>

                    <td class="py-4">
                    <p>
                        {{
                        invoice.customer_first_name + " " + (invoice.customer_last_name || "")
                        }}
                    </p>
                    </td>

                    <td class="py-4">
                    <p>{{ invoice.net_total }}</p>
                    </td>

                    <td class="py-4 d-none d-md-table-cell">
                    <p>{{ new Date(invoice.created_at).toUTCString() }}</p>
                    </td>
                    <td class="py-4"><p class="header" v-if="invoice.sales_rep_note"><i class="bi bi-chat-square-dots-fill"></i></p></td>
                </tr>
            </tbody>
            </table>
        </div>
        <div class="pagination d-flex justify-content-end" v-if="invoices">
            <button class="btn me-2 btn-sm" :disabled="page<=1"><i class="bi bi-chevron-left" @click="getNextInvoices(page-1)"></i></button>
            <button class="btn btn-sm" @click="getNextInvoices(page+1)"><i class="bi bi-chevron-right"></i></button>
        </div>
        <InvoicePreview/>
    </div>
</template>
<script>
import {ref,watch} from 'vue';
import {useStore} from 'vuex';
// import { search } from '../../composables/searchEngine';
import InvoicePreview from "../../components/Invoice/InvoicePreview.vue";
export default {
    components:{
        InvoicePreview
    },
    setup() {
        const store = useStore();
        const invoices = ref();
        const page = ref(1);
        const query = ref('');

        store.dispatch('getInvoices',page.value)
        watch(()=>store.getters.getInvoices,(newInvoices)=>{
            invoices.value = newInvoices;
        })


        const setPreview = (id) => {
    
            store.dispatch("retrieveInvoice", {
                id
            });
        };

        // watch(
        //     () => query.value,
        //     (newQuery) => {
        //         if (newQuery.length >= 1) {
        //         invoices.value = search(newQuery, store.getters.getInvoices);
        //         } else {
        //         invoices.value = store.getters.getInvoices;
        //         }
        //     }
        // );


         const getNextInvoices = (newPage)=>{
            page.value = newPage;
            store.dispatch('getInvoices',page.value);
        }


        return{invoices,setPreview,getNextInvoices,page,query}
    },
}
</script>