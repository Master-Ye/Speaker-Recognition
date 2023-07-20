import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'virtual:windi.css'
import {Quasar} from 'quasar'
const app=createApp(App)
import router from './router'
app.use(router)
app.use(ElementPlus)
import '@quasar/extras/material-icons/material-icons.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { createPinia } from 'pinia'
import "~/router/permission.js"

  // 引入ECharts
import "echarts";
app.use(createPinia())
import store from "~/store/index.js"
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
import EChart from "vue-echarts";
import "@lottiefiles/lottie-player";
import DataVVue3 from '@kjgl77/datav-vue3'
app.component("v-chart", EChart);

app.use(DataVVue3)
app.use(store)
import "nprogress/nprogress.css"
import 'virtual:windi.css'
app.mount('#app')
