import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
    const apiUrl = ref('http://127.0.0.1:8000/api/')

    const isLoged = ref(false)
    const userInfo = ref({})

    return {
        isLoged,
        userInfo,
        apiUrl,
    }
})