import axios from '@/libs/api.request'
import config from '@/config'


// S3存储+ebs部分api+风险主机管理


// 风险主机API
// 获取风险主机列表
export const getRiskyServerList = (page, limit, key) => {
	return axios.request({
		url: '/cmdb2/v1/cmdb/dangers/',
		method: 'get',
		params: {
			key,
			page,
			limit
		}
	})
};

// 手动刷新，同步AWS的资产
export const syncAWShost = () => {
	return axios.request({
		url: '/cmdb2/v1/cmdb/dangers/',
		method: 'post'
	})
};

// 更新风险主机备注
export const updateRiskyServer = (data) => {
	return axios.request({
		url: '/cmdb2/v1/cmdb/dangers/',
		method: 'put',
		data
	})
};


// S3桶部分API
//获取S3列表
export const getDBlist= (page, limit, key) => {
  return axios.request({
    url: '/cmdb2/v1/cmdb/s3/',
    method: 'get',
    params: {
      page,
      limit,
      key
    }
  })
}

//更新S3桶备注信息
export const updateRemark = (data) => {
  return axios.request({
    url: '/cmdb2/v1/cmdb/s3/',
    method: 'put',
    data
  })
}


// EBS部分API
// 获取EBS列表
export const getEBSList = (page, limit, key) => {
  return axios.request({
    url: '/cmdb2/v1/cmdb/ebs/',
    method: 'get',
    params: {
      page,
      limit,
      key
    }
  })
}

// 同步AWS的EBS资产
export const getAWSEbs = () => {
  return axios.request({
    url: '/cmdb2/v1/cmdb/ebs/',
    method: 'post',
  })
}

// DNS部分API
// 获取DNS列表
export const getDNSList = (page, limit, key) => {
    return axios.request({
        url: '/cmdb2/v1/cmdb/dns/',
        method: 'get',
        params: {
            page,
            limit,
            key
        }

    })
}

// 标签查询
// 获取标签列表
export const getTagList = (page, limit, key) => {
    return axios.request({
        url: '/cmdb2/v1/cmdb/tag/',
        method: 'get',
        params: {
            page,
            limit,
            key
        }
    })
}