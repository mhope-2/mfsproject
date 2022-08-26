import Vuex from 'vuex';

//Module Imports
import auth from './modules/auth';
import product from './modules/product';
import cart from './modules/cart.js';
import customers from './modules/customers';
import invoices from './modules/invoice';
import quotations from './modules/quotations';

export default new Vuex.Store({
    modules:{
        //All Modules Go Here
        auth,
        product,
        cart,
        customers,
        invoices,
        quotations
    }
})