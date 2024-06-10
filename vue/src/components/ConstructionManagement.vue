<template>
  <div class="w-full fadein animation-duration-1000">
    <DataTable
      :value="workList"
      tableStyle="min-width: 50rem"
      :lazy="true"
      :loading="loadingTable"
      :paginator="true"
      :rows="rowsTable"
      :page="pageTable"
      :rowsPerPageOptions="[5, 8]"
      :total-records="workList.length"
      dataKey="id"
      @page="onPage($event)"
      responsive-layout="scroll"
      class="p-datatable-sm"
    >
      <template #empty>
        <div class="flex justify-content-center">
          <div class="flex align-items-center justify-content-center">
            <span>La lista de obras está vacía</span>
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
            @click="getWorkList()"
          />
          <div class="flex">
            <Button
              type="button"
              icon="pi pi-plus"
              class="p-button-rounded p-button-raised p-button-success mr-1"
              v-tooltip="'Registrar obra'"
              @click="openForm()"
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
      v-model:visible="showAddWorkDialog"
      :style="{ width: '620px' }"
      :header="'Crear obra'"
      :modal="true"
      class="p-fluid"
      @after-hide="clearForm"
    >
      <div class="p-field mb-3">
        <div class="inline-block w-15rem mr-5">
          <span> Nombre de la obra </span>

          <InputText
            type="text"
            v-model="dialogFields['nameOfWork']"
            placeholder="Ingrese un nombre..."
            :disabled="createWorkLoading"
          />
        </div>

        <div class="inline-block w-15rem">
          <span> Dirección </span>

          <InputText
            type="text"
            v-model="dialogFields['direction']"
            placeholder="Ingrese una dirección"
            :disabled="createWorkLoading"
          />
        </div>
      </div>

      <div class="p-field mb-3">
        <div class="inline-block w-15rem mr-5">
          <span> Director </span>

          <Dropdown
            v-model="dialogFields['director']"
            :options="directorList"
            optionLabel="displayName"
            optionValue="id"
            placeholder="Seleccione un director..."
            :disabled="createWorkLoading"
          />
        </div>

        <div class="inline-block w-15rem">
          <span> Capataz </span>

          <Dropdown
            v-model="dialogFields['foreman']"
            :options="capatacesList"
            optionLabel="displayName"
            optionValue="id"
            placeholder="Seleccione un capataz..."
            :disabled="createWorkLoading"
          />
        </div>
      </div>

      <div class="p-field mb-3">
        <div class="inline-block w-15rem mr-5">
          <span> Peones </span>

          <MultiSelect
            v-model="dialogFields['powns']"
            :options="pownsList"
            optionLabel="displayName"
            optionValue="id"
            placeholder="Seleccione los peones..."
            :disabled="createWorkLoading"
          />
        </div>

        <div class="inline-block w-15rem">
          <span> Ayudantes </span>

          <MultiSelect
            v-model="dialogFields['helpers']"
            :options="helpersList"
            optionLabel="displayName"
            optionValue="id"
            placeholder="Seleccione los ayudantes..."
            :disabled="createWorkLoading"
          />
        </div>
      </div>

      <div class="p-field flex align-items-start mb-3">
        <div class="inline-block w-15rem mr-5">
          <span> Reporte </span>

          <Textarea
            v-model="dialogFields['report']"
            rows="5"
            cols="30"
            :disabled="createWorkLoading"
          />
        </div>

        <div class="inline-block w-15rem">
          <span> Estado </span>

          <Dropdown
            v-model="dialogFields['status']"
            :options="statusOptions"
            optionLabel="name"
            optionValue="code"
            placeholder="Seleccione un estado..."
            :disabled="createWorkLoading"
          />
        </div>
      </div>

      <template #footer>
        <Button
          type="button"
          icon="pi pi-save"
          label="Crear obra"
          class="p-button-primary p-button-raised p-button-rounded"
          @click="createWork()"
          :loading="createWorkLoading"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import MultiSelect from 'primevue/multiselect'
import InputText from 'primevue/inputtext'
import DataTable from 'primevue/datatable'
import Textarea from 'primevue/textarea'
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

const { makeRequest, resultRequest, empty } = useAxios()
const useUserVariables = useUserStore()
const { isLoged, apiUrl } = storeToRefs(useUserVariables)
const toast = useToast()

const rowsTable = ref(5)
const pageTable = ref(1)

const createWorkLoading = ref(false)
const showAddWorkDialog = ref(false)
const loadingTable = ref(false)
const capatacesList = ref([])
const directorList = ref([])
const dialogFields = ref({})
const helpersList = ref([])
const menuActions = ref({})
const pownsList = ref([])
const workList = ref([])

let record = Object

const dataTableColumns = ref([
  { field: 'id', header: 'ID' },
  { field: 'nombre', header: 'Nombre' },
  { field: 'direccion', header: 'Direción' },
  { field: 'estado', header: 'Estado' },
  { field: 'reporte', header: 'Reporte' },
  { field: 'actions', header: 'Acciones' },
])
const actions = ref([
  {
    icon: 'pi pi-pencil',
    label: 'Actualizar datos',
    action: 'edit',
  },
  {
    icon: 'pi pi-trash',
    label: 'Desactivar obra',
    action: 'delete',
  },
])
const statusOptions = ref([
  { name: 'Nueva', code: 'nueva' },
  { name: 'En desarrollo', code: 'en_desarrollo' },
  { name: 'Finalizada', code: 'finalizada' },
])

const getWorkList = async () => {
  loadingTable.value = true

  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  }
  try {
    const response = await fetch(apiUrl.value + 'work-management/', requestOptions)

    if (!response.ok) {
      throw new Error('Error en la solicitud: ' + response.statusText)
    }

    const data = await response.json()
    workList.value = data

    if (!empty(workList.value)) {
      Object.entries(workList.value).forEach((element) => {
        let work = workList.value[element[0]]
        work.actions = actions.value
      })
    }
  } catch (error) {
    console.error(error)
  }

  loadingTable.value = false
}

const disableWork = async () => {
  const requestOptions = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id: record.id,
    }),
  }

  try {
    const response = await fetch(
      apiUrl.value + 'work-management/' + String(record.id),
      requestOptions
    )

    if (!response.ok) {
      throw new Error('Error en la solicitud: ' + response.statusText)
    }

    getWorkList()
  } catch (error) {
    console.error(error)
  }
}

const getDirectors = async () => {
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  }

  try {
    const response = await fetch(apiUrl.value + 'users/get_directores/', requestOptions)

    if (!response.ok) {
      throw new Error('Error en la solicitud: ' + response.statusText)
    }

    const data = await response.json()
    directorList.value = data

    if (!empty(data)) {
      Object.entries(directorList.value).forEach((element) => {
        let director = directorList.value[element[0]]

        director.displayName = director.name + ' (' + director.email + ')'
      })
    }
  } catch (error) {
    console.error(error)
  }
}

const getCapataces = async () => {
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  }

  try {
    const response = await fetch(apiUrl.value + 'users/get_capataces/', requestOptions)

    if (!response.ok) {
      throw new Error('Error en la solicitud: ' + response.statusText)
    }

    const data = await response.json()
    capatacesList.value = data

    if (!empty(capatacesList.value)) {
      Object.entries(capatacesList.value).forEach((element) => {
        let foreman = capatacesList.value[element[0]]

        foreman.displayName = foreman.name + ' (' + foreman.email + ')'
      })
    }
  } catch (error) {
    console.error(error)
  }
}

const getHelpers = async () => {
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  }

  try {
    const response = await fetch(apiUrl.value + 'users/get_ayudantes/', requestOptions)

    if (!response.ok) {
      throw new Error('Error en la solicitud: ' + response.statusText)
    }

    const data = await response.json()
    helpersList.value = data

    if (!empty(helpersList.value)) {
      Object.entries(helpersList.value).forEach((element) => {
        let helper = helpersList.value[element[0]]
        helper.displayName = helper.name + ' (' + helper.email + ')'
      })
    }
  } catch (error) {
    console.error(error)
  }
}

const getPowns = async () => {
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  }

  try {
    const response = await fetch(apiUrl.value + 'users/get_peones/', requestOptions)

    if (!response.ok) {
      throw new Error('Error en la solicitud: ' + response.statusText)
    }

    const data = await response.json()
    pownsList.value = data

    if (!empty(pownsList.value)) {
      Object.entries(pownsList.value).forEach((element) => {
        let pown = pownsList.value[element[0]]
        pown.displayName = pown.name + ' (' + pown.email + ')'
      })
    }
  } catch (error) {
    console.error(error)
  }
}

const createWork = async () => {
  createWorkLoading.value = true
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      nombre: dialogFields.value.nameOfWork,
      direccion: dialogFields.value.direction,
      director: dialogFields.value.director,
      capataz: dialogFields.value.foreman,
      peones: dialogFields.value.powns,
      ayudantes: dialogFields.value.helpers,
      reporte: dialogFields.value.report,
      estado: dialogFields.value.status,
    }),
  }

  try {
    const response = await fetch(apiUrl.value + 'work-management/', requestOptions)

    if (!response.ok) {
      throw new Error('Error en la solicitud: ' + response.statusText)
    }

    dialogFields.value = {}
  } catch (error) {
    console.error(error)
  }
  createWorkLoading.value = false
}

const openForm = () => {
  getCapataces()
  getDirectors()
  getHelpers()
  getPowns()
  showAddWorkDialog.value = true
}

const clearForm = () => {
  showAddWorkDialog.value = false
  getWorkList()
}

const makeAction = (action) => {
  if (action === 'edit') {
    openForm()
  } else if (action === 'delete') {
    disableWork()
  }
}

const toggleMenu = (event, rowKey, rowData) => {
  menuActions.value['menuActions' + rowKey].toggle(event)
  record = rowData
}

const onPage = (event) => {
  const { filters, page, rows } = event

  rowsTable.value = rows
  pageTable.value = page
}

onMounted(() => {
  getWorkList()
})
</script>
