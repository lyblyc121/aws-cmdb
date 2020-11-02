<template>
<div>
    <Input
              placeholder="输入关键字全局搜索"
              class="search-input"
              v-model="searchValue"
            />
            <Button @click="handleSearch" class="search-btn" type="primary">搜索</Button>
            <Button @click="handleSearch" class="search-btn" type="primary">更新数据</Button>
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
export default {
    data(){
        return{
            columns: [
                {
                    title: "用户名",
                    key: "hostid",
                    minWidth: 150,
                    align: "center",
                },
                {
                    title: "状态",
                    key: "hostname",
                    minWidth: 150,
                    align: "center",
                },
                {
                    title: "subnetId",
                    key: "project",
                    minWidth: 160,
                    align: "center",
                },
                {
                    title: "vpcid",
                    key: "require",
                    width: 100,
                    align: "center",
                },
                {
                    title: "是否可用",
                    key: "prepare",
                    width: 100,
                    align: "center",
                }
            ],
        }
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
