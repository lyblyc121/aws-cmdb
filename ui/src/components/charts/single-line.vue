<template>
    <div ref="dom" class="charts chart-line"></div>
</template>>

<script>
import echarts from 'echarts'
import tdTheme from './theme.json'
import { on, off } from '@/libs/tools'
echarts.registerTheme('tdTheme', tdTheme)
export default {
    name: 'ChartSingleLine',
    props: {
        value: Array,
        title: String
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
        init() {
            console.log(this.value)
            let xLabel = this.value.map( _ => _.text)
            console.log(xLabel)
            let option = {
                xAxis: {
                    type: 'category',
                    data: xLabel
                },
                yAxis: {
                    type: 'value'
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '10%',
                    top:'5%',
                    containLabel: false
                },
                series: [{
                    data: this.value,
                    type: 'line'
                }]
            }
            this.dom = echarts.init(this.$refs.dom, 'tdTheme')
            this.dom.setOption(option,true)
            on(window, 'resize', this.resize)
        }
    },
    mounted () {
        this.$nextTick(()=>{
            this.init()
        })
    },
    beforeDestroy () {
        off(window, 'resize', this.resize)
    },
    watch: {
        value() {
            this.$nextTick(()=>{
                if(this.value){
                    this.init()
                }
            })
        }
    }
}
</script>

<style scoped>
.chart-line {
    width: 100%;
    height: 100%;
}
</style>