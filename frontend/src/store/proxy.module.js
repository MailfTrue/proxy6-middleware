import ProxyService from '../services/proxy.service'

export const proxy = {
    namespaced: true,
    state: {
        list: null,
        countries: null,
    },
    getters: {
        list: (state) => state.list,
        countries: (state) => state.countries,
    },
    actions: {
        loadList({commit}) {
            return ProxyService.list().then(
                res => {
                    commit('listSuccess', res.data.list);
                },
                () => {
                    commit('listFailed');
                }
            );
        },
        loadCountries({commit}) {
            return ProxyService.countries().then(
                res => {
                    commit('countriesSuccess', res.data.list);
                },
                () => {
                    commit('countriesFailed');
                }
            );
        },
    },
    mutations: {
        listSuccess(state, list) {
            state.list = list;
        },
        listFailed(state) {
            state.list = null
        },
        countriesSuccess(state, countries) {
            state.countries = countries;
        },
        countriesFailed(state) {
            state.countries = null
        },
    }
};