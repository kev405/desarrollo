<template>
  <div class="w-full">
    <div class="inline card flex justify-content-center m-3">
      <Chart type="pie" :data="chartData" :options="chartOptions" class="md:w-30rem" />
    </div>

    <div class="inline card flex justify-content-center m-3">
      <Chart
        type="bar"
        :data="chartDataBar"
        :options="chartOptionsBar"
        class="md:w-30rem"
      />
    </div>
  </div>
</template>

<script setup>
import Chart from 'primevue/chart'

import { ref, onMounted } from 'vue'

onMounted(() => {
  chartData.value = setChartData()
  chartOptions.value = setChartOptions()

  chartDataBar.value = setChartDataBar()
  chartOptionsBar.value = setChartOptionsBar()
})

const chartDataBar = ref()
const chartOptionsBar = ref()

const chartData = ref()
const chartOptions = ref()

const setChartDataBar = () => {
  const documentStyle = getComputedStyle(document.documentElement)

  return {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        type: 'bar',
        label: 'Labor 1',
        backgroundColor: documentStyle.getPropertyValue('--cyan-500'),
        data: [50, 25, 12, 48, 90, 76, 42],
      },
      {
        type: 'bar',
        label: 'Labor 2',
        backgroundColor: documentStyle.getPropertyValue('--gray-500'),
        data: [21, 84, 24, 75, 37, 65, 34],
      },
      {
        type: 'bar',
        label: 'Labor 3',
        backgroundColor: documentStyle.getPropertyValue('--orange-500'),
        data: [41, 52, 24, 74, 23, 21, 32],
      },
    ],
  }
}
const setChartOptionsBar = () => {
  const documentStyle = getComputedStyle(document.documentElement)
  const textColor = documentStyle.getPropertyValue('--text-color')
  const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary')
  const surfaceBorder = documentStyle.getPropertyValue('--surface-border')

  return {
    maintainAspectRatio: false,
    aspectRatio: 0.8,
    plugins: {
      tooltips: {
        mode: 'index',
        intersect: false,
      },
      legend: {
        labels: {
          color: textColor,
        },
      },
    },
    scales: {
      x: {
        stacked: true,
        ticks: {
          color: textColorSecondary,
        },
        grid: {
          color: surfaceBorder,
        },
      },
      y: {
        stacked: true,
        ticks: {
          color: textColorSecondary,
        },
        grid: {
          color: surfaceBorder,
        },
      },
    },
  }
}

const setChartData = () => {
  const documentStyle = getComputedStyle(document.body)

  return {
    labels: ['Tarea 1', 'Tarea 2', 'Tarea 3'],
    datasets: [
      {
        data: [540, 325, 702],
        backgroundColor: [
          documentStyle.getPropertyValue('--cyan-500'),
          documentStyle.getPropertyValue('--orange-500'),
          documentStyle.getPropertyValue('--gray-500'),
        ],
        hoverBackgroundColor: [
          documentStyle.getPropertyValue('--cyan-400'),
          documentStyle.getPropertyValue('--orange-400'),
          documentStyle.getPropertyValue('--gray-400'),
        ],
      },
    ],
  }
}

const setChartOptions = () => {
  const documentStyle = getComputedStyle(document.documentElement)
  const textColor = documentStyle.getPropertyValue('--text-color')

  return {
    plugins: {
      legend: {
        labels: {
          usePointStyle: true,
          color: textColor,
        },
      },
    },
  }
}
</script>

<style lang="scss" scoped></style>
