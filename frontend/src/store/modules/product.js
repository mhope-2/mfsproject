import axios from 'axios';
import productService from '../../config/config';

//Auth Token
const token = localStorage.getItem('key');

//Pagination
const offset = 30;
const limit = 30;

const branch_id = 1;


const state = {
    products:[],
    next:2,
    previous:1,
}

const getters = {
    getProducts:(state)=>{
        return state.products;
    },
    getPagination:(state)=>{
        return {next,previous}
    }
}


const actions = {
    async getProducts({ commit },  page) {
        return await axios
          .get(
            `http://localhost:8000/api/v1/product/service/products`,
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          )
          .then((res) => {
            commit("SET_PRODUCTS", {data: res.data });
          })
          .catch((err) => {
            commit("SET_LOADING",{loading:false})
          });
      },
      async getProduct({ commit }, id) {},
    
      async createProduct({ commit }, product) {
        await axios
          .post(`http://localhost:8000/api/v1/product/service/products/create`, product, {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((res) => {
    
          })
          .catch((err) => {
    
          });
      },

      updateProduct({ commit }, { product, id }) {
        return axios
          .put(`http://localhost:8000/api/v1/product/service/products/${id}/update`, product, {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((res) => {

          })
          .catch((err) => {

          });
      },
    
      async setToDelete({ commit }, { id, index }) {
        commit("TO_DELETE", { id, branch_id, index });
      },
    
    
      async deleteProduct({ commit }, {id} ) {
        return await axios
          .delete(`http://localhost:8000/api/v1/product/service/products/${id}/delete`, {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((res) => {
            commit("EMPTY_TO_DELETE");
          })
          .catch((err) => {
            console.log(err);
          });
      },

      // async deleteProduct({ commit }, {id,branch_id} ) {
      //   return await axios
      //     .delete(`${endPoint}/products/by/branch/${id}/delete`, {
      //       headers: { Authorization: `Bearer ${token}` },
      //       data: { branch_id },
      //     })
      //     .then((res) => {
      //       commit("EMPTY_TO_DELETE");
      //     })
      //     .catch((err) => {
      //       console.log(err);
      //     });
      // },

      // async searchProduct({ commit }, { keyword, branch_id, unit }) {
      //   await axios
      //     .post(
      //       `http://localhost:8000/product/service/products/by/branch/product/search`,
      //       { keyword: keyword, branch_id: branch_id, unit },
      //       {
      //         headers: { Authorization: `Bearer ${token}` },
      //       }
      //     )
      //     .then((res) => {
      //       commit("GET_SEARCHED_PRODUCT", res.data.response);
      //     })
      //     .catch((err) => {
      //       console.log(err);
      //     });
      // },
}


const mutations = {
    SET_PRODUCTS: (state, { page, data }) => {
        state.products = data;
        state.next =
          page >= 1 && page <= Math.round(data.count / 30) ? page + 1 : 2;
        state.previousPage =
          page >= 1 && page <= Math.round(data.count / 30) ? page - 1 : 1;
      },
    
      TO_DELETE: (state, { id, index }) => {
        if (id) {
          state.toDelete = { id, index };
        } else {
          state.toDelete = {};
        }
      },
      EMPTY_TO_DELETE: (state) => {
        state.toDelete = {};
      },
      SET_EDIT: (state, data) => {
        state.sProduct = data;
      },
      SET_SELECTED_DELETE: (state, data) => {
        state.selected_delete = data;
      },
      GET_SEARCHED_PRODUCT: (state, data) => {
        state.searchedProductData = data;
      }
}

export default {
    state,
    getters,
    actions,
    mutations
}