<template>
<div>
    <div class="search-box">
        <Input
              placeholder="输入关键字全局搜索"
              class="search-input"
              v-model="searchValue"
            />
        <Button @click="handleSearch" class="search-btn" type="primary">搜索</Button>
        <Button @click="handleSearch" class="search-btn" type="primary">更新数据</Button>
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
</div>
    
</template>

<script>
import { getRdsList } from "@/api/cmdn-complaince/unconventional-RDS.js"
export default {
    data(){
        return{
            columns: [
                {
                    title: "Identifier",
                    key: "db_Identifier",
                    minWidth: 120,
                    align: "center",
                },
                {
                    title: "区域",
                    key: "db_region",
                    minWidth: 120,
                    align: "center",
                },
                {
                    title: "host",
                    key: "db_host",
                    minWidth: 120,
                    align: "center",
                },
                {
                    title: "实例ID",
                    key: "db_instance_id",
                    width: 120,
                    align: "center",
                },
                {
                    title: "7天连接数",
                    key: "db_conn",
                    width: 120,
                    align: "center",
                },
                {
                    title: "公网访问",
                    key: "db_public_access",
                    width: 120,
                    align: "center",
                },
                {
                    title: "开启备份",
                    key: "db_backup",
                    width: 120,
                    align: "center",
                    render: (h, params) => {
                        if(params.row.db_backup===true){
                            return h('div',"是")
                        }else{
                            return h('div',"否")
                        }
                    }
                },
                {
                    title: "备份时间",
                    key: "db_backup_period",
                    width: 120,
                    align: "center",
                },
                {
                    title: "加密储存",
                    key: "db_enncrypted",
                    width: 120,
                    align: "center",
                }
            ],
            tableData:[
                {
                   db_Identifier: 'xxxxxxxxx',
                   db_region:  'xxxxxxxxxx',
                   db_host: 'xxxxxxxxx',
                   db_instance_id:'xxxxxxxx',
                   db_conn: 'xxxxxxxxx',
                   db_public_access: 'xxxxxxxxxx',
                   db_backup: true,
                   db_backup_period:'cccccccccccc',
                   db_enncrypted:'xxxxxxxxxxxxxxx'
                },
                {
                   db_Identifier: 'xxxxxxxxx',
                   db_region:  'xxxxxxxxxx',
                   db_host: 'xxxxxxxxx',
                   db_instance_id:'xxxxxxxx',
                   db_conn: 'xxxxxxxxx',
                   db_public_access: 'xxxxxxxxxx',
                   db_backup: 'mmmmm,mmmmmmmmm',
                   db_backup_period:'cccccccccccc',
                   db_enncrypted:'xxxxxxxxxxxxxxx'
                },
                {
                   db_Identifier: 'xxxxxxxxx',
                   db_region:  'xxxxxxxxxx',
                   db_host: 'xxxxxxxxx',
                   db_instance_id:'xxxxxxxx',
                   db_conn: 'xxxxxxxxx',
                   db_public_access: 'xxxxxxxxxx',
                   db_backup: 'mmmmm,mmmmmmmmm',
                   db_backup_period:'cccccccccccc',
                   db_enncrypted:'xxxxxxxxxxxxxxx'
                }
            ]
        }
    },
    methods: {
        getRdsDataList(){
            getRdsList(1,1,18),then(res=>{
                console.log(res)
            })
        }
    },
    mounted() {
        this.getRdsDataList()
    }
}
</script>

<style>
.search-box{
    padding-bottom: 20px;
}
.search-input{
    display: inline-block;
    width: 200px;
    margin-left: 2px;
}
.search-btn{
    margin-left: 20px;
}
</style>
