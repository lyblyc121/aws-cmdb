<template>
    <div>
        <Row :gutter="20">
            <!-- <alert> 提示：暂时还未有折线图 </alert> -->
              <div style="margin: 10px; overflow: hidden;">
                <ul class="text-btn">
                    <li v-for="month in monthList" @click="handleChart(null,month.date,month.text)" :key="month.text"><a :style="{'color': (selectMonth!=month.text? '#2d8cf0' : '#515a6e')}">{{ month.text }}</a></li>
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
                    :title="cTitle">
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
                @on-selection-change="handleSelectChange"
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
import { ChartPie, ChartBar, ChartLine } from "_c/charts"
import Detail from "./server_detail";
import {
  getServerList,
  getServerDetailList,
  operationServer,
  assetServerUpdate,
  getTagtree,
  getErrorLog,
  syncServerToTagTree,
  webterminnal,
} from "@/api/cmdb2/server.js";
import { getAdminUserList } from "@/api/cmdb2/admin_user"
import { 
    getResourceList,
    getResourceDetailList,
    getResourceUsage,
    getDisplayMonthList
} from '@/api/usage/resource.js'
import { getTagList } from "@/api/cmdb2/tag.js";
import { getIDClist } from "@/api/cmdb2/idc.js";
import MultiAdd from "./multi_add_server";
import { mapState } from "vuex";
export default {
    components: {
        MultiAdd,
        Detail,
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
            monthList: {},

            // search part
            searchKey: "",
            searchValue: "",

            // chart
            timeData: ['2020-03-01', '2020-03-02', '2020-03-03', '2020-03-04', '2020-03-05', '2020-03-06'],
            cLegend: {'cpu': 'CPU利用率', 'memory': '内存利用率', 'disk':'磁盘利用率'},
            cTitle: "资源使用折线图",
            opData: {
                'cpu': [0.22, 0.45, 0.23, 0.56, 0.53, 0.7],
                'memory': [0.32, 0.67, 0.56, 0.2, 0.76, 0.36],
                'disk': [0.856, 0.24, 0.62, 0.7, 0.124, 0.34]
            },
            // 
            columns: [
                {
                    type: "selection",
                    key: "id",
                    width: 60,
                    aligin: "center"
                },
                {
                    title: "主机ID",
                    key: "hostid",
                    minWidth: 150,
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
                             params.row.hostid
                        );
                    }
                },
                {
                    title: "主机名",
                    key: "hostname",
                    minWidth: 150,
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
                             params.row.hostname
                        );
                    }
                },
                {
                    title: "所属项目",
                    key: "project",
                    minWidth: 180,
                    aligin: "center",
                    sortable: false,
                },
                {
                    title: "CPU使用率",
                    key: "CPUUtilization",
                    minWidth: 120,
                    aligin: "center",
                    sortable: true,
                },
                {
                    title: "内存使用率",
                    key: "MemoryUtilization",
                    minWidth: 120,
                    aligin: "center",
                    sortable: true,
                },
                {
                    title: "磁盘使用率",
                    key: "DiskUitlization",
                    minWidth: 120,
                    aligin: "center",
                    sortable: true,
                },
                {
                    title: "当前机型",
                    key: "type",
                    minWidth: 140,
                    aligin: "center",
                    sortable: true,
                },
                {
                    title: "建议机型",
                    key: "suggest_type",
                    minWidth: 140,
                    aligin: "center",
                    sortable: false,
                },
            ],

            //
            selectHost: "",
            selectMonth: "",

            auth_key: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODQxNzU0NTksIm5iZiI6MTU4NDA4OTAxOSwiaWF0IjoxNTg0MDg5MDI5LCJpc3MiOiJhdXRoOiBzcyIsInN1YiI6Im15IHRva2VuIiwiaWQiOiIxNTYxODcxODA2MCIsImRhdGEiOnsidXNlcl9pZCI6IjEiLCJ1c2VybmFtZSI6ImFkbWluIiwibmlja25hbWUiOiJhZG1pbiIsImVtYWlsIjoiMTkxNzE1MDMwQHFxLmNvbSIsImlzX3N1cGVydXNlciI6dHJ1ZX19.KFpDrMMzjz1_x1EbPUSk58AcYEEwo3uTcPEpukPf970"
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

        // 批量添加
        handlemultiAdd() {
            this.multi_dialog = {
                show: true,
                title: "批量添加主机"
            };
        },
        closeMultiModal() {
            this.formData_multi = {
                data: null
            };
            this.multi_dialog.show = false;
        },
        handleErrorLog(value) {
            this.logModal = true;
            getErrorLog("ip", value).then(res => {
                if (res.data.code === 0) {
                this.logInfo = res.data.data;
                } else {
                this.$Message.error(`${res.data.msg}`);
                }
            });
        },
        handlerCheckErrorLog() {
            this.logModal = true;
            getErrorLog().then(res => {
                if (res.data.code === 0) {
                this.logInfo = res.data.data;
                } else {
                this.$Message.error(`${res.data.msg}`);
                }
            });
        },
        closeModal() {
            this.over();
        },
        // 获取TagTree
        getTagTree(key) {
            getTagtree(key).then(res => {
                if (res.data.code === 0) {
                this.tagTreeData = res.data.data;
                } else {
                this.$Message.error(`${res.data.msg}`);
                }
            });
        },
        // 获取展示月份
        getDisplayMonthList() {
            getDisplayMonthList(this.auth_key).then(res => {
                if (res.data.code === 0) {
                    console.log(res.data)
                }
            })
            
        },

        getServerList(key, value) {
            getServerList(this.pageNum, this.pageSize, key, value).then(res => {
                if (res.data.code === 0) {
                    this.pageTotal = res.data.count
                    this.tableData = res.data.data
                    this.monthList = [
                        {
                            text: '2020年1月',
                            date: new Date(2020,1,1)
                        },
                        {
                            text: '2020年2月',
                            date: new Date(2020,2,1)
                        },
                        {
                            text: '2020年3月',
                            date: new Date(2020,3,1)
                        }
                    ]
                    // this.monthList = res.data.data[0].date_list
                } else {
                    this.$Message.error(`${res.data.msg}`)
                }
            });
        },
        // 获取资源详情
        getResourceList(key, value) {
            getResourceList(key, value).then(res => {
                if (res.data.code === 0) {
                    this.pageTotal = res.data.count
                    this.tableData = res.data.data
                    this.monthList = res.data.data[0].date_list
                } else {
                    this.$Message.error(`${res.data.msg}`);

                }
            })
        },
        // 获取主机详情
        getServerDetailList(key, value) {
        // console.log('key, vlaue', key,value)
            getServerDetailList(key, value).then(res => {
                if (res.data.code === 0) {
                    this.serverDetail = res.data.data[0];
                } else {
                    this.serverDetail = {
                    cpu: "",
                    disk: "",
                    disk_utilization: "",
                    id: "",
                    // instance_id: null
                    // instance_type: null
                    ip: "",
                    memory: "",
                    os_distribution: "",
                    os_version: "",
                    sn: ""
                };
                // this.$Message.error(`${res.data.msg}`)
                }
            })
        },

        // 获取管理用户列表
        getAdminUserList(page, limit, key, value) {
            getAdminUserList(page, limit, key, value).then(res => {
                if (res.data.code === 0) {
                // this.$Message.success(`${res.data.msg}`)
                this.admUserList = res.data.data;
                } else {
                this.$Message.error(`${res.data.msg}`);
                }
            });
        },
        // 获取IDC列表
        getIDCList() {
            getIDClist().then(res => {
                if (res.data.code === 0) {
                // this.$Message.success(`${res.data.msg}`)
                this.allIDCList = res.data.data;
                // console.log(this.allTagList)
                }
            });
        },

        // 获取Tag列表
        getTagList() {
            getTagList().then(res => {
                if (res.data.code === 0) {
                // this.$Message.success(`${res.data.msg}`)
                this.allTagList = res.data.data;
                // console.log(this.allTagList)
                }
            });
        },
        // table 选中的ID
        handleSelectChange(val) {
            let SelectIdList = [];
            val.forEach(item => {
                SelectIdList.push(item.id);
            });
            this.tableSelectIdList = SelectIdList;
        },
        // 折线图渲染
        handleChart(key, date, text) {
            this.selectMonth = text
            let selectHost = key === null ? this.selectHost : this.tableData[0].id
            getResourceUsage(selectHost, date).then(res => {
                if (res.data.code === 0) {
                    this.opData = res.data.data
                } else {
                    this.opData = {
                        cpu: [],
                        memory: [],
                        disk: [] 
                    }
                }
            })
        },
        handleDetail(paramsRow) {
            console.log(paramsRow)
            this.selectHost = paramsRow.id
            this.handleChart(this.selectHost, paramsRow.date_list[paramsRow.date_list.length-1].date, paramsRow.date_list[paramsRow.date_list.length-1].text)
        },
        closeModal() {
            this.dialog.show = false;
        },
        tagHandleChange(newTargetKeys) {
            this.formData.tag = newTargetKeys;
        },
        tagFilter(data, query) {
            return data.label.indexOf(query) > -1;
        },
        editModal(paramsRow, meth, mtitle) {
            this.modalMap.modalVisible = true;
            this.modalMap.modalTitle = mtitle;
            this.editModalData = meth;
            if (paramsRow && paramsRow.id) {
                // put
                this.getTagList();
                this.getAdminUserList();
                this.formValidate = {
                id: paramsRow.id,
                hostname: paramsRow.hostname,
                ip: paramsRow.ip,
                public_ip: paramsRow.public_ip,
                port: paramsRow.port,
                idc: paramsRow.idc,
                region: paramsRow.region,
                admin_user: paramsRow.admin_user,
                tag_list: paramsRow.tag_list,
                detail: paramsRow.detail
                };
            } else {
                // post
                this.getAdminUserList();
                this.getTagList();
                if (this.selectTag) {
                    this.formValidate = {
                        hostname: "",
                        ip: "",
                        port: "22",
                        admin_user: "",
                        idc: "",
                        region: "",
                        tag_list: [this.selectTag],
                        detail: "",
                        state: "new"
                    };
                } else {
                    this.formValidate = {
                        hostname: "",
                        ip: "",
                        port: "22",
                        admin_user: "",
                        idc: "",
                        region: "",
                        tag_list: [],
                        detail: "",
                        state: "new"
                    };
                }
            }
        },
        handleSubmit(value) {
            this.$refs[value].validate(valid => {
                if (valid) {
                setTimeout(() => {
                    operationServer(this.formValidate, this.editModalData).then(res => {
                    if (res.data.code === 0) {
                        this.$Message.success(`${res.data.msg}`);
                        this
                        .getServerList
                        // this.pageNum,
                        // this.pageSize,
                        // this.searchKey,
                        // this.searchValue
                        ();
                        // this.getTagtree()
                        this.modalMap.modalVisible = false;
                    } else {
                        this.$Message.error(`${res.data.msg}`);
                    }
                    });
                }, 1000);
                // this.$Message.success('Success!');
                } else {
                this.$Message.error("缺少必要参数");
                }
            });
        },
        handleReset(name) {
            this.$refs[name].resetFields();
        },

        handlerAssetUpdate() {
        // console.log(this.tableSelectIdList.length)
            if (this.tableSelectIdList.length > 6) {
                this.$Message.error(
                `手动更新请不要超过5个，默认添加的机器都会自动推送更新`
                );
                return;
            }
            if (this.tableSelectIdList.length > 0) {
                this.$Spin.show({
                render: h => {
                    return h("div", [
                    h("Icon", {
                        class: "demo-spin-icon-load",
                        props: {
                        type: "ios-loading",
                        size: 18
                        }
                    }),
                    h("div", "资产更新中....")
                    ]);
                }
                });
                assetServerUpdate({ id_list: this.tableSelectIdList }, "post").then(
                res => {
                    this.$Spin.hide();
                    if (res.data.code === 0) {
                    this.$Message.config({
                        top: 24,
                        duration: 5 // 停留时间
                    });
                    this.$Message.info(`${res.data.msg}`);
                    this.getServerList(this.searchVal);
                    } else {
                    this.$Message.config({
                        top: 24,
                        duration: 5 // 停留时间
                    });
                    this.$Message.error(`${res.data.msg}`);
                    }
                }
                );
            } else {
                this.$Message.info(`你总要选中点什么吧`);
            }
        },

        handleSyncTagTree() {
            this.loading = true;
            this.$Modal.confirm({
                title: "提醒",
                content: "<p>向【作业配置】--【Tag树】进行同步资产任务</p>",
                loading: true,
                onOk: () => {
                setTimeout(() => {
                    this.$Modal.remove();
                    syncServerToTagTree().then(res => {
                    if (res.data.code === 0) {
                        this.$Message.success(`${res.data.msg}`);
                    } else {
                        this.$Message.error(`${res.data.msg}`);
                    }
                    this.loading = false;
                    });
                }, 2000);
                },
                onCancel: () => {
                this.loading = false;
                this.$Message.info("Clicked cancel");
                }
            });
        },

        handlerDelete() {
        // console.log(this.tableSelectIdList.length)
        if (this.tableSelectIdList.length > 0) {
            if (confirm(`确定要批量删除选中主机 `)) {
            operationServer({ id_list: this.tableSelectIdList }, "delete").then(
                res => {
                if (res.data.code === 0) {
                    this.$Message.success(`${res.data.msg}`);
                    this.getServerList(this.searchVal);
                } else {
                    this.$Message.error(`${res.data.msg}`);
                }
                }
            );
            }
        } else {
            this.$Message.info(`你总要选中点什么吧`);
        }
        },
        // 删除
        delData(params) {
        if (confirm(`确定要删除 ${params.row.hostname}`)) {
            // console.log(params.row.id)
            operationServer(
            {
                server_id: params.row.id
            },
            "delete"
            ).then(res => {
            if (res.data.code === 0) {
                this.$Message.success(`${res.data.msg}`);
                this.tableData.splice(params.index, 1);
            } else {
                this.$Message.error(`${res.data.msg}`);
            }
            });
        }
        },
        handleClear(e) {
        if (e.target.value === "") this.tableData = this.value;
        },
        handleSearch() {
            this.getServerList(this.searchValue);
        },
        // 点击节点
        handlerTreeChange(obj) {
        if (obj.length !== 0) {
            const data = obj[0];
            // this.searchVal = null
            this.pageNum = 1;
            if (data.title === "root") {
            this.selectTag = null;
            // this.selectTwo = 'tag'
            this.getTagList();
            this.getServerList();
            } else if (data.tag_name) {
            this.selectTwo = data.node;
            this.selectTag = data.tag_name;
            this.getServerList("tag_name", data.tag_name);
            } else if (data.title === "root" && !data.node) {
            this.selectTag = null;
            this.selectTwo = data.title;
            this.getServerList();
            }
        }
        },
        // 翻页
        changePage(value) {
        this.pageNum = value;
        if (this.selectTwo === "tag") {
            if (this.searchValue) {
            this.getTagList("tag_name", this.searchValue);
            } else {
            this.getTagList();
            }
        } else if (this.selectTag) {
            this.getServerList("tag_name", this.selectTag);
        } else {
            this.getServerList();
        }
        },
        // 切换分页
        handlePageSize(value) {
        this.pageSize = value;
        this.pageNum = 1;
        if (this.searchValue) {
            this.getServerList(this.searchValue);
        } else if (this.selectTag) {
            this.getServerList("tag_name", this.tag_name);
        } else {
            this.getServerList();
        }
        }
    },
    computed: {
    ...mapState({
      rules: state => state.user.rules
    }),
    },
    mounted() {
        this.getServerList()
        this.getTagList()
        this.getAdminUserList()
        this.getDisplayMonthList()
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