import axios from "axios";
import productService from "../../config/config";

//Auth Token
const token =  '32faa3858437ece24b104ceb6739add9adcab108' //localStorage.getItem('key');

const state = {
  customers: [],
  customer: {},
  sCustomer: {},
};

const getters = {
  getCustomers: (state) => {
    return state.customers;
  },
  getCustomer: (state) => {
    return state.customer;
  },
  getSCustomer: (state) => {
    return state.sCustomer;
  },
};

const actions = {
  async getCustomers({ commit }) {
    await axios
      .get(`http://localhost:8000/api/v1/product/service/customers`, {
        params: { key: token },
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        commit("SET_CUSTOMERS", res.data);
      })
      .catch((err) => {});
  },
  async getCustomer({ commit }, id ) {
    await axios
      .get(`http://localhost:8000/api/v1/product/service/customer/${id}/retrieve`, {
        params: { key: token },
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        commit("SET_CUSTOMER", res.data);
      })
      .catch((err) => {});
  },

  async createCustomer({ commit }, body) {
    await axios
      .post(`http://localhost:8000/api/v1/product/service/customers/create`, body, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {

      })
      .catch((err) => {

      });
  },

  async updateCustomer({ commit }, { id, body }) {
    await axios
      .put(`http://localhost:8000/api/v1/product/service/customers/${id}/update`, body, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {

      })
      .catch((err) => {

      });
  },

  async deleteCustomer({ commit }, id) {
    await axios
      .delete(`http://localhost:8000/api/v1/product/service/customers/${id}/delete`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
      })
      .catch((err) => {

      });
  },

  async setQuoteCustomer({ commit }, { customer }) {
    commit("SET_SCUSTOMER", customer);
  },

};

const mutations = {
  SET_CUSTOMERS: (state, data) => {
    state.customers = data;
  },

  SET_CUSTOMER: (state, data) => {
    state.customer = data;
  },
  SET_SCUSTOMER: (state, customer) => {
    state.sCustomer = customer;
  },

};

export default {
  state,
  getters,
  actions,
  mutations,
};
