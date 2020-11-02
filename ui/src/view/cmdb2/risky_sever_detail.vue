<template>
<Modal width="800px;" v-model="dialog.show"  :title="dialog.title" :loading=true :footer-hide=true>
    <Card dis-hover>
      <div class="inner" >
        <Alert show-icon>基本信息</Alert>
            <div style="margin-top:10px;margin-bottom:10px">
                <Row>
                    <Col span="4"><p> <b>实例ID：</b> </p></Col>
                    <Col span="20"><p> {{formData.server_instance_id}} </p></Col>
                </Row>

                <Row>
                    <Col span="4"><p> <b>实例名称：</b></p></Col>
                    <Col span="20"><p><Tag color="blue"> {{formData.server_name}}</tag></p></Col>
                </Row>
                <Row>
                    <Col span="4"><p> <b>所属项目：</b> </p></Col>
                    <Col span="20"><p> {{formData.server_Project}}</p></Col>
                </Row>
                <Row>
                    <Col span="4"><p> <b>实例状态：</b> </p></Col>
                    <Col span="8"><p> <Tag color="blue">{{formData.security_state ? '安全': '不安全'}}</tag> </p></Col>
                    <!-- <Col span="4"><p> <b>实例类型：</b> </p></Col>
                    <Col span="8"><p> {{formData.instance_type}} </p></Col> -->
                </Row>
                <Row>
                    <Col span="4"><p> <b>公网IP地址：</b> </p></Col>
                    <Col span="20"><p> <Tag color="blue">{{formData.server_public_ip}}</tag> </p></Col>

                </Row>
                <Row>
                    <Col span="4"><p> <b>相关安全组</b> </p></Col>
                    <Col span="20"><p> <Tag color="blue" v-for="item in formData.security_group" :key="item">{{item}}</tag> </p></Col>
                </Row>
                <Row>
                    <Col span="4"><p> <b>风险端口</b> </p></Col>
                    <Col span="20"><p> <Tag color="red" v-for="item in formData.risk_port" :key="item">{{item}}</tag> </p></Col>
                </Row>

                <Row>
                    <Col span="4"><p> <b>备注</b>  </p></Col>
                    <Col span="20"><p> {{formData.server_mark}} </p></Col>
                </Row>
                <!-- <Row>
                    <Col span="4"><p> <b>最后一次更新时间</b>  </p></Col>
                    <Col span="20"><p> {{formData.update_time}} </p></Col>
                </Row> -->

            </div>
      </div>
    </Card>
</Modal>

</template>
<script>
export default {
  name: 'detail',
  props: {
    dialog: Object,
    formData: Object
  }
}
</script>
