import axios from '@/libs/api.request';
import config from '@/config';

export const getBillList = (page, limit, type, date) => {
	return axios.request({
		url: '/cmdb2/v1/cmdb/bill/',
		method: 'get',
		params: {
			type,
			date,
			page,
			limit
		}
	})
};

