import { createApp } from 'vue'
import './assets/main.css'
import VNetworkGraph from "v-network-graph"
import "v-network-graph/lib/style.css"
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)
app.use(VNetworkGraph)

app.mount('#app')
