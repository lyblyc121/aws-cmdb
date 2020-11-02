<template>
    <div>
        <Row :gutter="20">
            <!-- <Card>
                  <i-col :md="24" :lg="5" style="margin-bottom: 20px;">
                <Card>
                  <Tree ref="tree" :data="tagTreeData"  @on-select-change="handlerTreeChange" getSelectedNodes></Tree>
                </Card>
              </i-col> -->
            <div class="search-con search-con-top">
                <!-- <Input class="search-input" v-model="searchVal" style="padding:6px;" placeholder="输入关键字搜索"/> -->
                <Input @on-change="handleClear" clearable placeholder="输入关键字全局搜索" class="search-input" v-model="searchValue"/>
                <Button @click="handleSearch" class="search-btn" type="primary">搜索</Button>
                <!-- <slot name="new_btn">
                    <Button type="primary" @click="handlerDB('', 'post', '添加数据库')" class="search-btn">添加数据库</Button>
                </slot> -->
                <!-- <Button type="info" class="search-btn"  @click="handlemultiAdd">批量添加</Button> -->
                <!-- <Button type="error" class="search-btn" @click="handlerDelete">批量删除</Button> -->
                <Button type="primary" class="search-btn" @click="exportData(2)"><Icon type="ios-download-outline"></Icon>导出数据 </Button>
                      </div>
            <Table size="small" ref="selection" border :columns="columns" :data="tableData"
                   @on-selection-change="handleSelectChange"></Table>
            <div style="margin: 10px; overflow: hidden">
                <div style="float: left;">
                    <Page :total="pageTotal" :current="pageNum" :page-size="pageSize" :page-size-opts=[18,35,50,100,200,500]
                          show-sizer
                          show-total @on-change="changePage" @on-page-size-change="handlePageSize"></Page>
                </div>
            </div>

            <Modal v-model="modalMap1.modalVisible" :title="modalMap1.modalTitle" :loading=true :footer-hide=true
                   :mask-closable=false width="650">
              <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100">
                <FormItem label="主机名" prop="bucket_name">
                    <Input v-model="formValidate.bucket_name" :maxlength="120" disabled></Input>
                </FormItem>
                <FormItem label="状态" prop="security_state">
                    <Checkbox :checked.sync="formValidate.security_state" @on-change='hahah' :maxlength=200 >安全</Checkbox>
                </FormItem> 
                <FormItem label="备注" prop="bucket_remark">
                    <Input v-model="formValidate.bucket_remark" :maxlength=200 placeholder='请输入备注'></Input>
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

import Detail from './db_detail'
import {getDBlist, getDBDetail, operationDB, updateRemark} from '@/api/cmdb2/aws_asset.js'
// import {getIDClist} from '@/api/cmdb2/idc.js'
// import {getTagList} from '@/api/cmdb2/tag.js'
// import {getProxylist} from '@/api/task-other'
// import {getuserlist} from '@/api/user'
// import MultiAdd from './multi_add_db'

export default {
  // components: {
  //   Detail,
  //   MultiAdd
  // },
  data () {
    return {
      formData_multi: {
        data: null
      },
      multi_dialog: {
        show: false,
        title: '批量添加'
      },
      DBDetail: Object,
      dialog2: {
        show: false,
        title: 'DB详情'
      },
      // 分页
      pageTotal: 0, // 数据总数
      pageNum: 1, // 当前页码
      pageSize: 18, // 每页条数
      searchKey: '',
      searchValue: '',
      selectTwo: 'tag',
      selectTag: null,
      tagTreeData: [],
      searchVal: '',
      modalMap1: {
        modalVisible: false,
        modalTitle: '添加数据库'
      },
      editModalData: null,
      tableData: [],
      tableDataServer: [],
      // tableDataDB: [],
      //
      allServerList: [],
      allDBList: [],
      allUser: [],
      allTagList: [],
      allIDCList: [],
      allProxyList: [],
      tableSelectIdList: [],
      formValidate: {
        id: null,
        bucket_name: '',
        security_state: false,
        bucket_remark: '介绍一下吧' 
      },
      envList: [
        {value: 'dev', label: 'dev'},
        {value: 'qa', label: 'qa'},
        {value: 'staging', label: 'staging'},
        {value: 'sandbox', label: 'sandbox'},
        {value: 'release', label: 'release'},
        {value: 'hidden', label: 'hidden'}
      ],
      typeList: [
        {value: 'mysql', label: 'mysql'},
        {value: 'redis', label: 'redis'},
        {value: 'mongodb', label: 'mongodb'},
        {value: 'other', label: 'other'}
      ],
      markList: [
        {value: '写', label: '写'},
        {value: '读', label: '读'},
        {value: '备', label: '备'}
      ],

      ruleValidate: {
        bucket_name: [{required: true, message: 'The bucket_name cannot be empty', trigger: 'blur'}]
        // db_host: [{required: true, message: 'The db_host cannot be empty', trigger: 'blur'}],
        // db_port: [{required: true, message: 'The db_port cannot be empty', trigger: 'blur'}],
        // db_user: [{required: true, message: 'The db_user cannot be empty', trigger: 'blur'}],
        // db_pwd: [{ required: true, message: "The db_pwd cannot be empty", trigger: "blur"}],
        // db_env: [{ required: true, message: "请选择一个环境", trigger: "change"}],
        // proxy_host: [{ required: true, message: "请选择代理主机", trigger: "change"}],
        // db_type: [{ required: true, message: '请选择数据库类型', trigger: 'change'}]
        // bucket_status: [{ required: true, message: "请选择安全状态", trigger: "change"}],
        // db_mark: [{ required: true, message: "请选择标记", trigger: "change"}],
      },

      columns: [
        {
          type: 'selection',
          key: 'id',
          width: 60,
          align: 'center'
        },
        {
          title: 'S3存储桶名称',
          key: 'bucket_name',
          align: 'center',
          minWidth:150,
          // render: (h, params) => {
          //   return h('div', [
          //     h(
          //       'a',
          //       {
          //         on: {
          //           click: () => {
          //             this.handleDetail(params.row)
          //           }
          //         }
          //       },
          //       params.row.bucket_name
          //     )
          //   ])
          // }
        },
        {title: '标签', key: 'bucket_tags', width: 180, align: 'center', sortable: true},
        {
          title: '是否公开', 
          key: 'bucket_acl', 
          width: 120, 
          align: 'center', 
          sortable: true,
          render: (h, params) => {
            let isPublic = parseInt(params.row.bucket_acl) > 0 ? '是' : '否' 
            return h(
              "a",
              isPublic
            );
          }  
        },
        {title: '迁移', key: 'bucket_lifecycle', width: 120, align: 'center', sortable: true},
        {
          title: '是否安全', 
          key: 'bucket_mark', 
          width: 120, 
          align: 'center', 
          sortable: true,
          render: (h, params) => {
            let bucket_mark = parseInt(params.row.bucket_mark) > 0 ? true : false

            return h("div", [
              h("Checkbox", { props: { value: bucket_mark}}, "")
            ])
          }
        },
        {title: '备注', key: 'bucket_remark', width: 180, align: 'center', sortable: true},

        {title: '创建时间', key: 'create_time', width: 160, align: 'center', sortable: true},
        {title: '更新时间', key: 'update_time', width: 160, align: 'center', sortable: true},
        // {title: '容量', key: 'idc', width: 120, align: 'center', sortable: true},
        // {title: '可用区', key: 'db_region', width: 150, align: 'center', sortable: true},
        // {title: '地址', key: 'db_host', align: 'center', sortable: true,minWidth: 120},
        // {title: '端口', key: 'db_port', width: 120, align: 'center', sortable: true},
        // {title: '用户', key: 'db_user', width: 120, align: 'center', sortable: true},
        // // { title: '环境',  key: 'db_env', align: 'center', sortable: true },
        // // { title: '角色',  key: 'db_mark',width: 80, align: 'center', sortable: true },
        // {title: '类型', key: 'db_type', width: 120, align: 'center', sortable: true},
        // {title: '版本', key: 'db_version', width: 120, align: 'center', sortable: true},
        // // { title: '代理', key: 'proxy_host', align: 'center', sortable: true},
        // {title: '状态', key: 'state', width: 150, align: 'center', sortable: true},

        // {
        //   title: '状态',
        //   key: 'state',
        //   width: 120,
        //   align: 'center',
        //   render: (h, params) => {
        //     let state = params.row.state
        //     if (state === 'available') {
        //       return h('div', [
        //         h('Tag', { props: { color: 'success' } }, '运行中')
        //       ])
        //     } else if (state === '运行中') {
        //       return h('div',[h('Tag', { props: { color: 'success' }}, '运行中')])
        //     } else if (state === 'Running') {
        //       return h('div',[h('Tag', { props: { color: 'success' }}, '运行中')])
        //     } else if (state === 'Handle') {
        //       return h('div',[h('Tag', { props: { color: 'blue' }}, 'Handle')])
        //     } else if (state === 'backing-up') {
        //       return h('div',[h('Tag', { props: { color: 'blue' }}, '同步从库')])
        //     } else if (state === 'storage-full') {
        //       return h('div',[h('Tag', { props: { color: 'error' }}, '磁盘已满')])
        //     } else if (state === 'Normal'){
        //       return h('div',[h('Tag', { props: { color: 'success' }}, '运行中')])
        //     }
        //     else {
        //     return h('div', [
        //       h(
        //         'Button',
        //         {
        //           props: {
        //             type: 'error',
        //             size: 'small'
        //           },
        //           style: {
        //             marginRight: '4px'
        //           },
        //           on: {
        //             click: () => {
        //               this.handleErrorLog(params.row.ip)
        //             }
        //           }
        //         },
        //         'False'
        //       ),
        //       ])
        //     }
        //   }
        // },

        {
          title: '操作',
          key: 'handle',
          width: 130,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h(
                'Button',
                {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '2px'
                  },
                  on: {
                    click: () => {
                      this.handlerDB(params.row, 'put', 'S3桶信息编辑')
                    }
                  }
                },
                '编辑'
              )
              // h('Button',
              //   {
              //     props: {type: 'error', size: 'small'},
              //     on: {
              //       click: () => {
              //         this.handlerDeleteDB(params)
              //       }
              //     }
              //   },
              //   '删除'
              // )
            ])
          }
        }
      ]
    }
  },
  methods: {
    hahah(e) {
      this.formValidate.security_state = e
      console.log(this.formValidate)
    },
    // 导出数据、支持分页、过滤、搜索、排序后导出
    exportData (type) {
        if (type === 1) {
            this.$refs.selection.exportCsv({
                filename: 'codo_cmdb_original_data'
            });
        } else if (type === 2) {
            this.$refs.selection.exportCsv({
                filename: 'codo_cmdb_sorting_and_filtering_data',
                original: false
            });
        } else if (type === 3) {
            this.$refs.selection.exportCsv({
                filename: 'codo_cmdb_custom_data',
                columns: this.columns8.filter((col, index) => index < 4),
                data: this.data7.filter((data, index) => index < 4)
            });
        }
    },    
    // 批量添加
    // handlemultiAdd () {
    //   this.multi_dialog = {
    //     show: true,
    //     title: '批量添加数据库'
    //   }
    // },
    // closeMultiModal () {
    //   this.formData_multi = {
    //     data: null
    //   }
    //   this.multi_dialog.show = false
    // },
    // 获取数据库
    getDBList (key) {
      getDBlist(this.pageNum, this.pageSize, key).then(res => {
        if (res.data.code === 0) {
          console.log(res.data)
          this.pageTotal = res.data.count
          this.tableData = res.data.data

        } else {
          this.$Message.error(`${res.data.msg}`)
        }
      })
    },
    // 获取主机详情
    // getDBDetailList (key, value) {
    //   // console.log('key, vlaue', key,value)
    //   getDBDetail(key, value).then(res => {
    //     if (res.data.code === 0) {
    //       this.DBDetail = res.data.data[0]
    //     } else {
    //       this.DBDetail = {
    //         id: null,
    //         // idc: '',
    //         // db_region: '',
    //         // db_disk: '',
    //         // db_code: '',
    //         // db_host: '',
    //         // db_port: '',
    //         // db_user: '',
    //         // db_pwd: '',
    //         // db_env: '',
    //         // proxy_host: '',
    //         // db_type: '',
    //         // db_version: '',
    //         // db_mark: '',
    //         // tag_list: [],
    //         s3_remark: '',
    //         // db_public_ip: '',
    //         // update_time: '',
            
    //       }
    //       // this.$Message.error(`${res.data.msg}`)
    //     }
    //   })
    // },

    // 获取所有数据库信息
    // getALLDBList () {
    //   getDBlist(1, 888).then(res => {
    //     if (res.data.code === 0) {
    //       this.allDBList = res.data.data
    //     } else {
    //       this.$Message.error(`${res.data.msg}`)
    //     }
    //   })
    // },

    // // 获取用户列表
    // getUserList () {
    //   getuserlist(1, 2000).then(res => {
    //     if (res.data.code === 0) {
    //       this.allUser = res.data.data
    //     } else {
    //       this.$Message.error(`${res.data.msg}`)
    //     }
    //   })
    // },
    // 获取代理主机
    // getProxyList () {
    //   getProxylist().then(res => {
    //     if (res.data.code === 0) {
    //       this.allProxyList = res.data.data
    //     } else {
    //       this.$Message.error(`${res.data.msg}`)
    //     }
    //   })
    // },
    // // 获取IDC列表
    // getIDCList () {
    //   getIDClist().then(res => {
    //     if (res.data.code === 0) {
    //       // this.$Message.success(`${res.data.msg}`)
    //       this.allIDCList = res.data.data
    //       // console.log(this.allTagList)
    //     }
    //   })
    // },

    // // 获取Tag列表
    // getTagList () {
    //   getTagList().then(res => {
    //     if (res.data.code === 0) {
    //       // this.$Message.success(`${res.data.msg}`)
    //       this.allTagList = res.data.data
    //     }
    //   })
    // },

    // handlerDelete () {
    //   // console.log(this.tableSelectIdList.length)
    //   if (this.tableSelectIdList.length > 0) {
    //     if (confirm(`确定要批量删除选中数据库 `)) {
    //       operationDB({'id_list': this.tableSelectIdList}, 'delete').then(
    //         res => {
    //           if (res.data.code === 0) {
    //             this.$Message.success(`${res.data.msg}`)
    //             this.getDBList(this.searchVal)
    //           } else {
    //             this.$Message.error(`${res.data.msg}`)
    //           }
    //         })
    //     }
    //   } else {
    //     this.$Message.info(`你总要选中点什么吧`)
    //   }
    // },

    // handleDetail (paramsRow) {
    //   this.dialog2.show = true
    //   // this.serverDetail = {}
    //   this.DBDetail = {
    //     id: null,
    //     db_code: '',
    //     db_host: '',
    //     db_port: '',
    //     db_user: '',
    //     db_pwd: '',
    //     db_env: '',
    //     proxy_host: '',
    //     db_type: '',
    //     db_version: '',
    //     db_mark: '',
    //     tag_list: [],
    //     s3_remark: '',
    //     db_public_ip: '',
    //     update_time: ''
    //   }
    //   this.getDBDetailList('ip', paramsRow.ip)
    //   setTimeout(() => {
    //     this.formValidate = {
    //       id: paramsRow.id,
    //       bucket_mark: paramsRow.bucket_mark,
    //       // idc: paramsRow.idc,
    //       // db_code: paramsRow.db_code,
    //       // db_class: paramsRow.db_class,
    //       // db_region: paramsRow.db_region,
    //       // db_disk: paramsRow.db_disk,
    //       // db_host: paramsRow.db_host,
    //       // db_port: paramsRow.db_port,
    //       // db_user: paramsRow.db_user,
    //       // db_pwd: paramsRow.db_pwd,
    //       // db_env: paramsRow.db_env,
    //       // db_version: paramsRow.db_version,
    //       // proxy_host: paramsRow.proxy_host,
    //       // db_type: paramsRow.db_type,
    //       // db_mark: paramsRow.db_mark,
    //       s3_remark: paramsRow.bucket_mark,
    //       // state: paramsRow.state,
    //       // db_tag: paramsRow.tag_list,
    //       // db_public_ip: paramsRow.db_public_ip,
    //       // update_time: paramsRow.update_time
    //     }
    //   }, 500)
    // },
    closeModal () {
      this.over()
    },
    // table 选中的ID
    handleSelectChange (val) {
      let SelectIdList = []
      val.forEach(item => {
        SelectIdList.push(item.id)
      })
      this.tableSelectIdList = SelectIdList
    },
    // tagHandleChange (newTargetKeys) {
    //   this.formData.tag = newTargetKeys
    // },
    // tagFilter (data, query) {
    //   return data.label.indexOf(query) > -1
    // },
    handlerDB (paramsRow, meth, mtitle) {
      this.modalMap1.modalVisible = true
      this.modalMap1.modalTitle = mtitle
      // this.editModalData = meth

      if (paramsRow && paramsRow.id) {
        this.formValidate = {
          id: paramsRow.id,
          bucket_name: paramsRow.bucket_name,
          security_state: paramsRow.bucket_mark === 1 ? true : false,
          bucket_remark: paramsRow.bucket_remark,
          // update_time: paramsRow.update_time
        }
      } else {
        this.formValidate = {
          id: null,
          bucket_name: '',
          bucket_remark: '介绍一下吧',
          security_state: false
        }
      }
    },
    handleSubmit (value) {
      console.log(this.formValidate)
      this.$refs[value].validate((valid) => {
        if (valid) {
          setTimeout(() => {
            let requireData = {
              name: this.formValidate.bucket_name,
              status: this.formValidate.security_state ? "1" : "0",
              remark: this.formValidate.bucket_remark
            }
            console.log(requireData)
            updateRemark(requireData).then(res => {
              if (res.data.code === 0) {
                console.log(res.data)
                this.$Message.success(`${res.data.msg}`)
                this.getDBList(
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
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    },
    // 删除DB
    // handlerDeleteDB (params) {
    //   if (confirm(`确定要删除数据库 ${params.row.db_code}`)) {
    //     operationDB({db_id: params.row.id}, 'delete').then(
    //       res => {
    //         if (res.data.code === 0) {
    //           this.$Message.success(`${res.data.msg}`)
    //           this.getDBList('tag_name', this.selectTag)
    //         } else {
    //           this.$Message.error(`${res.data.msg}`)
    //         }
    //       })
    //   }
    // },
    // 删除
    // delData (params) {
    //   if (confirm(`确定要删除 ${params.row.db_code}`)) {
    //     operationDB(
    //       {
    //         id: params.row.id
    //       },
    //       'delete'
    //     ).then(res => {
    //       if (res.data.code === 0) {
    //         this.$Message.success(`${res.data.msg}`)
    //         this.tableData.splice(params.index, 1)
    //       } else {
    //         this.$Message.error(`${res.data.msg}`)
    //       }
    //     })
    //   }
    // },
    // setDefaultSearchKey() {
    //   this.searchKey =
    //     this.columns[0].key && this.columns[0].key !== "handle"
    //       ? this.columns[0].key
    //       : this.columns.length > 1
    //       ? this.columns[1].key
    //       : "";
    // },
    handleClear (e) {
      if (e.target.value === '') this.tableData = this.value
    },
    handleSearch () {
      // this.getDBList(this.pageNum, this.pageSize, this.searchKey, this.searchValue)
      this.getDBList(this.searchValue)
    },
    changePage (value) {
      if (this.searchValue) {
        this.getDBList(this.searchValue)
      } else if (this.selectTag) {
        this.getDBList('tag_name', this.selectTag)
      } else {
        this.pageNum = value
        this.getDBList(this.searchKey, this.searchVal,this.pageNum, this.pageSize)
      }
      // this.pageNum = value
      // this.getDBList(
      //     this.pageNum,
      //     this.pageSize,
      //     this.searchKey,
      //     this.searchValue
      //   )
    },
    // 每页条数
    handlePageSize (value) {
      if (this.searchValue) {
        this.getDBList(this.searchValue)
      } else if (this.selectTag) {
        this.getDBList('tag_name', this.tag_name)
      } else {
        this.pageSize = value
        this.getDBList(this.searchVal)
      }
      // this.pageSize = value
      // this.operationDB(1, this.pageSize, this.searchKey, this.searchValue)
    }
  },
  // watch: {
  //   searchVal (val) {
  //     this.searchVal = val
  //     this.getDBList(this.searchVal)
  //     // if(this.selectTwo === 'tag'){
  //     //   this.getTagList("tag_name", this.searchVal)
  //     // }else if(this.selectTwo === 'DB'){
  //     //   this.getDBList(this.searchVal)
  //     // }else if(this.selectTwo === 'server'){
  //     //   this.getServerList(this.searchVal)
  //     // }
  //   }
  // },

  mounted () {
    this.getDBList()
    // this.getIDCList()
  }
}
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
