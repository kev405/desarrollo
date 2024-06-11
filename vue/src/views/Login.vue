<template>
  <div
    class="w-6 flex justify-content-center align-items-center flex-wrap card-container fadein animation-duration-1000"
  >
    <div
      class="flex-1 w-6 h-22rem bg-green-500 border-round-left-3xl p-3"
      id="information-ds"
    >
      <div class="block mx-3 mt-3">
        <div class="block flex align-items-center justify-content-center mb-3">
          <i class="flex pi pi-building-columns text-white" style="font-size: 5rem" />
        </div>

        <div class="block flex align-items-center justify-content-center">
          <span class="flex text-lg text-white">EQUIPO DE DESARROLLO #6</span>
        </div>
      </div>

      <div class="block mx-3 mb-3">
        <div class="flex align-items-center justify-content-center">
          <span class="text-xs text-white"
            >Desarrollamos y cumplimos tus necesidades.</span
          >
        </div>
      </div>

      <div class="block m-3">
        <div class="flex align-items-center justify-content-center">
          <span class="text-white">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Nam odit recusandae
            aspernatur quasi repellat maxime. Alias, nulla nisi. Animi incidunt eius, sunt
            voluptatem rem provident obcaecati illum facere architecto dolor.
          </span>
        </div>
      </div>

      <div class="block m-3">
        <div class="flex align-items-center justify-content-center">
          <span class="text-xs text-white">* 2024 All rights reserved</span>
        </div>
      </div>
    </div>

    <div class="flex-1 w-6 h-22rem surface-ground border-round-right-3xl p-3">
      <div class="block m-3">
        <div class="flex align-items-center justify-content-center">
          <span class="text-xl font-bold">Bienvenido!</span>
        </div>
      </div>

      <div class="block m-3">
        <div class="flex align-items-center justify-content-center">
          <span class="text-600">Estamos felices de verte otra vez!</span>
        </div>
      </div>

      <!-- Sign in -->
      <div class="block m-3">
        <div class="block mb-3">
          <InputText
            type="text"
            v-model="email"
            class="w-full"
            placeholder="Correo electrónico"
          />
        </div>

        <div class="block mb-3">
          <Password
            v-model="password"
            class="w-full"
            placeholder="Contraseña"
            toggleMask
          />
        </div>

        <!-- div para el catcha -->
        <div class="block mb-3">
          <div class="flex justify-content-between flex-wrap">
            <div class="flex align-items-center justify-content-center">
              <Checkbox v-model="checked" :binary="true" inputId="remember-me" />
              <label for="remember-me" class="ml-2 text-xs text-600"> Recuerdame </label>
            </div>

            <div class="flex align-items-center justify-content-center">
              <span class="text-xs font-bold cursor-pointer hover:text-500">
                Has olvidado tu contraseña
              </span>
            </div>
          </div>
        </div>

        <div class="block mb-3">
          <Button
            @click="signIn()"
            class="w-full"
            label="Iniciar sesión otra vez marditasea"
            icon="pi pi-user"
            id="sign-in-button"
            :loading="signInLoading"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import InputText from 'primevue/inputtext'
import Checkbox from 'primevue/checkbox'
import Password from 'primevue/password'
import Button from 'primevue/button'

import { useAxios } from '@/composables/axios'
import { ref } from 'vue'
import { useUserStore } from '@/store/user'
import { storeToRefs } from 'pinia'

const { makeRequest, resultRequest } = useAxios()
const useUserVariables = useUserStore()
const { isLoged, userInfo, apiUrl } = storeToRefs(useUserVariables)

const email = ref('')
const password = ref('')
const signInLoading = ref(false)

const signIn = async () => {
  signInLoading.value = true

  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email.value,
      password: password.value,
    }),
  }

  try {
    const response = await fetch(apiUrl.value + 'user/login', requestOptions)

    if (!response.ok) {
      throw new Error('Error en la solicitud: ' + response.statusText)
    }

    const data = await response.json()

    if (data.success) {
      isLoged.value = true
      userInfo.value = data.user
    }
  } catch (error) {
    console.error(error)
  }

  signInLoading.value = false
}
</script>

<style lang="scss" scoped>
#sign-in-button {
  background-color: #1b1b2b !important;
  border: none !important;
}

// .p-inputtext, .p-component, .p-password-input {
//   width: 100% !important;
// }
// .p-password-panel, .p-password-meter, .p-password-info {
//   width: 100% !important;
// }

#information-ds {
  background-color: #3ca978 !important;
}

.p-password-info {
  width: 100% !important;
}
</style>
