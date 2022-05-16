import { apiService } from "./";
import axios from "axios";
import router from "../router";

const API_URL = '/jwt/';

class AuthService {
    login(user) {
        return apiService
            .post(API_URL, {
                username: user.username,
                password: user.password,
            })
            .then(response => {
                if (response.data.access) {
                    localStorage.setItem('user', JSON.stringify(response.data));
                }

                return response.data;
            });
    }

    async refresh() {
        const user = JSON.parse(localStorage.getItem('user'));
        if (user && user.refresh) {
            try {
                const response = await axios.post((process.env.VUE_APP_API_BASE_URL || '') + API_URL + 'refresh/', {
                    refresh: user.refresh
                })
                if (response.data.access) {
                    user.access = response.data.access;
                    localStorage.setItem('user', JSON.stringify(user));
                    console.log("token refreshed");
                    return response.data.access;
                }
            } catch {
                return null
            }
        }
    }

    logout() {
        localStorage.clear();
        router.push({ name: "Login" })
    }
}

export default new AuthService();
