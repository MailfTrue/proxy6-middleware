import axios from 'axios';
import qs from 'qs';
import authService from "@/services/auth.service";
import store from "@/store";
import {router} from "@/router";

export const baseURL = process.env.VUE_APP_API_BASE_URL || '';

export const apiService = axios.create({
    baseURL,
    transformRequest: [
        (data, headers) => {
            const user = JSON.parse(localStorage.getItem('user'));
            if (user && user.access)
                headers["Authorization"] = `Bearer ${user.access}`;
            return data;
        },
        ...axios.defaults.transformRequest
    ],
    paramsSerializer: function (params) {
        function filterNonNull(obj) {
            return Object.fromEntries(Object.entries(obj).filter(([, v]) => {
                if (typeof v === 'undefined' || v === null) return false
                if (typeof v === 'string' && v.length === 0) return false
                return true
            }));
        }
        return qs.stringify(filterNonNull(params), {arrayFormat: 'repeat'})
    },
})

const REFRESH_ENDPOINT = '/api/token/refresh/';

apiService.interceptors.response.use((response) => {
    return response
}, async function (error) {
    const originalRequest = error.config;
    const responseStatus = error?.response?.status;
    const tokenNotValid = error?.response?.data?.code === 'token_not_valid';
    if ((responseStatus === 401 || tokenNotValid) && !originalRequest._retry && originalRequest.url !== REFRESH_ENDPOINT) {
        originalRequest._retry = true;
        const access_token = await authService.refresh();
        if (access_token)
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
        else {
            await store.dispatch('auth/logout')
            await router.push({name: "Login"});
        }
        return apiService(originalRequest);
    }
    if (originalRequest._retry && localStorage.getItem('user')) {
        localStorage.removeItem("user");
        delete axios.defaults.headers.common['Authorization'];
        return apiService(originalRequest);
    }

    // Логируем ошибки
    if (responseStatus !== 401) {
        const errorData = error.response.data;
        let text = 'Неизвестная ошибка';
        if (errorData instanceof Object) {
            text = Object.values(errorData).join(', ')
        } else if (responseStatus) {
            text = 'Сервер недоступен'
        }
        console.log("Ошибка:", text)
    }
    return Promise.reject(error);
});
