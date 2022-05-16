import AuthService from '../services/auth.service';
import UserService from "@/services/user.service";

const user = JSON.parse(localStorage.getItem('user'));
const initialState = user
    ? {status: {loggedIn: true}, user}
    : {status: {loggedIn: false}, user: null};

export const auth = {
    namespaced: true,
    state: {
        ...initialState,
        fullUser: null
    },
    getters: {
        userData(state) {
            return JSON.parse(atob(state.user.access.split(".")[1]))
        },
        isSuperuser: (state) => !!state.fullUser?.is_superuser,
        role: (state) => state.fullUser?.role,
        mainRegion: (state) => state.fullUser?.main_region,
        id: (state) => state.fullUser?.id,
    },
    actions: {
        login({commit}, {user, code}) {
            return AuthService.login(user, code).then(
                user => {
                    commit('loginSuccess', user);
                    return Promise.resolve(user);
                },
                error => {
                    commit('loginFailure');
                    return Promise.reject(error);
                }
            );
        },
        logout({commit}) {
            AuthService.logout();
            commit('logout');
        },
        getFullUser({commit, getters}) {
            UserService.get(getters.userData.user_id).then((res) => {
                commit("setFullUser", res.data)
            })
        },
        async update({dispatch, getters}, data) {
            await UserService.partial({id: getters.userData.user_id, ...data})
            await dispatch('getFullUser')
        }
    },
    mutations: {
        loginSuccess(state, user) {
            state.status.loggedIn = true;
            state.user = user;
        },
        loginFailure(state) {
            state.status.loggedIn = false;
            state.user = null;
        },
        logout(state) {
            state.status.loggedIn = false;
            state.user = null;
        },
        setFullUser(state, user) {
            state.fullUser = user
        }
    }
};