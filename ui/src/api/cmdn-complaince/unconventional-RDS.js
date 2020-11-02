import axios from '@/libs/api.request'

export const getRdsList = (key , page, size) => {
	return axios.request({
		url: `/v1/cmdb/rds?key=${key}&page=${page}&size=${size}`,
		method: 'get'
	})
};
