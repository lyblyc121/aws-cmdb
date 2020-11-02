<template>
  <div>
    <Row :gutter="20">
      <i-col :xs="12" :md="8" :lg="4" key="infor-1" style="height: 90px;padding-bottom: 10px;">
        <infor-card shadow color="#E46CBB" icon="md-person-add" :icon-size="36">
          <h3><router-link :to="{name:'user'}" class="nav-link">用户管理</router-link></h3>
        </infor-card>
      </i-col>
      <i-col :xs="12" :md="8" :lg="4" key="infor-2" style="height: 90px;padding-bottom: 10px;">
        <infor-card shadow color="#2d8cf0" icon="md-cube" :icon-size="36">
          <h3><router-link :to="{name: 'asset_server'}" class="nav-link">资产管理</router-link></h3>
        </infor-card>
      </i-col>
      <i-col :xs="12" :md="8" :lg="4" key="infor-3" style="height: 90px;padding-bottom: 10px;">
        <infor-card shadow color="#19be6b" icon="ios-hammer" :icon-size="36">
          <h3><router-link :to="{name: 'resource_usage'}" class="nav-link">资源管理</router-link></h3>
        </infor-card>
      </i-col>
      <!-- <i-col :xs="12" :md="8" :lg="4" key="infor-3" style="height: 90px;padding-bottom: 10px;">
        <infor-card shadow color="#19be6b" icon="ios-hammer" :icon-size="36">
          <h3><router-link :to="{name: 'confd_project'}" class="nav-link">配置中心</router-link></h3>
        </infor-card>
      </i-col>
      <i-col :xs="12" :md="8" :lg="4" key="infor-3" style="height: 90px;padding-bottom: 10px;">
        <infor-card shadow color="#19be6b" icon="ios-hammer" :icon-size="36">
          <h3><router-link :to="{name: 'confd_project'}" class="nav-link">配置中心</router-link></h3>
        </infor-card>
      </i-col>
      <i-col :xs="12" :md="8" :lg="4" key="infor-4" style="height: 90px;padding-bottom: 10px;">
        <infor-card shadow color="#9A66E4" icon="ios-alarm" :icon-size="36">
          <h3><router-link :to="{name: 'cronjobs'}" class="nav-link">定时任务</router-link></h3>
        </infor-card>
      </i-col>
      <i-col :xs="12" :md="8" :lg="4" key="infor-5" style="height: 90px;padding-bottom: 10px;">
        <infor-card shadow color="#ff9900" icon="ios-alarm" :icon-size="36">
          <h3><router-link :to="{name: 'paid_reminder'}" class="nav-link">提醒管理</router-link></h3>
        </infor-card>
      </i-col>
      <i-col :xs="12" :md="8" :lg="4" key="infor-6" style="height: 90px;padding-bottom: 10px;">
        <infor-card shadow color="#ed3f14" icon="md-warning" :icon-size="36">
          <h3><router-link :to="{name: 'prometheus_alert'}" class="nav-link">kubernetes告警</router-link></h3>
        </infor-card>
      </i-col> -->
    </Row>


    <Row :gutter="20" style="margin-top: 10px;">
      <i-col :md="24" :lg="12" style="margin-bottom: 10px;">
        <Card shadow>
          <!-- <IssuesInfo :data="IssuesInfoData"></IssuesInfo> -->
          <h1 class="home-title">当月资源使用率</h1>
          <chart-line 
            style="height: 340px; font-size:15px" 
            :time="lineResUsage.xAxis"
            :opData="lineResUsage.yAxis"
            :legend="lineResUsage.legend"
            formatter="percentage" 
            title=""/>
          <Sliders 
            style="height: 30px;"
            :value="resId"
            @watchChild="handleChart">
          </Sliders>
        </Card>
      </i-col>

      <i-col :md="24" :lg="12" style="margin-bottom: 10px;">
        <Card shadow>
          <h1 class="home-title">账单组成</h1>
          <div style="overflow:hidden">
          <i-select 
          :model.sync="model1" 
          style="width:70px; height:50px; margin:0px auto 0px auto; float:right;" 
          placeholder="月份"
          @on-change="billMonthHandler">
            <i-option v-for="item in monthList" :value="item.value">{{ item.label }}</i-option>
          </i-select>
          </div>
          <chart-pie ref="childBillCon" style="height: 300px;" :value="pieBillConData" :pos="pos"></chart-pie>
          <h4 style="text-align: center; height: 20px; font-weight:normal; color:#2D8cF0;"> {{pieBillConText}} </h4>
        </Card>
      </i-col>
    </Row>

    <Row :gutter="20" style="margin-top: 10px;">
      <i-col :md="24" :lg="12" style="margin-bottom: 10px;">
      <Card shadow>
          <h1 class="home-title">当月预留实例情况</h1>
          <chart-line 
            style="height: 340px; font-size:15px" 
            :time="lineReserved.xAxis"
            :opData="lineReserved.yAxis"
            :legend="lineReserved.legend"
            formatter="percentage"/>
          <Sliders 
            style="height: 30px;"
            :value="reservedId"
            @watchChild="handleReserved">
          </Sliders>
        </Card>
      </i-col>
      

      <i-col :md="24" :lg="12" style="margin-bottom: 10px;">
        <Card shadow>
          <h1 class="home-title" style="display:inline; text-align:left;">月度账单</h1>
          <div style="overflow:hidden; margin-top: 20px; display:inline;">
            <i-select 
              :model.sync="model2" 
              style="width:120px; height:50px; float:right;padding:0 10px;" 
              placeholder="选择服务"
              @on-change="billServiceHandler">
              <i-option v-for="item in serviceList" :value="item">{{ item }}</i-option>
            </i-select>
            <i-select 
              :model.sync="model3" 
              style="width:120px; height:50px; padding:0 10px;float:right;" 
              placeholder="年份"
              @on-change="billServiceHandler">
              <i-option v-for="item in yearList" :value="item">{{ item }}</i-option>
            </i-select>
          </div>
          <chart-single-line
            style="height: 340px; font-size:15px" 
            :value="serviceBillData" 
            title=""/>
          <h4 style="text-align: center; display:block; height: 15px; font-weight:normal; color:#2D8cF0; margin-top:15px;"> {{annualBillTitle}} </h4>
        </Card>
      </i-col>

    </Row>

      <Row :gutter="20" style="margin-top: 10px;">
      <i-col :md="24" :lg="24" style="margin-bottom: 10px;">
        <Card shadow>
          <IssuesInfo :data="IssuesInfoData"></IssuesInfo>
          <!-- <chart-bar style="height: 340px;" :value="barTaskData" text="告警预留位"/> -->
        </Card>
      </i-col>
    </Row>

  </div>
</template>

<script>
import InforCard from '_c/info-card'
import Sliders from '_c/slider'
import CountTo from '_c/count-to'
import { ChartPie, ChartBar, ChartLine, ChartSingleLine} from '_c/charts'
import Example from './example.vue'
import { getTagList, getTaskOrderlist, getTaskStatementlist } from '@/api/dashboard/home.js'
import { getZabbixLastissues } from "@/api/devops-tools";
import TaskInfo from './taskinfo'
import IssuesInfo from './issuesinfo'
import {
  getHostUsageDetail,
  getResourceList,
  getReserverdList,
  getReservedDetail
} from '@/api/usage/resource.js'
import {
  getTotalBillMonthly,
  getDisplaySerYear,
  getServiceBill
} from '@/api/usage/bill.js'
// import { getTaskCheckHistorylist } from '@/api/task'

export default {
  name: 'home',
  components: {
    InforCard,
    ChartPie,
    ChartBar,
    ChartLine,
    ChartSingleLine,
    Example,
    TaskInfo,
    IssuesInfo,
    Sliders
  },
  data () {
    return {
      lineResUsage: {
        xAxis: [],
        yAxis: {},
        legend: {
          'cpu': 'CPU利用率', 
          'memory': '内存利用率', 
          'disk':'磁盘利用率'
          }
      },
      resId: "",
      resList: [],
      currentItem: 0,

      currentReserved: 0,
      lineReserved: {
        xAxis: [],
        yAxis: {},
        legend: {
          'current': '当前运行因子总和', 
          'purchased': '已购因子', 
          'coverage':'预留覆盖率'
        }
      },
      reservedList: [],
      reservedId: "",
      // reservedInfo: Object,

      // cardData: {
      //   users: 0,
      //   cmdb: 0,
      //   project: 0,
      //   alarm: 0,
      //   remind: 0,
      //   crontab: 0
      // },
      pieCmdbData: [],
      pieTaskData: [],
      taskInfoData: [],
      pieBillConData: [],
      pieBillConText: '账单组成',
      pos: ['center', 'bottom'],
      // IssuesInfoData: [{
      //   "host": "samonitor",
      //   "issue": "Zabbix agent on us_samonitor is unreachable for 5 minutes",
      //   "last_change": "2019-07-08 13:46:51",
      //   "level": '3',
      // }
      // ],
      IssuesInfoData: [],
      barTaskData: {
        Mon: 9,
        Tue: 2,
        Wed: 45,
        Thu: 32,
        Fri: 5,
        Sat: 30,
        Sun: 7
      },

      // 账单组成
      model1: '',
      monthList: [
        {
          value: 'Jan',
          label: '1月'
        },
        {
          value: 'Feb',
          label: '2月'
        },
        {
          value: 'Mar',
          label: '3月'
        },
        {
          value: 'Apr',
          label: '4月'
        },
        {
          value: 'May',
          label: '5月'
        },
        {
          value: 'Jun',
          label: '6月'
        },
        {
          value: 'Jul',
          label: '7月'
        },
        {
          value: 'Aug',
          label: '8月'
        },
        {
          value: 'Sep',
          label: '9月'
        },
        {
          value: 'Oct',
          label: '10月'
        },
        {
          value: 'Nov',
          label: '11月'
        },
        {
          value: 'Dec',
          label: '12月'
        }
      ],
      monthDict: {
        Jan: 1,
        Feb: 2,
        Mar: 3,
        Apr: 4,
        May: 5,
        Jun: 6,
        Jul: 7,
        Aug: 8,
        Sep: 9,
        Oct: 10,
        Nov: 11,
        Dec: 12,
      },
      curDate: null,

      // 月账单
      model2: '',
      serviceList: [],
      model3: '',
      yearList: [],
      serviceBillData: [],
      pickedYear: null,
      pickedService: 'EC2',
      annualBillTitle: '2020年EC2每月账单'

    }
  },
  methods: {
    // 获取zabbix last issues
    GetZabbixLastissues(){
      getZabbixLastissues().then(res => {
        if (res.data.code === 0) {
          const data = res.data.data
          // const slice_data = data.slice(0,10)
          this.IssuesInfoData = data
        }
      })
    },

    //初始化 历史任务类型饼图数据
    initPieTask () {
      // this.pieTaskData.push({name: '服务器发布', value:20},{name: '资源申请', value:20},{name: 'MySQL审核', value:20},{name: '自定义任务', value:50},)
      getTaskStatementlist().then(res => {
        if (res.data.code === 0) {
            const data = res.data.data
            // 切割下列表，历史任务可能有很多，限制
            const slice_data = data.slice(0,36)
            for (var item in slice_data) {
              this.pieTaskData.push({
                value: data[item].task_len,
                name: data[item].task_type
              })
            }
        } else {
          // this.$Message.error(`${res.data.msg}`)
        }
      })
    },

    // 初始化 CMDB Tag饼图数据
    initPieCmdb () {
      // this.pieCmdbData.push({name: '服务器发布', value:20},{name: '资源申请', value:20},{name: 'MySQL审核', value:20},{name: '自定义任务', value:50},)

      getTagList().then(res => {
        if (res.data.code === 0) {
            const data = res.data.data
            // 切割下列表，历史任务可能有很多，做个限制
            const slice_data = data.slice(0,36)
            for (var item in slice_data) {
              this.pieCmdbData.push({
                value: data[item].server_len,
                name: data[item].tag_name
              })
            }
        } else {
          // this.$Message.error(`${res.data.msg}`)
        }
      })
    },

    // 初始化 [待处理任务订单]
    initTaskInfo () {
      getTaskOrderlist().then(res => {
        const data = res.data.data
        for (var item in data) {
          this.taskInfoData.push({
            id: data[item].list_id,
            name: data[item].task_name + '-' + data[item].task_type,
            creator: data[item].creator,
            status: data[item].status
          })
        }
      })
    },

    // 初始化 账单组成
    initBillCon (month) {
      this.pieBillConData = []
      // this.pieBillConData.push({name: 'EC2', value:199.8},{name: 'RDS', value: 299.7},{name: 'S3', value:418.9})
      getTotalBillMonthly(month).then(res => {
        if (res.data.code === 0) {
          const data = res.data.data
          data.forEach(ele => {
            this.pieBillConData.push({
              name: ele.product_code,
              value: ele.total_cost
            })
          })
          if (data.length == 0) {
            let tmpMonth = this.curDate.getFullYear().toString() + '年' + (this.curDate.getMonth() + 1).toString()
            if (month) {
              this.pieBillConText = '暂无'+ month + '月账单'
            }
            else this.pieBillConText = '暂无'+ tmpMonth + '月账单'
            
          } else {
            this.pieBillConText = data[0].start_date.substring(0,7) + "账单组成"
          }
          
        }
      })
    },
    
    // 切换月份账单组成
    billMonthHandler (element) {
      let tmpMonth = this.monthDict[element]
      let tmpMonthStr = tmpMonth < 10 ? '0' + tmpMonth.toString() : tmpMonth.toString()
      tmpMonth = (this.curDate.getMonth() + 1 > tmpMonth) ? this.curDate.getFullYear().toString() + '-' + tmpMonthStr : (this.curDate.getFullYear()-1).toString() + '-' +  tmpMonthStr
      this.initBillCon(tmpMonth)
    },

    // 初始化月账单的服务选项和年份选项
    initYearBillData (service, year) {
      this.serviceBillData = []
      getServiceBill(service, year).then(res => {
        if (res.data.code === 0) {
          let data = res.data.data
          data.forEach(ele => {
            this.serviceBillData.push({
              text: ele.month,
              value: ele.total_cost
            })
          })
          this.annualBillTitle = + this.pickedYear + '年' + this.pickedService +'每月账单'
        } 
      })
    },

    getDisplaySerYear () {
       getDisplaySerYear().then(res => {
        if (res.data.code === 0) {
          this.serviceList = res.data.data.products
          this.yearList = res.data.data.years
          // this.pickedYear = this.curDate.getFullYear().toString()
          // this.pickedService = this.serviceList.length > 0 ? this.serviceList[0] : 'AmazonEC2'
        }
      })
      
    },

    // 切换服务年内月度账单趋势
    billServiceHandler (element) {
      // 服务
      if (isNaN(element)) {
        this.pickedService = element
      } else {
        // 年份
        this.pickedYear = element
      }
      this.initYearBillData(this.pickedService, this.pickedYear)
    },

    // 处理预留实例的下方主机切换
    handleReserved (ele) {
      if (ele === "1") {
        this.currentReserved += 1
        if (this.currentReserved  === this.reservedList.length) {
          this.currentReserved = 0
        }
      } else {
        this.currentReserved -= 1
         if (this.currentReserved  === -1) {
          this.currentReserved = this.reservedList.length -1 
        }
      }
      this.getReservedDetail(this.reservedList[this.currentReserved])
    },

    // 处理当月使用情况下方主机切换
    handleChart (ele) {
      if (ele === "1") {
        this.currentItem += 1
        if (this.currentItem  === this.resList.length) {
          this.currentItem = 0
        }
      } else {
        this.currentItem -= 1
         if (this.currentItem  === -1) {
          this.currentItem = this.resList.length -1 
        }
      }
      this.getHostUsageDetail(this.resList[this.currentItem])
    },

    // 初始化 资源实例下方展示列表
    initResUsage () {
      getResourceList().then(res => {
        if (res.data.code === 0) {
          let result = res.data.data
          result.forEach(ele => {
            this.resList.push(ele.ec2_id)
          })
          if (this.resList.length > 0) {
            this.getHostUsageDetail(this.resList[0])
          }
        }
      })      
    },

    // 获取当月该主机使用情况
    getHostUsageDetail (ec2_id) {
       getHostUsageDetail(ec2_id).then(res => {
        if (res.data.code === 0) {
          if (res.data.count > 0) {
            this.lineResUsage.xAxis = []
            this.lineResUsage.yAxis = {
              cpu: [],
              disk: [],
              memory: []
            }
            this.resId = res.data.data.ec2_info.host_name + "(" + res.data.data.ec2_info.project_name + ")"
            let usageData = res.data.data.usage_list
            usageData.forEach(ele => {
                this.lineResUsage.xAxis.push(ele.date)
                this.lineResUsage.yAxis.cpu.push((ele.cpu_usage*0.01).toFixed(2))
                this.lineResUsage.yAxis.disk.push((ele.disk_usage*0.01).toFixed(2))
                this.lineResUsage.yAxis.memory.push((ele.mem_usage*0.01).toFixed(2))
            })
          } else {
          this.resId = res.data.data.ec2_info.host_name + "(" + res.data.data.ec2_info.project_name + ")"
          this.lineResUsage.xAxis = []
          this.lineResUsage.yAxis = {
            cpu: [],
            disk: [],
            memory: []
          }
        }
        } 
      })
    },

    // 初始化 预留实例列表
    initReserved () {
      getReserverdList().then(res => {
        if (res.data.code === 0) {
          let result = res.data.data
          result.forEach(ele => {
            this.reservedList.push({
              family: ele.family,
              size: ele.size,
              platform: ele.platform
            })
          })
          if (this.reservedList.length > 0) {
            this.getReservedDetail(this.reservedList[0])
          } else {
            this.getReservedDetail({family:null,size:null, platform:null})
          }
        }
      })
    },

    // 获取当月该预留实例使用情况
    getReservedDetail (reservedInfo) {
       getReservedDetail(reservedInfo.family, reservedInfo.size, reservedInfo.platform).then(res => {
        if (res.data.code === 0) {
          if (res.data.count > 0) {
            
            this.lineReserved.xAxis = []
            this.lineReserved.yAxis = {
              current: [],
              purchased: [],
              coverage: []
            }
            this.reservedId = reservedInfo.family + "(" + reservedInfo.platform + ")"
            let usageData = res.data.data
            usageData.forEach(ele => {
                this.lineReserved.xAxis.push(ele.date)
                this.lineReserved.yAxis.current.push(ele.total_running)
                this.lineReserved.yAxis.purchased.push(ele.total_ri)
                this.lineReserved.yAxis.coverage.push(ele.coverage_rate)
            })
          } else {
            this.lineReserved.xAxis = []
            this.lineReserved.yAxis = {
              current: [],
              purchased: [],
              coverage: []
            }
            this.reservedId = reservedInfo.family + "(" + reservedInfo.platform + ")"
          }
        } 
      })
    }
  },
  mounted () {
    // this.initPieCmdb()
    // this.initTaskInfo()
    // this.initPieTask()
    // this.GetZabbixLastissues()
    this.curDate =new Date()
    this.initResUsage()
    this.initReserved()
    this.initBillCon()
    this.getDisplaySerYear()
    this.initYearBillData()
    
  },
  watch: {
    pieBillConData: function() {
      this.$refs.childBillCon.initPie()
    },
    pieCmdbData: function () {
      this.$refs.childCmdb.initPie()
    },
    pieTaskData: function () {
      this.$refs.childTask.initPie()
    }
  }
}
</script>

<style lang="less">
.count-style{
  font-size: 50px;
}
.home-title {
  font-size: 18px;
  color: #516b91;
  text-align: center;
}
</style>