<template>
    <div>
        <Row :gutter="20">
            <!-- <alert> 提示：暂时还未有折线图 </alert> -->
            <!-- <div style="margin: 10px; overflow: hidden;">
                <ul class="text-btn">
                    <li v-for="month in monthList" @click="handleMonth(month.text)" :key="month.text"><a :style="{'color': (selectMonth!=month.text? '#2d8cf0' : '#515a6e')}">{{ month.text }}</a></li>
                </ul>
            </div> -->
            <!-- <div style="margin: 10px; overflow: hidden">
            </div> -->
            <div style="height: 300px;">
                <chart-line
                    id="diskEchart-line"
                    :time="timeData"
                    :opData="opData"
                    :legend="cLegend"
                    :title="cTitle">
                </chart-line>
            </div>
            <div class="search-con search-con-top" style="margin-bottom:10px;">
                    <Input @on-change="handleClear" clearable place="请输入关键字全局搜索" class="search-input" v-model="searchValue"/>
                <Button @click="handleSearch" class="search-btn" type="primary">搜索</Button>

                <Date-picker 
                    type="daterange" 
                    placement="bottom-end" 
                    placeholder="日期范围" 
                    style="width: 200px; margin-left:20px;" 
                    @on-change="selectDate"
                >
                </Date-picker>
                
            </div>
            <Table
                size="small"
                ref="selection"
                border
                :columns="columns"
                :data="tableData"
            ></Table>

            <div style="margin: 10px; overflow: hidden">
                <div style="float: left;">
                <Page
                    :total="pageTotal"
                    :current="pageNum"
                    :page-size="pageSize"
                    :page-size-opts=[15,35,50,100,200,500]
                    show-sizer
                    show-total
                    @on-change="changePage"
                    @on-page-size-change="handlePageSize"
                ></Page>
                </div>
            </div>
        
        </Row>
    </div>
   
</template>

<script>
import { ChartLine } from "_c/charts"
import { 
    getReserverdList,
    getReservedDetail
} from '@/api/usage/resource.js'
// import { getTagList } from "@/api/cmdb2/tag.js";
// import { getIDClist } from "@/api/cmdb2/idc.js";
// import MultiAdd from "./multi_add_server";
import { mapState } from "vuex";
export default {
    components: {
        ChartLine
    },
    data() {
        return {
            loding: false,
            SSHloading: false,
            searchVal: "",
            pageNum: 1,
            pageTotal: 0,
            pageSize: 15,
            tableData: [],

            // datePick

            // select Part
            selectIns: {
                family: null,
                size: null,
                platform: null
            },
            

            // search part
            searchKey: "",
            searchValue: "",
            dateRange: [null,null],
            // chart
            timeData: [],
            // timeData: ['2020-03-01', '2020-03-02', '2020-03-03', '2020-03-04', '2020-03-05', '2020-03-06'],
            cLegend: {'current': '当前运行因子总和', 'purchased': '已购因子', 'coverage':'预留覆盖率'},
            cTitle: "预留实例使用情况",
            opData: {
                current: [],
                purchased: [],
                coverage: []
            },
            // opData: {
            //     'cpu': [0.22, 0.45, 0.23, 0.56, 0.53, 0.7],
            //     'memory': [0.32, 0.67, 0.56, 0.2, 0.76, 0.36],
            //     'disk': [0.856, 0.24, 0.62, 0.7, 0.124, 0.34]
            // },
            // 
            columns: [

                {
                    title: "系列",
                    key: "family",
                    minWidth: 180,
                    aligin: "center",
                    sortable: true,
                    render: (h, params) => {
                        return h(
                            "a",
                            {
                                on: {
                                    click: () => {
                                        this.handleDetail(params.row);
                                    }
                                }                          
                            },
                            params.row.family
                        );
                    }
                },
                {
                    title: "类型",
                    key: "size",
                    minWidth: 150,
                    aligin: "center",
                    sortable: true,
                },
                {
                    title: "操作系统",
                    key: "platform",
                    minWidth: 120,
                    aligin: "center",
                    sortable: false,
                },
                {
                    title: "当前运行(因子)总和",
                    key: "total_running",
                    minWidth: 160,
                    aligin: "center",
                    sortable: true,
                },
                {
                    title: "已购(因子)总和",
                    key: "total_ri",
                    minWidth: 140,
                    aligin: "center",
                    sortable: true,
                },
                {
                    title: "预留覆盖率(%)",
                    key: "coverage_rate",
                    minWidth: 120,
                    aligin: "center",
                    sortable: true,
                }
            ],

            //
            selectHost: "",
            selectMonth: "",

        };
    },
    methods: {
        //请求Web Terminal接口

        // 导出数据、支持分页、过滤、搜索、排序后导出
        exportData(type) {
            if (type === 1) {
                this.$refs.selection.exportCsv({
                filename: "codo_cmdb_original_data"
                });
            } else if (type === 2) {
                this.$refs.selection.exportCsv({
                filename: "codo_cmdb_sorting_and_filtering_data",
                original: false
                });
            } else if (type === 3) {
                this.$refs.selection.exportCsv({
                filename: "codo_cmdb_custom_data",
                columns: this.columns8.filter((col, index) => index < 4),
                data: this.data7.filter((data, index) => index < 4)
                });
            }
        },

       
        // 获取展示月份
        getDisplayMonthList() {
            getDisplayMonthList(this.auth_key).then(res => {
                if (res.data.code === 0) {
                    let tmpMonth = res.data.data
                    tmpMonth.forEach( ele => {
                        let tmp = ele.split(" ")[0].split('-')
                        this.monthList.push({
                            text: tmp[0]+"-"+tmp[1],
                            date: ele
                        })
                    })
                }
            })
            
        },

        // 获取资源列表
        getReservedList(key) {
            getReserverdList(this.pageNum, this.pageSize, key).then(res => {
                if (res.data.code === 0) {
                    this.pageTotal = res.data.count
                    this.tableData = res.data.data
                    console.log(res.data)
                } else {
                    this.$Message.error(`${res.data.msg}`);

                }
            })
        },
        getReservedDetail() {
            getReservedDetail(this.dateRange[0], this.dateRange[1], 
            this.selectIns.family, this.selectIns.size, this.selectIns.platform).then(res => {
                if (res.data.code === 0) {
                   this.timeData = []
                    this.opData = {
                            current: [],
                            purchased: [],
                            coverage: []
                    }
                    console.log(res.data)
                    if (res.data.count === 0) {
                        this.$Message.info("暂无此时间段使用情况");
                        this.cTitle = this.selectIns.family ? this.selectIns.family+ "(" + this.selectIns.platform + ")": "情况"
                    } else {
                        let totalData = res.data.data
                        this.cTitle = totalData[0].family + "(" + totalData[0].platform + ")" 
                        this.opData = {
                            current: [],
                            purchased: [],
                            coverage: []
                        }
                        totalData.forEach(ele => {
                            this.timeData.push(ele.date)
                            this.opData.current.push(ele.total_running)
                            this.opData.purchased.push(ele.total_ri)
                            this.opData.coverage.push(ele.coverage_rate)
                        })
                    }
                } else {
                    this.$Message.error(`${res.data.msg}`);
                }
            })
        },
        handleDetail(row) {
            this.selectIns = {
                family: row.family,
                size: row.size,
                platform: row.platform
            }
            this.getReservedDetail()
            
        },
        selectDate(dateRange) {
            this.dateRange = dateRange
            this.getReservedDetail()
        },

        // 折线图渲染
        handleChart(row) {
            getHostUsageDetail(this.auth_key, this.selectHost, this.selectMonth).then(res => {
                if (res.data.code === 0) {
                    this.timeData = []
                    this.opData = {
                        cpu: [],
                        disk: [],
                        memory: []
                    }
                    if (res.data.count === 0) {
                        this.$Message.info("暂无该月份使用情况");
                        this.cTitle = row? row.host_name + "(" + row.project_name + ")": "资源使用情况"

                    } else {
                        this.cTitle = res.data.data.ec2_info.host_name + "(" + res.data.data.ec2_info.project_name + ")" 
                        this.opData = {
                            cpu: [],
                            disk: [],
                            memory: []
                        }
                        let usageData = res.data.data.usage_list
                        usageData.forEach(ele => {
                            this.timeData.push(ele.date)
                            this.opData.cpu.push(ele.cpu_usage/100)
                            this.opData.disk.push(ele.disk_usage/100)
                            this.opData.memory.push(ele.mem_usage/100)
                        })
                    }
                } else {
                    this.$Message.error(`${res.data.msg}`);
                }
            })
            // this.selectMonth = text
            // let selectHost = key === null ? this.selectHost : this.tableData[0].id
            // getResourceUsage(selectHost, date).then(res => {
            //     if (res.data.code === 0) {
            //         this.opData = res.data.data
            //     } else {
            //         this.opData = {
            //             cpu: [],
            //             memory: [],
            //             disk: [] 
            //         }
            //     }
            // })
        },
    
        handleClear(e) {
            if (e.target.value === "") this.tableData = this.value;
        },
        handleSearch() {
            this.getReservedList(this.searchValue);
        },
        // 翻页
        changePage(value) {
            this.pageNum = value
            if (this.searchValue) {
                this.getReservedList(this.searchValue)
            } else {
                this.getReservedList()
            }
        },
        // 切换分页
        handlePageSize(value) {
            this.pageSize = value
            this.pageNum = 1
            if (this.searchValue) {
                getReservedList(this.searchValue)
            } else {
                getReservedList()
            }
            
        }
    },
    computed: {
    ...mapState({
      rules: state => state.user.rules
    }),
    },
    mounted() {
        // this.handleChart()
        // this.getTagList()
        // this.getAdminUserList()
        // this.getDisplayMonthList()
        this.getReservedList()
        // this.handleChart()
    }

};
</script>

<style lang="less" scoped>
.search-con {
  padding: 10px 0;
  .search {
    &-col {
      display: inline-block;
      width: 200px;
    }
    &-input {
      display: inline-block;
      width: 200px;
      margin-left: 2px;
    }
    &-btn {
      margin-left: 2px;
    }
  }
}
.date-btn {
    border-right:2px solid #515a6e;
    border-radius: 0;
    padding: 0 5px;
    // color: #dddddd;
    
    span {
        color : #2d8cf0;
        text-decoration:underline;
        font-size: 15px;
        padding: 0;
    }
}
.text-btn li{
    padding: 0;
    list-style: none;
    float:left;   
}
.text-btn  a {
    border-right: 2px solid #515a6e;
    color: #2d8cf0;
    padding: 0 10px;
    line-height: 1.35px;
    text-decoration: underline;
    font-size: 15px;
}
.text-btn a:hover {
    color: #5ea3f3;
}
.text-btn a:active {
    color: #515a6e;
}
</style>