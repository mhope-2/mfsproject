<template>
  <div class="p-4">
    <PreviewQuote />
    <div class="py-3">
      <div class="mt-3 mb-3">
        <input
          type="text"
          class="form-control"
          v-model="query"
          placeholder="Search Quotations"
        />
      </div>
      <div class="d-sm-none clearfix"></div>
    </div>

        <div class="pagination d-flex justify-content-end" v-if="quotations">
            <button class="btn me-2 btn-sm" :disabled="page<=1"><i class="bi bi-chevron-left" @click="goTo(page-1)"></i></button>
            <button class="btn btn-sm" @click="goTo(page+1)"><i class="bi bi-chevron-right"></i></button>
        </div>

    <div v-if="quotations" class="table-res">
      <table class="table table-borderless quote-table pt-5">
        <thead>
          <tr class="border-bottom header">
            <th scope="col">Quote No.</th>
            <th scope="col">Customer</th>
            <th scope="col">Business Name</th>

            <th scope="col">Issued By</th>
            <th scope="col">Date Of Issue</th>
          </tr>
        </thead>

        <tbody class="quote-semi-table">
          <tr
            v-for="(quote, index) in quotations"
            :key="index"
            class="border-bottom"
            @click="previewQuote(quote.id)"
            data-bs-toggle="modal"
            data-bs-target="#quotePreview"
          >
            <th scope="row" class="pt-2 pb-5">{{ quote.quotation_no }}</th>
            <td class="pt-2 pb-5 text-capitalize">
              {{ quote.customer_first_name + " " }}
              {{ quote.customer_last_name }}
            </td>
            <th scope="row" class="pt-2 pb-5">
              {{ quote.business_name }}
            </th>
            <td>{{ quote.issued_by }}</td>
            <td class="pt-2 pb-5">
              {{ new Date(quote.created_at).toDateString() }}<br />
              {{ new Date(quote.created_at).toLocaleTimeString() }}
            </td>
            <td>
              <p class="header fs-3" v-if="quote.unmatched">
                <i class="bi bi-link-45deg"></i>
              </p>
            </td>
          </tr>
        </tbody>
      </table>

        <div class="pagination d-flex justify-content-end" v-if="quotations">
            <button class="btn me-2 btn-sm" :disabled="page<=1"><i class="bi bi-chevron-left" @click="goTo(page-1)"></i></button>
            <button class="btn btn-sm" @click="goTo(page+1)"><i class="bi bi-chevron-right"></i></button>
        </div>
    </div>

  </div>
</template>

<script>
import { ref, watch } from "vue";
import { useStore } from "vuex";
// import { search } from "../../composables/searchEngine";
import PreviewQuote from "../../components/quotations/PreviewQuote.vue";
export default {
  components: {
    PreviewQuote,
  },

  setup() {
    const store = useStore();
    const quotations = ref([]);
    const query = ref();
    const pagination = ref();
    const btn_array = ref([]);
    const count = ref();
    const unmatched = ref();
    const page = ref(1);

    store.dispatch("getUnmatched");



    store.dispatch("getQuotes", page.value );

    watch(
      () => store.getters.getQuotes,
      (newQuotes) => {
        quotations.value = newQuotes;
      }
    );

    const previewQuote = (id) => {
      const indexOfUnmacthed = store.getters.getUnmatched.findIndex(
        (item) => item.id == id
      );
      let unm = false;
      if (indexOfUnmacthed >= 1) {
        unm = true;
      }
      store.dispatch("getQuoteDetails", { id,  unm });
    };

    watch(
      () => store.getters.getQuotes,
      (newQuotes) => {
        quotations.value = newQuotes;
      }
    );

    //Search Quotes
    watch(
      () => query.value,
      (newQuery) => {
        if (newQuery.length >= 1) {
          quotations.value = search(newQuery, store.getters.getQuotes);
        } else {
          quotations.value = store.getters.getQuotes;
        }
      }
    );

    //Goto
    const goTo = (newPage) => {
    page.value = newPage;
      store.dispatch("getQuotes",page.value);
    };

    return {
      quotations,
      previewQuote,
      query,
      pagination,
      count,
      goTo,
      page
    };
  },
};
</script>

<style scoped>
.quote-semi-table tr:hover {
  cursor: pointer;
  background-color: var(--pink-dk) !important;
  color: var(--bg-primary) !important;
}
</style>
