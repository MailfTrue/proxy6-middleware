import {apiService} from '@/services';

const API_URL = '/v1/proxy';

class ProxyService {
    list() {
        return apiService.get(`${API_URL}/list`);
    }

    price(params) {
        return apiService.get(`${API_URL}/price`, {params});
    }

    count(params) {
        return apiService.get(`${API_URL}/count`, {params});
    }

    countries() {
        return apiService.get(`${API_URL}/countries`);
    }

    buy(params) {
        return apiService.get(`${API_URL}/buy`, {params});
    }

    delete(params) {
        return apiService.get(`${API_URL}/delete`, {params});
    }
}

export default new ProxyService();
