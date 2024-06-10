import '@/assets/scss/main.scss'

import { createApp } from 'vue'
import { createPinia } from "pinia"

import App from './App.vue'
import router from './router'
import store from './store'

import ToastService from 'primevue/toastservice'
import PrimeVue from 'primevue/config'

import ConfirmationService from 'primevue/confirmationservice'
import BadgeDirective from 'primevue/badgedirective'
import StyleClass from 'primevue/styleclass'
import Tooltip from 'primevue/tooltip'
import Ripple from 'primevue/ripple'

const app = createApp(App)

app.use(ConfirmationService)
app.use(BadgeDirective)
app.use(createPinia())
app.use(ToastService)
app.use(PrimeVue)
app.use(store)
app.use(router)

app.directive('ripple', Ripple)
app.directive('styleclass', StyleClass)
app.directive('tooltip', Tooltip)
app.directive('badge', BadgeDirective)

app.mount('#app')
