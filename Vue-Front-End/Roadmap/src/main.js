import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome' // <-- CRITICAL: The component to render icons

// 2. Import *All* Used Solid Icons (Cleaned list based on application needs)
import { 
    faUser, 
    faChevronLeft, 
    faChartLine, 
    faTrophy, 
    faHammer, 
    faGraduationCap, 
    faCogs, 
    faGem, 
    faClipboardList,
    faCheckCircle,
    faCheck,
    faPlay,
    faMapSigns
} from '@fortawesome/free-solid-svg-icons'

library.add(
    faUser, 
    faChevronLeft, 
    faChartLine, 
    faTrophy, 
    faHammer, 
    faGraduationCap, 
    faCogs, 
    faGem, 
    faClipboardList,
    faCheckCircle,
    faCheck,
    faPlay,
    faMapSigns
)

const app = createApp(App)

app.use(createPinia())
app.component('font-awesome-icon', FontAwesomeIcon) 
app.use(router)

app.mount('#app')
