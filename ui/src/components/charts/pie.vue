<template>
  <div ref="dom" class="charts chart-pie"></div>
</template>

<script>
import echarts from 'echarts'
import tdTheme from './theme.json'
import { on, off } from '@/libs/tools'
echarts.registerTheme('tdTheme', tdTheme)
export default {
  name: 'ChartPie',
  props: {
    value: Array,
    text: String,
    subtext: String,
    pos: Array
  },
  data () {
    return {
      dom: null
    }
  },
  methods: {
    resize () {
      this.dom.resize()
    },
    initPie () {
      this.$nextTick(() => {
        let legend = this.value.map(_ => _.name)
        let option = {
          title: {
            text: this.text,
            subtext: this.subtext,
            x: this.pos[0],
            y: this.pos[1]
          },
          tooltip: {
            trigger: 'item',
            formatter: '{b} : <br/> {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            data: legend
          },
          series: [
            {
              type: 'pie',
              radius: '55%',
              center: ['80%', '70%'],
              data: this.value,
              labelLine: {
                show: false
              },
              label: {
                show: false,
                position: 'center'
              },
              itemStyle: {
                emphasis: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }
        this.dom = echarts.init(this.$refs.dom, 'tdTheme')
        this.dom.setOption(option)
        on(window, 'resize', this.resize)
      })
    }
  },
  mounted () {
    this.pos = ['center', 'top']
    this.initPie()
  },
  beforeDestroy () {
    off(window, 'resize', this.resize)
  }
}
</script>
