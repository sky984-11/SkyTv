
import { defineStore } from 'pinia';
import { store } from '@/store';

export const useTvStore = defineStore({
    id: 'tv-store',
    state: () => ({
        tvDetails: []
    }),
    actions: {
        setTvDetails(tv) {
            this.tvDetails = tv;
        },
        clearTvDetails() {
            this.tvDetails = [];
        }
    }
});

export function useTvStoreHook() {
    return useTvStore(store);
}
