import {apiService} from '@/services';

const API_URL = '/v1/users/';

class UserService {
    get(id) {
        return apiService.get(`${API_URL}${id}/`);
    }

    partial(data) {
        const id = data.id;
        delete data.id;
        return apiService.patch(`${API_URL}${id}/`, data)
    }
}

export default new UserService();
