import axios from "axios";
import { useToast } from "vue-toastification";

//Auth Token
const token = localStorage.getItem('key');

const toast = useToast();
const offset = 30;
const limit = 30;


const state = {
  quotations: [],
  currQuote: "",
  quoteItems: [],
  tempQuote: "", //Temp Quote for Invoice Generation
  quoteToPreview: {},
  allQuote: [],
  unmatched:[],
  nextPageQuote:2,
  prevPageQuote:0,
  currentPageQuote:1,
  quoteCount:0
};

const getters = {
  getQuotes: (state) => {
    return state.quotations;
  },
  getCurrQuote: (state) => {
    return state.currQuote;
  },
  getQuoteItems: (state) => {
    return state.quoteItems;
  },
  getTempQuote: (state) => {
    return state.tempQuote;
  },
  getQuoteToPreview: (state) => {
    return state.quoteToPreview;
  },
  getAllQuote: (state) => {
    return state.allQuote;
  },
  getQuotationPagination:(state)=>{
    return {next:state.nextPageQuote,prev:state.prevPageQuote,current:state.currentPageQuote,count:state.quoteCount}
  }
};

const actions = {
  async getQuote({ commit }, id ) {
    axios
      .get(`http://localhost:8000/api/v1/checkout/service/quotations/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        console.log(res);
        commit("SET_QUOTE", res.data);
      });
  },

  async saveQuote({ commit }, { cart, customer, user_id }) {
    let quoteItems = [];
    cart.forEach((item) => {
      var newItem = { product_id: item.item.id, quantity: item.quantity };

      quoteItems.push(newItem);
    });
    const body = {
      quotation: {
        customer_id: customer.id,
        customer_first_name: customer.first_name,
        customer_middle_name: customer.middle_name,
        customer_last_name: customer.last_name,
        customer_email: customer.email,
        customer_phone: customer.phone,
        user_id: user_id,
      },
      quotation_items: quoteItems,
    };

    await axios
      .post(`http://localhost:8001/api/v1/checkout/service/quotations/create`, body, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        commit("SET_TEMP", res.data);
        console.log(res.data)
        toast.success(`Quotation Created Successfully - ${res.data.quotation.quotation_no}`)
      })
      .catch((err) => {
        if (err) {
          toast.error(
            "Sorry! Quotation Creation Failed: " + err
          );
        } else {
          toast.error("Sorry! Quotation Creation Failed: " + err);
        }
      });
  },

  async getQuoteDetails({ commit }, { id,unm }) {
    axios
      .get(`http://localhost:8001/api/v1/checkout/service/quotation/${id}/retrieve`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        console.log(res)
        commit("QUOTE_TO_PREVIEW", {data:res.data,unm});
      });
  },

};

const mutations = {
  SET_GET_ALL_PRODUCTS: (state, quotes) => {
    state.allQuote = quotes;
  },
  SET_QUOTATIONS: (state, {data,page}) => {
    state.quotations = data.results;
    state.quoteCount =data.count;
    state.nextPageQuote = page + 1;
    state.prevPageQuote = (page>=2)?page-1:0;
    state.currentPageQuote = page;
  },
  SET_QUOTE: (state, quote) => {
    state.currQuote = quote;
  },
  SET_QUOTE_ITEMS: (state, items) => {
    state.quoteItems = items;
  },
  SET_TEMP: (state, data) => {
    state.tempQuote = data.quotation.quotation_no;
  },
  QUOTE_TO_PREVIEW: (state, {data,unm}) => {
    data.quotation.unmatched = unm;
    state.quoteToPreview = data;
  },
  SET_UNMATCHED:(state,data)=>{
    state.unmatched = data.results;
  }
};

export default {
  state,
  getters,
  actions,
  mutations,
};
