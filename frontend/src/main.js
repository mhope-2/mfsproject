import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/index'


// Import the CSS or use your own!
import "vue-toastification/dist/index.css";

const options = {
  transition: "Vue-Toastification__bounce",
  maxToasts: 20,
  newestOnTop: true,
};

//Bootstrap Import
import "bootstrap-icons/font/bootstrap-icons.css"
import "bootstrap/dist/css/bootstrap.min.css"
import 'bootstrap'

import './assets/main.css'

const app = createApp(App)

app.use(router)
app.use(store)
app.mount('#app')
