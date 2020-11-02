<template>
    <div>
        <Row :gutter="20">
            <!-- <alert> 提示：暂时还未有折线图 </alert> -->
              <div style="margin: 10px; overflow: hidden;">
                <ul class="text-btn">
                    <li v-for="month in monthList" @click="handleMonth(month.text)" :key="month.text"><a :style="{'color': (selectMonth!=month.text? '#2d8cf0' : '#515a6e')}">{{ month.text }}</a></li>
                </ul>
            </div>
            <!-- <div style="margin: 10px; overflow: hidden">
                <Button type="text" class="date-btn" v-for="month in monthList" @click="handleChart(null,month.date)" :key="month.date"><span>{{ month.text }}</span></Button>
            </div> -->
            <div style="height: 300px;">
                <chart-line
                    id="diskEchart-line"
                    :time="timeData"
                    :opData="opData"
                    :legend="cLegend"
                    formatter="percentage"
                    :title="cTitle"
                    >
                </chart-line>
            </div>
            <div class="search-con search-con-top">
                <Input @on-change="handleClear" clearable place="请输入关键字全局搜索" class="search-input" v-model="searchValue"/>
                <Button @click="handleSearch" class="search-btn" type="primary">搜索</Button>
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
import { ChartPie, ChartBar, ChartLine } from "_c/charts"
// import Detail from "./server_detail";
// import {
//   getServerList,
//   getServerDetailList,
//   operationServer,
//   assetServerUpdate,
//   getTagtree,
//   getErrorLog,
//   syncServerToTagTree,
//   webterminnal,
// } from "@/api/cmdb2/server.js";
// import { getAdminUserList } from "@/api/cmdb2/admin_user"
import { 
    getResourceList,
    getResourceDetailList,
    getDisplayMonthList,
    getHostUsageDetail
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
            monthList: [],

            // search part
            searchKey: "",
            searchValue: "",

            // chart
            timeData: [],
            // timeData: ['2020-03-01', '2020-03-02', '2020-03-03', '2020-03-04', '2020-03-05', '2020-03-06'],
            cLegend: {'cpu': 'CPU利用率', 'memory': '内存利用率', 'disk':'磁盘利用率'},
            cTitle: "资源使用折线图",
            opData: {
                'cpu': [],
                'memory': [],
                'disk': []
            },
            // opData: {
            //     'cpu': [0.22, 0.45, 0.23, 0.56, 0.53, 0.7],
            //     'memory': [0.32, 0.67, 0.56, 0.2, 0.76, 0.36],
            //     'disk': [0.856, 0.24, 0.62, 0.7, 0.124, 0.34]
            // },
            // 
            columns: [
                {
                    type: "selection",
                    key: "id",
                    width: 60,
                    aligin: "center",
                    // render: (h, params) => {
                    //     return h(
                    //         "Checkbox",
                    //         {
                    //             on: {
                    //                 click: () => {
                    //                     this.handleDetail(params.row);
                    //                 }
                    //             }
                               
                    //         },
                    //     );
                    // }
                },
                {
                    title: "主机ID",
                    key: "ec2_id",
                    minWidth: 150,
                    aligin: "center",
                    sortable: true,
                    render: (h, params) => {
                        return h(
                            "a",
                            {
                                on: {
                                    click: () => {
                                        this.handleSelect(params.row);
                                    }
                                }
                               
                            },
                             params.row.ec2_id
                        );
                    }
                },
                {
                    title: "主机名",
                    key: "host_name",
                    minWidth: 150,
                    aligin: "center",
                    sortable: true,
                    render: (h, params) => {
                        return h(
                            "a",
                            {
                                on: {
                                    click: () => {
                                        this.handleSelect(params.row);
                                    }
                                }
                               
                            },
                             params.row.host_name
                        );
                    }
                },
                {
                    title: "所属项目",
                    key: "project_name",
                    minWidth: 180,
                    aligin: "center",
                    sortable: false,
                },
                {
                    title: "CPU使用率",
                    key: "cpu_avg_usage",
                    minWidth: 120,
                    aligin: "center",
                    sortable: true,
                },
                {
                    title: "内存使用率",
                    key: "mem_avg_usage",
                    minWidth: 120,
                    aligin: "center",
                    sortable: true,
                },
                {
                    title: "磁盘使用率",
                    key: "disk_avg_usage",
                    minWidth: 120,
                    aligin: "center",
                    sortable: true,
                },
                {
                    title: "当前机型",
                    key: "curr_inst_type",
                    minWidth: 140,
                    aligin: "center",
                    sortable: true,
                },
                {
                    title: "建议机型",
                    key: "suggest_inst_type",
                    minWidth: 140,
                    aligin: "center",
                    sortable: false,
                },
            ],

            //
            selectHost: "",
            selectMonth: "",

            auth_key: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODU5OTY2ODgsIm5iZiI6MTU4NTkxMDI0OCwiaWF0IjoxNTg1OTEwMjU4LCJpc3MiOiJhdXRoOiBzcyIsInN1YiI6Im15IHRva2VuIiwiaWQiOiIxNTYxODcxODA2MCIsImRhdGEiOnsidXNlcl9pZCI6IjEiLCJ1c2VybmFtZSI6ImFkbWluIiwibmlja25hbWUiOiJhZG1pbiIsImVtYWlsIjoiMTkxNzE1MDMwQHFxLmNvbSIsImlzX3N1cGVydXNlciI6dHJ1ZX19.mBJfMO7vRj10D-rjRk-VVjOXc4cz9I09Q1emOifv5K8"
        };
    },
    methods: {
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
            getDisplayMonthList().then(res => {
                if (res.data.code === 0) {
                    let tmpMonth = res.data.data
                    tmpMonth.forEach( ele => {
                        let tmp = ele.split(" ")[0].split('-')
                        this.monthList.push({
                            text: tmp[0]+"-"+tmp[1],
                            date: ele
                        })
                    })
                    this.selectMonth = this.monthList[this.monthList.length-1].text
                    console.log(this.selectMonth)
                }
            })
            
        },

        // 获取资源列表
        getResourceList(key) {
            let month = this.selectMonth ? this.selectMonth + '-01' : null
            getResourceList(this.pageNum, this.pageSize, month, key).then(res => {
                if (res.data.code === 0) {
                    this.pageTotal = res.data.count
                    this.tableData = res.data.data
                    console.log(res.data)
                } else {
                    this.$Message.error(`${res.data.msg}`);

                }
            })
        },
        // 点击主机ID或者主机名
        handleSelect(row) {
            this.selectHost = row.ec2_id
            this.handleChart(row)
        },
        // 月份选择
        handleMonth(month) {
            this.selectMonth = month
            this.handleChart()
            this.getResourceList()
        },
        // 折线图渲染
        handleChart(row) {
            getHostUsageDetail(this.selectHost, this.selectMonth).then(res => {
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
                        this.cTitle = res.data.data.ec2_info.host_name + "(" + res.data.data.ec2_info.ec2_id + ")" 
                        this.opData = {
                            cpu: [],
                            disk: [],
                            memory: []
                        }
                        let usageData = res.data.data.usage_list
                        usageData.forEach(ele => {
                            this.timeData.push(ele.date)
                            this.opData.cpu.push((ele.cpu_usage*0.01).toFixed(2))
                            this.opData.disk.push((ele.disk_usage*0.01).toFixed(2))
                            this.opData.memory.push((ele.mem_usage*0.01).toFixed(2))
                        })
                    }
                    console.log(this.opData,"00000000000000000")
                } else {
                    this.$Message.error(`${res.data.msg}`);
                }
        })
        },
    
        handleClear(e) {
            if (e.target.value === "") this.tableData = this.value;
        },
        handleSearch() {
            this.getResourceList(this.searchValue);
        },
      
        // 翻页
        changePage(value) {
            this.pageNum = value
             if (this.searchValue) {
                this.getResourceList(this.searchValue)
            } else {
               this.getResourceList() 
            }
        },
        // 切换分页
        handlePageSize(value) {
            this.pageSize = value
            this.pageNum = 1
            if (this.searchValue) {
                this.getResourceList(this.searchValue)
            } else {
               this.getResourceList() 
            }
            
        }
    },
    computed: {
    ...mapState({
      rules: state => state.user.rules
    }),
    },
    mounted() {
        this.handleChart()
        this.getDisplayMonthList()
        this.getResourceList()
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