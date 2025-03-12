<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme

export default {
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '350px'
    },
    chartData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        this.setOptions(val)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.setOptions(this.chartData)
    },
    setOptions({ labels, datasets } = {}) {
      this.chart.setOption({
        xAxis: {
          data: labels,
          boundaryGap: false,
          axisTick: {
            show: false
          }
        },
        grid: {
          left: 10,
          right: 10,
          bottom: 20,
          top: 30,
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: [5, 10]
        },
        yAxis: {
          axisTick: {
            show: false
          }
        },
        legend: {
          data: datasets.map(dataset => dataset.label)
        },
        series: datasets.map(dataset => ({
          name: dataset.label,
          smooth: true,
          type: 'line',
          data: dataset.data,
          animationDuration: 2800,
          animationEasing: 'cubicInOut',
          areaStyle: {
            normal: {
              color: dataset.backgroundColor,
              opacity: 0.8
            }
          },
          itemStyle: {
            normal: {
              color: dataset.borderColor,
              lineStyle: {
                color: dataset.borderColor,
                width: 2
              }
            }
          }
        }))
      })
    }
  }
}
</script> 