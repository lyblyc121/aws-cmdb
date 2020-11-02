import axios from '@/libs/api.request'

export const getElbList = (key , page, size) => {
	return axios.request({
		url: `/v1/cmdb/natgateway?key=${key}&page=${page}&size=${size}`,
		method: 'get'
	})
};
