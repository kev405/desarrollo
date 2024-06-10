<template>
  <div class="w-full h-full" id="main-page">
    <div
      v-if="!isLoged"
      class="w-full h-full m-0 flex justify-content-center align-items-center"
    >
      <Login />
    </div>

    <div v-if="isLoged">
      <PrincipalPage />
    </div>
  </div>
</template>

<script setup>
import PrincipalPage from '@/views/PrincipalPage'
import Login from '@/views/Login'

import { useUserStore } from '@/store/user'
import { storeToRefs } from 'pinia'

const useUserVariables = useUserStore()
const { isLoged } = storeToRefs(useUserVariables)
</script>

<style lang="scss" scoped>
#main-page {
  background-color: #1b1b2b !important;
}
</style>
