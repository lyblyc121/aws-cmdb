import axios from '@/libs/api.request';
import config from '@/config';

export const getResourceList = (page, limit, key, value) => {
	return axios.request({
		url: '/cmdb2/v1/cmdb/resource/',
		method: 'get',
		params: {
			key,
			value,
			page,
			limit
		}
	})
};


export const getResourceDetailList = (key, value) => {
	return axios.request({
		url: '/cmdb2/v1/cmdb/resource_detail',
        method: 'get',
        params: {
            key,
            value
        }
		
	})
};


export const getResourceUsage = (id, date) => {
    return axios.request({
        url: '/cmdb2/v1/cmdb/resource_usage',
        method: 'get',
        params: {
            id,
            date
        }
    })
}