<template>
    <div>
        <Row :gutter="20">
            <!-- <alert> 账单分摊还未完善！</alert>
            <Tabs type="card" @on-click="handleTabChange">
                <Tab-pane  :label="month.text"></Tab-pane>
            </Tabs> -->
            <div style="margin: 10px; overflow: hidden;">
                <DatePicker type="month" :value="new Date()"  placeholder="选择月份" style="width: 200px" @on-change="handleChange"></DatePicker>
            </div>
            <div style="margin: 10px; overflow: hidden;">
                <ul class="text-btn">
                    <li v-for="type in resType" :key="type.id" @click="handleBillType(type.id)"><a :style="{'color': (selectType!=type.id? '#2d8cf0' : '#515a6e')}">{{ type.text}}</a></li>
                </ul>
            </div>
            <Table
                size="small"
                :columns="columns"
                :data="tableData"
                border
            ></Table>
            <div style="margin: 10px; overflow: hidden">
                <div style="float: left;">
                    <Page
                        :total="pageTotal"
                        :current="pageNum"
                        :page-size="pageSize"
                        :page-size-opts=[18,35,50,100,200,500]
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
import { mapState } from "vuex";
import { getBillList } from "@/api/cmdb2/bill.js"
export default {
    data() {
        return {
            selectType: 0,
            value:'三月',
            monthList: [
            {
                text: '1月',
                date: new Date(2020,1,1)
            },
            {
                text: '2月',
                date: new Date(2020,2,1)
            },
            {
                text: '3月',
                date: new Date(2020,3,1)
            }
            ],  
            selectMonth: Date(),

            columns: [
                {
                    title: "主机ID",
                    key: "hostid",
                    minWidth: 150,
                    align: "center",
                    sortable: true,
                },
                {
                    title: "主机名",
                    key: "hostname",
                    minWidth: 150,
                    align: "center",
                    sortable: true,
                },
                {
                    title: "所属项目",
                    key: "project",
                    minWidth: 160,
                    align: "center",
                    sortable: true,
                },
                {
                    title: "按需",
                    key: "require",
                    width: 100,
                    align: "center",
                    sortable: true,
                },
                {
                    title: "预留",
                    key: "prepare",
                    width: 100,
                    align: "center",
                    sortable: true,
                },
                {
                    title: "S3",
                    key: "store",
                    width: 100,
                    align: "center",
                    sortable: true,
                },
                {
                    title: "网络流量",
                    key: "netflow",
                    width: 120,
                    align: "center",
                    sortable: true,
                },
                {
                    title: "Config",
                    key: "config",
                    width: 120,
                    align: "center",
                    sortable: true,
                },
                {
                    title: "CloudWatch",
                    key: "cloudwatch",
                    minWidth: 160,
                    align: "center",
                    sortable: true,
                },
                {
                    title: "EBS",
                    key: "ebs",
                    width: 100,
                    align: "center",
                    sortable: true,
                },
                {
                    title: "总计",
                    key: "total",
                    width: 100,
                    align: "center",
                    sortable: true,
                }
            ],
            tableData: [],
            resType: [
                {
                    id: 'EC2',
                    text: 'EC2'
                },
                {
                    id: 'RDS',
                    text: 'RDS'
                },
                {
                    id: 'EBS',
                    text: 'EBS'
                },
                {
                    id: 'Elc',
                    text: 'ElastiCache'
                },
                {
                    id: 'tobill',
                    text: '总账单'
                },
                // {
                //     id: 'resman',
                //     text: '资源管理'
                // },
                // {
                //     id: 'upbill',
                //     text: '更新计费'
                // }
            ],

            //
            pageTotal: 0,
            pageNum: 1,
            pageSize: 15
        }
    },
    methods: {
        handleBillType(type) {
            this.selectType = type
            this.getBillList()
        },
        changePage(value) {
            this.pageNum = value
            this.getBillList()
        },
        handlePageSize(value) {
            this.pageSize = value;
            this.pageNum = 1;
            this.getBillList()
        },
        handleTabChange(value) {
            console.log(value)
            this.selectMonth = this.monthList[0].date
            this.getBillList()
        },
        getBillList() {
            getBillList(this.pageNum, this.pageSize, this.selectType, this.selectMonth).then(res => {
                if (res.data.code === 0) {
                    this.pageTotal = res.data.count
                    this.tableData = res.data.data
                }
            })
        },
        //下拉切换月份后进行数据更改
        handleCreate1 (val) {
            console.log(val)
            this.handleMonth(val)
        },
        handleChange (date) {
            console.log(date)
        },

    },
    computed: {
    ...mapState({
      rules: state => state.user.rules
    }),
    },
    mounted() {
        this.monthList = [
            {
                text: '1月',
                date: new Date(2020,1,1)
            },
            {
                text: '2月',
                date: new Date(2020,2,1)
            },
            {
                text: '3月',
                date: new Date(2020,3,1)
            }
        ]
        this.selectType = this.resType[0].id
        this.selectMonth = this.monthList[0].date
        this.getBillList()
    }
}
</script>

<style scoped>
.date-btn{
    border-right:2px solid #515a6e;
    border-radius: 0;
    padding: 0 5px;
    /* color: #dddddd; */
    span{
        color: #2d8cf0;
        text-decoration: underline;
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

