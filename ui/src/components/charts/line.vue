<template>
    <div ref="dom" class="charts chart-line"></div>
</template>>

<script>
import echarts from 'echarts'
import tdTheme from './theme.json'
import { on, off } from '@/libs/tools'
import { max, min } from 'moment';
echarts.registerTheme('tdTheme', tdTheme)
export default {
    name: 'ChartLine',
    props: {
        id: String,
        time: Array,
        opData: Object,
        title: String,
        legend: Object,
        formatter: String,
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
            let xAxisData = this.time;
            let clegend = Object.values(this.legend)
            let keys = Object.keys(this.legend)
            let seriesData = []

            for (let i = 0; i < keys.length; i++) { 
                seriesData.push({
                    name: clegend[i],
                    type: 'line',
                    smooth: false,
                    data: this.opData[keys[i]]
                })
            }
            console.log(this)
            let option = {
                title: {
                    text: this.title,
                    // x: 'center',
                    // y: 'bottom'
                },
                legend: {
                    data: clegend,
                    // x:'right',      //可设定图例在左、右、居中
                    // y:'bottom', 
                    // orient: 'vertical',
                    padding: [20,0,0,0]
                },
                tooltip: {
                    trigger: 'axis'
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: xAxisData,
                },
                yAxis: {
                    type: 'value',
                    axisLabel:  {
                        formatter:null
                    },
                    max: 1
                },
                series: seriesData
            }
            if (this.formatter === 'percentage') {
                option.yAxis.axisLabel.formatter = function(value,index){
                    return (value*100).toFixed(1)+'%';
                }
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
        opData() {
            this.$nextTick(()=>{
                if(this.opData){
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