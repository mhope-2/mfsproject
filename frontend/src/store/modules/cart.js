import axios from "axios";
import productService from '../../config/config';

//Helper Function for validating products in cart
function containsObject(obj, list) {
    var i;
    for (i = 0; i < list.length; i++) {
        if (list[i].item.id === obj.id) {
            return true;
        }
    }

    return false;
}

const state = {
  cart: [],
  subTotal: 0,
  total: 0,
  tax: 0,
  showCart:false
};

const getters = {
  getCart: (state) => {
    return state.cart;
  },
  getTotal: (state) => {
    return { total: state.total, subTotal: state.subTotal, tax: state.tax };
  },
  isCartShown:(state)=>{
    return state.showCart;
  }
};

const actions = {
  async addToCart({ commit }, item) {
    commit("ADD_TO_CART", item);
  },

  async removeFromCart({ commit }, item) {
    commit("REMOVE_FROM_CART", item);
  },

  async clearCart({ commit }) {
    commit("CLEAR_CART");
  },

  async changeQuantity({ commit }, changeItem) {
    commit("CHANGE_QUANTITY", changeItem);
  },

  async calcTotal({ commit }) {
    let subTotalArr = [];
    let totalArr = [];
    let taxArr = [];
    state.cart.forEach((item) => {
      const subTotal =
        parseFloat(item.quantity) * parseFloat(item.item.unit_price);
      const total =
        parseFloat(item.quantity) * parseFloat(item.item.unit_price);
      const tax = total - subTotal;
      subTotalArr.push(subTotal);
      totalArr.push(total);
      taxArr.push(tax);
    });

    commit("SET_TOTAL", { subTotalArr, totalArr, taxArr });
  },

  async setCart({ commit }, { data,token }) {
    console.log(data)
   const ids = data.map(item=>item.product_details.id);
   await axios.post(`${productService}/products/get/updated/details`,{product_ids:ids},{headers:{'Authorization':`Bearer ${token}`}})
   .then(res=>{
    commit('SET_CART',{data,newData:res.data.product_data})
   })
  },

  async setCartNoUpdate({commit},data){
    commit('SET_CART_NO_UPDATE',{data})
  },

  async showCart ({commit}){
    commit('SHOW_CART');
  }
};

const mutations = {
  ADD_TO_CART: (state, item) => {
    var contains = containsObject(item, state.cart);

    if (!contains) {
      state.cart.unshift({ item, quantity: 1 });
    } else {
      var cartItem = state.cart.find((sitem) => sitem.item.id === item.id);
      var index = state.cart.indexOf(cartItem);
      if (
        parseInt(cartItem.item.quantity) -
          parseInt(cartItem.item.alert_quantity||5) >
        parseInt(cartItem.quantity)
      ) {
        cartItem.quantity++;
        state.cart[index] = {
          item: cartItem.item,
          quantity: cartItem.quantity,
        };
      }
    }
  },
  REMOVE_FROM_CART: async (state, item) => {
    var cartItem = state.cart.filter((sitem) => sitem.item !== item.item);
    state.cart = cartItem;
  },

  CLEAR_CART: (state) => {
    state.cart = [];
    state.total = 0;
  },

  CHANGE_QUANTITY: (state, changeItem) => {
    var cartItem = state.cart.find((sitem) => sitem.item.id === changeItem.id);
    var index = state.cart.indexOf(cartItem);
    if (
      parseInt(cartItem.item.quantity) -
        parseInt(cartItem.item.alert_quantity||5) >=
      parseInt(changeItem.value)
    ) {
      state.cart[index] = { item: cartItem.item, quantity: changeItem.value };
    }
  },
  SET_TOTAL: (state, { subTotalArr, totalArr, taxArr }) => {
    state.total = totalArr.reduce((a, b) => a + b, 0);
    state.subTotal = subTotalArr.reduce((a, b) => a + b, 0);
    state.tax = taxArr.reduce((a, b) => a + b, 0);
  },
  SET_CART: (state, {data,newData}) => {
    console.log(data,newData);
    newData.forEach((item)=>{
      var oldQuantity = data.find((old_item)=>{if(old_item.product_details.id === item.id){return old_item}}).quantity
      state.cart.push({item,quantity:oldQuantity});
    })
    // data.forEach((invItem) => {
    //   var newItem = {
    //     item: invItem.product_details,
    //     quantity: invItem.quantity,
    //   };
    //   state.cart.push(newItem);
    // });
  },

  SET_CART_NO_UPDATE:(state,{data})=>{
    console.log(data)
    state.cart =data;
  },

  SHOW_CART:(state)=>{
    if(state.showCart){
      state.showCart = false;
    } 
    else{
      state.showCart = true;
    }
  }
};

export default {
  state,
  getters,
  actions,
  mutations,
};
