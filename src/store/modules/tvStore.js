/*
 * @Description: 
 * @Author: sky
 * @Date: 2024-12-30 09:02:00
 * @LastEditTime: 2025-01-03 14:39:57
 * @LastEditors: sky
 */

import { defineStore } from 'pinia';
import { store } from '@/store';

export const useTvStore = defineStore({
    id: 'tv-store',
    state: () => ({
        tvDetails: {}
    }),
    actions: {
        setTvDetails(tv) {
            this.tvDetails = tv;
        },
        clearTvDetails() {
            this.tvDetails = {}
        }
    }
});

export function useTvStoreHook() {
    return useTvStore(store);
}
