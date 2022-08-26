import axios from "axios";
import { useToast } from "vue-toastification";
const toast = useToast();

const limit = 30;
const offset = 30;

//Auth Token
const token = localStorage.getItem('key');


const state = {
  invoices: [],
  currInvoiceNo: "",
  invoiceToPreview: {},
  nextPageInvoice: "",
  previousPageInvoice: "",
  currentPageInvoice: "",
  toPrint: "",
  getInvoices: [],
  countInvoice: "",
  set_quote_invoice: "",
};

const getters = {
  getInvoices: (state) => {
    return state.invoices;
  },
  getNextInvoice: (state) => {
    return state.currInvoiceNo;
  },
  invoiceToPreview: (state) => {
    return state.invoiceToPreview;
  },
  getToPrint: (state) => {
    return state.toPrint;
  },
  getInvoices: (state) => {
    return state.invoices;
  },
  getPaginationInvoices: (state) => {
    return {
      next: state.nextPageInvoice,
      previous: state.previousPageInvoice,
    };
  },
  getInvoiceCount: (state) => {
    return state.countInvoice;
  },
  getSetQuoteToInvoice: (state) => {
    return state.set_quote_invoice;
  },
};

const actions = {
  async getInvoices({ commit } ) {
    axios
      .get(
        `http://localhost:8001/api/v1/checkout/service/invoices`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      .then((res) => {
        commit("SET_INVOICES", { data: res.data });
      })
      .catch((err) => {
        toast.error("Sorry! Retrieving  Invoice Failed: " + err);
      });
  },

  async createInvoice(
    { commit },
    {
      cart,
      customer,
      user_id,
      quotation_no,
      cash,
      mobile_money,
      netTotal,
      bank_transfer,
      amount_received
    }
  ) {
    let invoice_items = [];

    cart.forEach((item) => {
      var newItem = {
        product_id: item.item.id,
        quantity: item.quantity,
        description: "",
        unit_price: parseFloat(item.item.unit_price),
        sub_total:
          parseFloat(item.quantity) *
          (parseFloat(item.item.unit_price)),
      };

      invoice_items.push(newItem);
    });
    const body = {
      invoice: {
        customer_id: customer.id,
        customer_first_name: customer.first_name,
        customer_middle_name: customer.middle_name,
        customer_last_name: customer.last_name,
        customer_email: customer.email,
        quotation_no: quotation_no,
        customer_phone: customer.phone,
        user_id: user_id,
        net_total: netTotal,
        cash: cash,
        bank_transfer: bank_transfer,
        mobile_money: mobile_money,
        amount_received
      },
      invoice_items: invoice_items,
    };

    await axios
      .post(`http://localhost:8001/api/v1/checkout/service/invoices/create`, body, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        commit("SET_PRINT", res.data);
        toast.success("Invoice Created Successfully");
      })
      .catch((err) => {
        toast.error("Sorry! Invoice Creation Failed: " + err);
      });
  },

  async retrieveInvoice({ commit }, { id }) {
    axios
      .get(
        `http://localhost:8001/api/v1/checkout/service/invoices/${id}/retrieve`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      .then((res) => {
        commit("SET_INVOICE_PREVIEW", res.data);
        console.log(res.data)
      });
  },


  async setToPrint({ commit }, data) {
    commit("SET_PRINT", data);
  },

  
  clearSetQuoteInvoice({ commit }) {
    commit("CLEAR_SET_QUOTE_TO_INVOICE");
  },
};

const mutations = {
  SET_INVOICES: (state, { data }) => {
    state.invoices = data;
  },
  NEXT_INVOICE: (state, data) => {
    state.currInvoiceNo = data;
  },
  SET_INVOICE_PREVIEW: (state, data) => {
    state.invoiceToPreview = data;
  },
  SET_PRINT: (state, data) => {
    state.toPrint = data;
  },
  SET_QUOTE_TO_INVOICE: (state, { updated, quotation }) => {
    state.set_quote_invoice = { updated, quotation };
  },
  CLEAR_SET_QUOTE_TO_INVOICE: (state) => {
    state.set_quote_invoice = "";
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
