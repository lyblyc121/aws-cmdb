import axios from '@/libs/api.request';
import config from '@/config';


// 资源使用率api
// 获取资源列表
export const getResourceList = (pageNum, pageSize, month, key) => {
	return axios.request({
		url: '/usage/v1/usage/report/',
		method: 'get',
		params: {
			pageNum,
			pageSize,
			month,
			key
		}
	})
};

// 获取展示在页面开头的月份
export const getDisplayMonthList = () => {
	return axios.request({
		url: '/usage/v1/usage/report/months/',
		method: 'get'
	})
};

// 获取具体某台机器某月使用情况
export const getHostUsageDetail = (ec2_id, month) => {
	return axios.request({
		url: '/usage/v1/usage/resource/',
		method: 'get',
		params: {
            ec2_id,
            month
		}
	})
};


// 预留实例部分api
// 获取预留实例列表
export const getReserverdList = (pageNum, pageSize, key) => {
	return axios.request({
		url: '/usage/v1/ri-usage/today/',
		method: 'get',
		params: {
			pageNum,
			pageSize,
			key
		}
	})
};

export const getReservedDetail = (start_day, end_day, family, size, platform) => {
	return axios.request({
		url: '/usage/v1/ri-usage/history/',
		method: 'get',
		params: {
			start_day,
			end_day,
			family,
			size,
			platform
		}
	})
};