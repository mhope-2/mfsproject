import axios from "axios";
import productService from "../../config/config";

//Auth Token
const token = localStorage.getItem('key');

const state = {
    user:'',
    token:'',
    isLoading:'',
    users:[]
}

const getters = {
    getUser: (state) => {
        return state.user;
    },
    getToken:(state)=> state.token,
    users: (state) => {
      return state.users;
    },
    roles: (state) => {
      return state.roles;
    },
}


const actions = {
    async authenticate({ commit }, cred) {
        await axios
          .post(`http://localhost:8000/api/v1/login/`, cred)
          .then((res) => {
            commit("SET_TOKEN", res.data);
          })
          .catch((err) => {
            console.log(err)
        });
    },

    async getUserByToken({ commit },token) {
        if (!token) console.log('No Token');
        await axios
          .post(
            `http://localhost:8000/api/v1/product/service/user/fetch/`,
            { auth_token: token},  
            { headers: { Authorization: `Bearer token` } }
          )
          .then((res) => {
            commit("PERSIST_USER", res.data);
            let currDate = new Date();
            currDate.setTime(currDate.getTime() + 1 * 3600 * 1000);
            localStorage.setItem('key',token);
          })
          .catch((err) => {
            //commit("LOGOUT");
          });

          
      },
   async fetchAllUsers({ commit }) {
    await axios
      .get(`${productService}/users`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        commit("SET_USERS", res.data);
      })
      .catch((err) => {
        commit("FLASH_ERR", err);
      });
  },

  async getUserById({ commit }, { id, token }) {},

  async registerUser({ commit }, { body, token }) {
    console.log(body);
    await axios
      .post(`${productService}/users/create`, body, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        commit("SET_USERS", res.data);
        toast.success("User Registration Successful");
      })
      .catch((err) => {
        commit("FLASH_ERR", err);
        toast.error("Sorry! User Registration Failed");
      });
  },

  async updateUser({ commit }, { id, user }) {
    console.log(user);
    await axios
      .put(`${productService}/users/${id}`, user, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        toast.success("User Updated Successfully");
      })
      .catch((response) => {
        toast.error("Sorry! User Update Failed: " + response);
      });
  },

  async deleteUser({ commit }, id ) {
    await axios
      .delete(`${productService}/user/${id}/delete`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        toast.success("User Deleted Successfully");
      })
      .catch((response) => {
        toast.error("Sorry! User Deletion Failed: " + response);
      });
  },

  async logout({commit}){
    commit('LOGOUT');
  }
}


const mutations = {
    SET_USER :(state,user)=>{
        state.user = user;
    },
    SET_TOKEN:(state,data)=>{
        state.token = data.key;
    },
    PERSIST_USER: (state, user) => {
        state.user = user;
    },
    LOGOUT: (state) => {
      state.curr = "";
      state.auth = false;
      localStorage.removeItem('key');
    },
    SET_USERS: (state, data) => {
      state.users = data;
    },
    FLASH_RESET: (state, email) => {
      state.reset_email = email;
    },
    SET_ROLES: (state, data) => {
      state.roles = data;
    },
    SET_USER_ACT: (state, data) => {
      state.userActivity = data;
    },
}


export default {
    state,
    getters,
    actions,
    mutations
}