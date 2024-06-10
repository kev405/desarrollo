<template>
  <div class="w-full fadein animation-duration-1000">
    <Toast />

    <DataTable
      :value="userList"
      tableStyle="min-width: 50rem"
      :lazy="true"
      :loading="loadingTable"
      :paginator="true"
      :rows="6"
      dataKey="id"
      :total-records="userList.length"
      responsive-layout="scroll"
    >
      <template #empty>
        <div class="flex justify-content-center">
          <div class="flex align-items-center justify-content-center">
            <span>No hay usuarios creados</span>
          </div>
        </div>
      </template>

      <template #header>
        <div class="justify-content-between flex">
          <Button
            type="button"
            icon="pi pi-refresh"
            class="p-button-rounded p-button-raised p-button-info mr-1"
            v-tooltip="'Recargar lista'"
            @click="getUserList()"
          />
          <div class="flex">
            <Button
              type="button"
              icon="pi pi-plus"
              class="p-button-rounded p-button-raised p-button-success mr-1"
              v-tooltip="'Añadir usuario'"
              @click="openForm('POST')"
            />
          </div>
        </div>
      </template>

      <Column
        v-for="col of dataTableColumns"
        :key="col.field"
        :field="col.field"
        :header="col.header"
      >
        <template #body="slotProps">
          <span v-if="col.field === 'actions'">
            <Button
              type="button"
              icon="pi pi-cog"
              aria-haspopup="true"
              @click="toggleMenu($event, slotProps.index, slotProps.data)"
            />
            <Menu
              :ref="
                (el) => {
                  if (el != null) {
                    menuActions['menuActions' + slotProps.index] = el
                  }
                }
              "
              :key="slotProps.index"
              :model="slotProps.data[col.field]"
              :popup="true"
              :hide="loadingTable"
            >
              <template #item="{ item }">
                <a @click="makeAction(item.action)" class="p-menuitem-link">
                  <span :class="['p-menuitem-icon', item.icon ?? 'pi pi-cog']"></span>
                  <span class="p-menuitem-text">{{ item.label }}</span>
                </a>
              </template>
            </Menu>
          </span>

          <span v-else class="text-center">{{ slotProps.data[col.field] }}</span>
        </template>
      </Column>
    </DataTable>

    <Dialog
      v-model:visible="showCreateUserView"
      :style="{ width: '450px' }"
      :header="headerUser"
      :modal="true"
      class="p-fluid"
      @after-hide="clearForm"
    >
      <div class="p-field mb-3">
        <span> Nombre </span>

        <InputText type="text" v-model="userName" class="w-full" placeholder="Nombre" />
      </div>

      <div class="p-field mb-3">
        <span> Correo electrónico </span>

        <InputText
          type="text"
          v-model="userEmail"
          class="w-full"
          placeholder="Correo electrónico"
        />
      </div>

      <div class="p-field mb-3">
        <span> Número de celular </span>

        <InputText
          type="text"
          v-model="phone"
          class="w-full"
          placeholder="Número de celular"
        />
      </div>

      <div class="p-field mb-3">
        <span> Rol </span>

        <Dropdown
          v-model="userRole"
          :options="roleOptions"
          optionLabel="name"
          placeholder="Seleccione un rol"
          class="w-full"
        />
      </div>

      <template #footer>
        <Button
          type="button"
          icon="pi pi-save"
          :label="headerUser"
          @click="createUser()"
          class="p-button-primary p-button-raised p-button-rounded"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import InputText from 'primevue/inputtext'
import DataTable from 'primevue/datatable'
import Dropdown from 'primevue/dropdown'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Menu from 'primevue/menu'

import { useAxios } from '@/composables/axios'
import { useToast } from 'primevue/usetoast'
import { useUserStore } from '@/store/user'
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'

const useUserVariables = useUserStore()
const { isLoged, apiUrl } = storeToRefs(useUserVariables)
const { makeRequest, resultRequest } = useAxios()
const toast = useToast()

const showCreateUserView = ref(false)
const loadingTable = ref(false)
const menuActions = ref({})
const headerUser = ref('')
const userList = ref([])
const userRole = ref('')
const userEmail = ref()
const method = ref('')
const userName = ref()
const phone = ref()

let record = Object

const dataTableColumns = ref([
  { field: 'id', header: 'ID' },
  { field: 'name', header: 'Nombre' },
  { field: 'roleRework', header: 'Rol' },
  { field: 'email', header: 'Correo electrónico' },
  { field: 'phone', header: 'Número de telefono' },
  { field: 'isActive', header: 'Estado del usuario' },
  { field: 'actions', header: 'Acciones' },
])
const actions = ref([
  {
    icon: 'pi pi-save',
    label: 'Actualizar usuario',
    action: 'update',
  },
  {
    icon: 'pi pi-trash',
    label: 'Desactivar usuario',
    action: 'delete',
  },
])
const roleOptions = ref([
  { name: 'Gerente', key: 'gerente' },
  { name: 'Director obra', key: 'director_obra' },
  { name: 'Capataz obra', key: 'capataz_obra' },
  { name: 'Peon', key: 'peon' },
  { name: 'Ayudante albañil', key: 'ayudante_albanil' },
])

const getUserList = async () => {
  loadingTable.value = true

  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  }
  try {
    const response = await fetch(apiUrl.value + 'users', requestOptions)

    if (!response.ok) {
      throw new Error('Error en la solicitud: ' + response.statusText)
    }

    const data = await response.json()
    userList.value = data

    Object.entries(userList.value).forEach((element) => {
      let user = userList.value[element[0]]

      switch (user.role) {
        case 'gerente':
          user.roleRework = 'Gerente'
          break
        case 'director_obra':
          user.roleRework = 'Director obra'
          break
        case 'capataz_obra':
          user.roleRework = 'Capataz obra'
          break
        case 'peon':
          user.roleRework = 'Peon'
          break
        case 'ayudante_albanil':
          user.roleRework = 'Ayudante albañil'
          break
        default:
          break
      }

      user.isActive = user.is_active === true ? 'Activo' : 'Desactivado'
      user.actions = actions.value
    })
  } catch (error) {
    console.error(error)
  }

  loadingTable.value = false
}

const createUser = async () => {
  let url = apiUrl.value + 'users'

  if (method.value === 'PUT') {
    url = apiUrl.value + 'users/' + String(record.id)
  }

  const requestOptions = {
    method: method.value,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: userEmail.value,
      name: userName.value,
      phone: phone.value,
      password: '123456',
      role: userRole.value.key,
      is_active: true,
      is_staff: true,
    }),
  }
  try {
    const response = await fetch(url, requestOptions)

    if (!response.ok) {
      throw new Error('Error en la solicitud: ' + response.statusText)
    }

    clearForm()
  } catch (error) {
    console.error(error)
  }
}

const deleteUser = async () => {
  const requestOptions = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
  }

  try {
    const response = await fetch(
      apiUrl.value + 'users/deactivate/' + String(record.id),
      requestOptions
    )

    if (!response.ok) {
      throw new Error('Error en la solicitud: ' + response.statusText)
    }

    getUserList()
  } catch (error) {
    console.error(error)
  }
}

const openForm = (methodToUse) => {
  showCreateUserView.value = true
  method.value = methodToUse
  headerUser.value = 'Crear usuario'
}

const clearForm = () => {
  userEmail.value = ''
  userName.value = ''
  phone.value = ''
  showCreateUserView.value = false
  getUserList()
}

const toggleMenu = (event, rowKey, rowData) => {
  menuActions.value['menuActions' + rowKey].toggle(event)
  record = rowData
}

const makeAction = (action) => {
  if (action === 'update') {
    method.value = 'PUT'

    userEmail.value = record.email
    userName.value = record.name
    phone.value = record.phone

    switch (record.role) {
      case 'gerente':
        userRole.value = { name: 'Gerente', key: 'gerente' }
        break
      case 'director_obra':
        userRole.value = { name: 'Director obra', key: 'director_obra' }
        break
      case 'capataz_obra':
        userRole.value = { name: 'Capataz obra', key: 'capataz_obra' }
        break
      case 'peon':
        userRole.value = { name: 'Peon', key: 'peon' }
        break
      case 'ayudante_albanil':
        userRole.value = { name: 'Ayudante albañil', key: 'ayudante_albanil' }
        break
      default:
        break
    }

    openForm('PUT')
    headerUser.value = 'Actualizar usuario'
  } else if (action === 'delete') {
    deleteUser()
  }
}

onMounted(() => {
  getUserList()
})
</script>
