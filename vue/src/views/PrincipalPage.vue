<template>
  <div class="w-full">
    <div class="w-full block">
      <Toolbar>
        <template #start>
          <div class="flex align-items-center gap-2">
            <img
              class="border-circle w-3rem h-3rem"
              src="../assets/img/company.jpeg"
              alt="company"
            />

            <span class="ml-3 text-white text-xl font-italic">{{
              tabSelected.label
            }}</span>
          </div>
        </template>

        <template #end>
          <div class="flex align-items-center gap-2">
            <Avatar
              image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png"
              style="width: 32px; height: 32px"
              class="cursor-pointer"
              @click="visibleLeft = true"
            />
          </div>

          <Sidebar
            v-model:visible="visibleLeft"
            :header="userInfo.name + ' (' + userInfo.role + ')'"
            position="right"
          >
            <ul class="list-none">
              <li class="mb-3">
                <div>
                  <a class="flex align-items-center cursor-pointer">
                    <span class="pi pi-cog hover:text-cyan-500" />
                    <span class="ml-2 text-900 hover:text-cyan-500">Settings</span>
                  </a>
                </div>
              </li>

              <li>
                <div>
                  <a
                    class="flex align-items-center cursor-pointer"
                    @click="isLoged = false"
                  >
                    <span class="pi pi-sign-out hover:text-cyan-500" />
                    <span class="ml-2 text-900 hover:text-cyan-500">Sign out</span>
                  </a>
                </div>
              </li>
            </ul>
          </Sidebar>
        </template>
      </Toolbar>
    </div>

    <div class="w-full block mt-3">
      <div class="card-container flex align-content-start">
        <div class="w-30rem inline-block p-3">
          <TieredMenu
            :model="tabsItems"
            style="background: #3ca978; border: #3ca978; height: 820px"
          >
            <template #item="{ item, props }">
              <a class="flex align-items-center" v-bind="props.action">
                <i
                  v-if="!empty(item.badge)"
                  v-badge="item.badge"
                  :class="item.icon + ' text-white hover:text-900'"
                />
                <i v-else :class="item.icon + ' text-white hover:text-900'" />
                <span class="ml-2 text-white hover:text-900">{{ item.label }}</span>
              </a>
            </template>
          </TieredMenu>
        </div>

        <div class="w-full inline-block p-3">
          <div class="flex justify-content-center flex-wrap">
            <div
              v-if="tabSelected.key === 'manage_user'"
              class="flex align-items-center justify-content-center"
            >
              <UserManagement />
            </div>

            <div
              v-if="tabSelected.key === 'construction_management'"
              class="flex align-items-center justify-content-center"
            >
              <ConstructionManagement />
            </div>

            <div
              v-if="tabSelected.key === 'dashboard'"
              class="flex align-items-center justify-content-center"
            >
              <Dashboard />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Dashboard from '@/components/Dashboard'
import UserManagement from '@/components/UserManagement'
import ConstructionManagement from '@/components/ConstructionManagement'

import TieredMenu from 'primevue/tieredmenu'
import Sidebar from 'primevue/sidebar'
import Toolbar from 'primevue/toolbar'
import Avatar from 'primevue/avatar'

import { useAxios } from '@/composables/axios'
import { ref } from 'vue'
import { useUserStore } from '@/store/user'
import { storeToRefs } from 'pinia'

const { makeRequest, resultRequest, empty } = useAxios()
const useUserVariables = useUserStore()
const { isLoged, userInfo } = storeToRefs(useUserVariables)

const tabSelected = ref({ label: 'Dashboard', key: 'dashboard' })
const visibleLeft = ref(false)

const tabsItems = ref([
  {
    label: 'Panel principal',
    icon: 'pi pi-chart-line',
    visible: true,
    command: () => {
      tabSelected.value = { label: 'Panel principal', key: 'dashboard' }
    },
  },
  {
    label: 'Gestion de usuarios',
    icon: 'pi pi-user-edit',
    visible: userInfo.value.role === 'gerente',
    command: () => {
      tabSelected.value = { label: 'Gestion de usuarios', key: 'manage_user' }
    },
  },
  {
    label: 'Task manage',
    icon: 'pi pi-list',
    visible: userInfo.value.role === 'director_obra',
    command: () => {
      tabSelected.value = { label: 'Task manage', key: 'task_manage' }
    },
  },
  {
    label: 'Work progres',
    icon: 'pi pi-hourglass',
    visible:
      userInfo.value.role === 'capataz_obra' ||
      userInfo.value.role === 'peon' ||
      userInfo.value.role === 'ayudante_albanil',
    command: () => {
      tabSelected.value = { label: 'Work progres', key: 'work_progress' }
    },
  },
  {
    label: 'Gestion de obras',
    icon: 'pi pi-share-alt',
    visible: userInfo.value.role === 'gerente' || userInfo.value.role === 'director_obra',
    command: () => {
      tabSelected.value = {
        label: 'Gestion de obras',
        key: 'construction_management',
      }
    },
  },
  {
    label: 'Progress manage',
    icon: 'pi pi-server',
    visible: userInfo.value.role === 'director_obra',
    command: () => {
      tabSelected.value = { label: 'Progress manage', key: 'progress_manage' }
    },
  },
  {
    label: 'Notificaciones',
    icon: 'pi pi-bell',
    badge: 2,
    visible: true,
    command: () => {
      tabSelected.value = { label: 'Notificaciones', key: 'notifications' }
    },
  },
])
</script>

<style lang="scss" scoped>
.p-toolbar {
  border-color: #1b1b2b !important;
  background: #1b1b2b !important;
}
</style>
