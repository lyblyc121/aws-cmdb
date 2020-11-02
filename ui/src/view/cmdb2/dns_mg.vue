<template>
  <div>
    <Row :gutter="20">
      <!-- <alert>同步Tag树：默认情况下部署CMDB时候settings里面配置了任务系统的数据库信息，主机资产会每天定时同步到Tag树，也可点击手动同步，无需选中主机，同步所有，注意请不要多次点击。</alert> -->
      <div class="search-con search-con-top">
        <Input
              @on-change="handleClear"
              clearable
              placeholder="输入关键字全局搜索"
              class="search-input"
              v-model="searchValue"
            />
            <Button @click="handleSearch" class="search-btn" type="primary">搜索</Button>
             <Button type="primary" class="search-btn" @click="exportData(2)">
              <Icon type="ios-download-outline"></Icon>导出数据
            </Button>
            <Detail :dialog="dialog2" :formData="detailData" @e-close="closeModal"></Detail>

      </div>

      <Table
            size="small"
            ref="selection"
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
      <Modal v-model="modalMap1.modalVisible" :title="modalMap1.modalTitle" :loading=true :footer-hide=true
                   :mask-closable=false width="650">
          <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100">
              <FormItem label="主机名" prop="server_id">
                  <Input v-model="formValidate.server_instance_id" :maxlength="120" disabled></Input>
              </FormItem>
              <FormItem label="状态" prop="security_state">
                  <Checkbox :value="formValidate.security_state" :maxlength=200 >安全</Checkbox>
              </FormItem> 
              <FormItem label="备注" prop="server_mark">
                  <Input v-model="formValidate.server_mark" :maxlength=200 placeholder='请输入备注'></Input>
              </FormItem> 
              <FormItem>
                  <Button type="primary" @click="handleSubmit('formValidate')">提交</Button>
                  <!-- <Button @click="handleReset('formValidate')" style="margin-left: 8px">重置</Button> -->
              </FormItem>
          </Form>
      </Modal>
    </Row>
  </div>
</template>

<script>
import Detail from "./risky_sever_detail";
import {
  getDNSList
} from "@/api/cmdb2/aws_asset.js";
// import { getAdminUserList } from "@/api/cmdb2/admin_user";
// import { getTagList } from "@/api/cmdb2/tag.js";
// import { getIDClist } from "@/api/cmdb2/idc.js";
// import MultiAdd from "./multi_add_server";
import { mapState } from "vuex";
export default {
  components: {
    // MultiAdd,
    Detail
  },
  data() {
    return {
      // formValidateLinkTag: {
      //   link_tag_list: []
      // },
      // modalMaplinkTag: {
      //   modalVisible: false,
      //   modalTitle: "选择你要关联的标签"
      // },
      // formData_multi: {
      //   data: null
      // },
      // multi_dialog: {
      //   show: false,
      //   title: "批量添加"
      // },
      // loading: false,
      // SSHloading: false,
      // logModal: false,
      // logInfo: [],
      // tagTreeData: [],
      // serverDetail: Object,
      dialog2: {
        show: false,
        title: "主机详情"
      },
      detailData: {
        server_instance_id: '',
        server_name: '',
        server_Project: '',
        security_state: false,
        server_public_ip: '',
        security_group: [],
        risk_port: [],
        server_mark: ''
      },
      formValidate: {
        server_instance_id: "",
        security_state: false,
        server_mark: ""
      },
      searchVal: "",

      modalMap1: {
        modalVisible: false,
        modalTitle: '修改主机信息'
      },
      // editModalData: null,
      tableData: [],
      // tableDataServer: [],

      // allServerList: [],
      // allDBList: [],
      // allUser: [],
      // allTagList: [],
      // allIDCList: [],
      // allProxyList: [],
      // tableSelectIdList: [],



      // single: false,
      // loadingStatus: false,
      // tableData: [],
      // admUserList: [],
      // allTagList: [],
      // allIDCList: [],
      // tableSelectIdList: [],

      // modalMap: {
      //   modalVisible: false,
      //   modalTitle: "新建"
      // },
      // formList: [],
      // editModalData: "",

      pageNum: 1, // 当前页码
      pageTotal: 0, // 数据总数
      pageSize: 15, // 每页条数
      //
      searchKey: "",
      searchValue: "",

      ruleValidate: {
        hostname: [
          {
            required: true,
            message: "The instance id cannot be empty",
            trigger: "blur"
          }
        ]
      },
      columns: [
        {
          title: "DNS名称",
          key: "dns_name",
          minWidth: 160,
          align: "center",
          sortable: true,
        },
        {
            title: "状态",
            key: "dns_status",
            width: 120,
            align: "center",
            sortable: true,
            render: (h, params) => {
                return h(
                "a",
                params.row.dns_status === "true" ? '已启用' : '未启用'
                );
            }
        },
        {
            title: "DNS类型",
            key: "dns_type",
            width: 130,
            align: "center",
            sortable: false
        },
        {
            title: "DNS内容",
            key: "dns_value",
            width: 180,
            align: "center",
            sortable: true
        },
        {
            title: "TTL",
            key: "dns_ttl",
            width: 120,
            align: "center",
            sortable: false
        },
        {
          title: "备注",
          key: "dns_remark",
          width: 200 ,
          align: "center",
          sortable: true
        }
      ]
    };
  },
  methods: {
    //请求Web Terminal接口
    // webTerminnal(params) {
    //   // this.SSHloading = true
    //   const data = {
    //     server_id: params.row.id
    //   };

    //   //ip地址
    //   let connect_ip = params.row.ip;
    //   webterminnal(data).then(res => {
    //     if (res.data.code === 0) {
    //       // this.loading = false;
    //       // this.$Message.success(`${res.data.msg}`);
    //       let web_terminal_conncet =
    //         res.data.data.web_terminal_url +
    //         connect_ip +
    //         "/" +
    //         res.data.data.web_terminal_key +
    //         "/";
    //       // console.log('web_terminal_conncet-->',web_terminal_conncet)
    //       window.open(web_terminal_conncet);
    //     } else {
    //       // this.loading = false;
    //       this.$Message.error(`${res.data.msg}`);
    //     }
    //   });
    // },

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

    // // 反向关联标签，支持多对多批量
    // handleSubmitlinkTag(value) {
    //   const data = {
    //     "tag_list": this.formValidateLinkTag.link_tag_list,
    //     "server_list": this.tableSelectIdList,
    //   }
    //   console.log('new_data--->', data)
    //   // console.log(this.formValidateLinkTag)
    //   // console.log('allTagList',this.allTagList)
    //   // this.$refs[value].validate((valid) => {
    //   //   if (valid) {
    //   //     setTimeout(() => {
    //   //       operationTag(this.formValidate2, this.editModalData).then(
    //   //         res => {
    //   //           if (res.data.code === 0) {
    //   //             this.$Message.success(`${res.data.msg}`);
    //   //             this.getTagList('tag_name', this.searchVal);
    //   //             // this.getTagTree()
    //   //             this.modalMap2.modalVisible = false;
    //   //           } else {
    //   //             this.$Message.error(`${res.data.msg}`);
    //   //           }
    //   //         }
    //   //       );
    //   //     }, 1000);
    //   //   } else {
    //   //     this.$Message.error('表单校验错误');
    //   //   }
    //   // })
    // },

    //点击关联标签按钮
    // HandlelinkTag() {
    //   console.log("长度", this.tableSelectIdList.length);
    //   if (this.tableSelectIdList.length > 1000) {
    //     this.$Message.error("一次性最多关联1000台");
    //     return;
    //   }
    //   if (this.tableSelectIdList.length > 0) {
    //     this.modalMaplinkTag.modalVisible = true;
    //   } else {
    //     this.$Message.info(`请选择你要关联的主机`);
    //   }
    // },

    // 批量添加
    // handlemultiAdd() {
    //   this.multi_dialog = {
    //     show: true,
    //     title: "批量添加主机"
    //   };
    // },
    // closeMultiModal() {
    //   this.formData_multi = {
    //     data: null
    //   };
    //   this.multi_dialog.show = false;
    // },
    // handleErrorLog(value) {
    //   this.logModal = true;
    //   getErrorLog("ip", value).then(res => {
    //     if (res.data.code === 0) {
    //       this.logInfo = res.data.data;
    //     } else {
    //       this.$Message.error(`${res.data.msg}`);
    //     }
    //   });
    // },
    // handlerCheckErrorLog() {
    //   this.logModal = true;
    //   getErrorLog().then(res => {
    //     if (res.data.code === 0) {
    //       this.logInfo = res.data.data;
    //     } else {
    //       this.$Message.error(`${res.data.msg}`);
    //     }
    //   });
    // },
    // closeModal() {
    //   this.over();
    // },
    // 获取TagTree
    // getTagTree(key) {
    //   getTagtree(key).then(res => {
    //     if (res.data.code === 0) {
    //       this.tagTreeData = res.data.data;
    //     } else {
    //       this.$Message.error(`${res.data.msg}`);
    //     }
    //   });
    // },
    // 获取主机信息
    getDNSList(value) {
      getDNSList(this.pageNum, this.pageSize, value).then(res => {
        if (res.data.code === 0) {
          this.pageTotal = res.data.count;
          this.tableData = res.data.data;
          console.log(res.data)
        } else {
          this.$Message.error(`${res.data.msg}`);
        }
      });
    },
    // 获取主机详情
    // getServerDetailList(key, value) {
    //   // console.log('key, vlaue', key,value)
    //   getServerDetailList(key, value).then(res => {
    //     if (res.data.code === 0) {
    //       this.serverDetail = res.data.data[0];
    //     } else {
    //       this.serverDetail = {
    //         cpu: "",
    //         disk: "",
    //         disk_utilization: "",
    //         id: "",
    //         // instance_id: null
    //         // instance_type: null
    //         ip: "",
    //         memory: "",
    //         os_distribution: "",
    //         os_version: "",
    //         sn: ""
    //       };
    //       // this.$Message.error(`${res.data.msg}`)
    //     }
    //   });
    // },

    // 获取管理用户列表
    // getAdminUserList(page, limit, key, value) {
    //   getAdminUserList(page, limit, key, value).then(res => {
    //     if (res.data.code === 0) {
    //       // this.$Message.success(`${res.data.msg}`)
    //       this.admUserList = res.data.data;
    //     } else {
    //       this.$Message.error(`${res.data.msg}`);
    //     }
    //   });
    // },
    // 获取IDC列表
    // getIDCList() {
    //   getIDClist().then(res => {
    //     if (res.data.code === 0) {
    //       // this.$Message.success(`${res.data.msg}`)
    //       this.allIDCList = res.data.data;
    //       // console.log(this.allTagList)
    //     }
    //   });
    // },

    // 获取Tag列表
    // getTagList() {
    //   getTagList().then(res => {
    //     if (res.data.code === 0) {
    //       // this.$Message.success(`${res.data.msg}`)
    //       this.allTagList = res.data.data;
    //       // console.log(this.allTagList)
    //     }
    //   });
    // },
    // table 选中的ID
    // handleSelectChange(val) {
    //   let SelectIdList = [];
    //   val.forEach(item => {
    //     SelectIdList.push(item.id);
    //   });
    //   this.tableSelectIdList = SelectIdList;
    // },
    handleHost(paramsRow, mtitle) {
      this.modalMap1.modalVisible = true
      this.modalMap1.modalTitle = mtitle
      // console.log(paramsRow)
      if (paramsRow && paramsRow.id) {
        this.formValidate = {
          server_instance_id: paramsRow.server_instance_id,
          security_state: paramsRow.security_state === "1" ? false : true,
          server_mark: paramsRow.server_mark
        }
        console.log(this.formValidate)
      } else {
        this.formValidate = {
          id: "paramsRow.server_instance_id",
          state: false,
          remark: ""
        }
      }
    },
    handleDetail(paramsRow) {
      this.dialog2.show = true;
      // this.getTagList()
      // this.getAdminUserList()
      let ports = paramsRow.risk_port
      let riskPorts = ports.split(',')
    
      // setTimeout(() => {
        
      // }
      this.detailData = {
        server_instance_id: paramsRow.server_instance_id,
        server_name: paramsRow.server_name,
        server_Project: paramsRow.server_Project,
        security_state: paramsRow.security_state === "" ? false : true,
        server_public_ip: paramsRow.server_public_ip,
        security_group: paramsRow.security_groups,
        risk_port: riskPorts,
        server_mark: paramsRow.server_mark
      }
    },
    closeModal() {
      this.dialog.show = false;
    },
    // tagHandleChange(newTargetKeys) {
    //   this.formData.tag = newTargetKeys;
    // },
    // tagFilter(data, query) {
    //   return data.label.indexOf(query) > -1;
    // },
    // editModal(paramsRow, meth, mtitle) {
    //   this.modalMap.modalVisible = true;
    //   this.modalMap.modalTitle = mtitle;
    //   this.editModalData = meth;
    //   if (paramsRow && paramsRow.id) {
    //     // put
    //     // this.getTagList();
    //     // this.getAdminUserList();
    //     this.formValidate = {
    //       id: paramsRow.id,
    //       hostname: paramsRow.hostname,
    //       ip: paramsRow.ip,
    //       public_ip: paramsRow.public_ip,
    //       port: paramsRow.port,
    //       idc: paramsRow.idc,
    //       region: paramsRow.region,
    //       admin_user: paramsRow.admin_user,
    //       tag_list: paramsRow.tag_list,
    //       detail: paramsRow.detail
    //     };
    //   } else {
    //     // post
    //     // this.getAdminUserList();
    //     // this.getTagList();
    //     if (this.selectTag) {
    //       this.formValidate = {
    //         hostname: "",
    //         ip: "",
    //         port: "22",
    //         admin_user: "",
    //         idc: "",
    //         region: "",
    //         tag_list: [this.selectTag],
    //         detail: "",
    //         state: "new"
    //       };
    //     } else {
    //       this.formValidate = {
    //         hostname: "",
    //         ip: "",
    //         port: "22",
    //         admin_user: "",
    //         idc: "",
    //         region: "",
    //         tag_list: [],
    //         detail: "",
    //         state: "new"
    //       };
    //     }
    //   }
    // },
    handleSubmit(value) {
        this.$refs[value].validate((valid) => {
        if (valid) {
          let requireData = {
              id: this.formValidate.server_instance_id,
              state: this.formValidate.security_state ? "1" : "",
              mark: this.formValidate.server_mark
            }
          console.log(requireData)

          setTimeout(() => {
            updateRiskyServer(requireData).then(res => {
              console.log(res.data)
              if (res.data.code === 0) {
                
                this.$Message.success(`${res.data.msg}`)
                this.getServerList(
                  this.searchValue
                )
                this.modalMap1.modalVisible = false
              } else {
                this.$Message.error(`${res.data.msg}`)
              }
            })
          }, 1000)
          // this.$Message.success('Success!');
        } else {
          this.$Message.error('缺少必要参数')
        }
      })








      // let data = {
      //   id: value.server_instance_id,
      //   state: value.security_state === "" ? true : value.security_state,
      //   mark: value.server_mark
      // }
      // console.log(data)
      // setTimeout( () => {
      //   updateRiskyServer(data).then(res => {
      //     if (res.data.code ===0 ) {
      //        this.$Message.success(`${res.data.msg}`);
      //        this.getServerList()
      //     } else {
      //       this.$Message.error(`${res.data.msg}`);
      //     }
      //   })
      // })


      // this.$refs[value].validate(valid => {
      //   if (valid) {
      //     setTimeout(() => {
      //       operationServer(this.formValidate, this.editModalData).then(res => {
      //         if (res.data.code === 0) {
      //           this.$Message.success(`${res.data.msg}`);
      //           this
      //             .getServerList
      //             // this.pageNum,
      //             // this.pageSize,
      //             // this.searchKey,
      //             // this.searchValue
      //             ();
      //           // this.getTagtree()
      //           this.modalMap.modalVisible = false;
      //         } else {
      //           this.$Message.error(`${res.data.msg}`);
      //         }
      //       });
      //     }, 1000);
      //     // this.$Message.success('Success!');
      //   } else {
      //     this.$Message.error("缺少必要参数");
      //   }
      // });
    },
    // handleReset(name) {
    //   this.$refs[name].resetFields();
    // },

    // handlerAssetUpdate() {
    //   // console.log(this.tableSelectIdList.length)
    //   this.getServerList()
    // },

    // handleSyncTagTree() {
    //   this.loading = true;
    //   this.$Modal.confirm({
    //     title: "提醒",
    //     content: "<p>向【作业配置】--【Tag树】进行同步资产任务</p>",
    //     loading: true,
    //     onOk: () => {
    //       setTimeout(() => {
    //         this.$Modal.remove();
    //         syncServerToTagTree().then(res => {
    //           if (res.data.code === 0) {
    //             this.$Message.success(`${res.data.msg}`);
    //           } else {
    //             this.$Message.error(`${res.data.msg}`);
    //           }
    //           this.loading = false;
    //         });
    //       }, 2000);
    //     },
    //     onCancel: () => {
    //       this.loading = false;
    //       this.$Message.info("Clicked cancel");
    //     }
    //   });
    // },

    // handlerDelete() {
    //   // console.log(this.tableSelectIdList.length)
    //   if (this.tableSelectIdList.length > 0) {
    //     if (confirm(`确定要批量删除选中主机 `)) {
    //       operationServer({ id_list: this.tableSelectIdList }, "delete").then(
    //         res => {
    //           if (res.data.code === 0) {
    //             this.$Message.success(`${res.data.msg}`);
    //             this.getServerList(this.searchVal);
    //           } else {
    //             this.$Message.error(`${res.data.msg}`);
    //           }
    //         }
    //       );
    //     }
    //   } else {
    //     this.$Message.info(`你总要选中点什么吧`);
    //   }
    // },
    // 删除
    // delData(params) {
    //   if (confirm(`确定要删除 ${params.row.hostname}`)) {
    //     // console.log(params.row.id)
    //     operationServer(
    //       {
    //         server_id: params.row.id
    //       },
    //       "delete"
    //     ).then(res => {
    //       if (res.data.code === 0) {
    //         this.$Message.success(`${res.data.msg}`);
    //         this.tableData.splice(params.index, 1);
    //       } else {
    //         this.$Message.error(`${res.data.msg}`);
    //       }
    //     });
    //   }
    // },
    handleClear(e) {
      if (e.target.value === "") this.tableData = this.value;
    },
    handleSearch() {
      this.getDNSList(this.searchValue);
    },
    // 翻页
    changePage(value) {
      this.pageNum = value;
      if (this.searchValue) {
        this.getDNSList(this.searchValue);
      } else {
        this.getDNSList();
      }
    },
    // 切换分页
    handlePageSize(value) {
      this.pageSize = value;
      this.pageNum = 1;
      if (this.searchValue) {
        this.getDNSList(this.searchValue);
      } else {
        this.getDNSList();
      }
    }
  },
  computed: {
    ...mapState({
      rules: state => state.user.rules
    })
  },
  watch: {
    // searchVal (val) {
    //   this.searchVal = val
    //   this.getServerList(this.searchVal)
    // }
  },

  mounted() {
    this.getDNSList();
    // this.getTagList();
    // this.getAdminUserList();
    // this.getTagTree();
    // this.getIDCList();
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
</style>
