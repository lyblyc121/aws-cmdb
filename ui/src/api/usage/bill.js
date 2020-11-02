import axios from '@/libs/api.request';
import config from '@/config';

// 账单API
// 获取某月所有服务账单
export const getTotalBillMonthly = (month) => {
	return axios.request({
		url: '/usage/v1/usage/bill/',
		method: 'get',
		params: {
			month,
		}
	})
}

export const getDisplaySerYear = (key) => {
    return axios.request({
		url: '/usage/v1/usage/bill/display/',
        method: 'get',
        params: {
            key
        }
	})
}

export const getServiceBill = (service, year) => {
    return axios.request({
		url: '/usage/v1/usage/bill/service/',
        method: 'get',
        params: {
            service,
            year
        }
	})
}


// export const getTotalBillMonthly = (month) => {
// 	return axios.request({
// 		url: '/usage/v1/usage/bill/',
// 		method: 'post'
// 	})
// };
