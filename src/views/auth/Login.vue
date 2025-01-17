<!--
 * @Description: 
 * @Author: sky
 * @Date: 2025-01-14 14:10:32
 * @LastEditTime: 2025-01-16 08:29:41
 * @LastEditors: sky
-->
<script setup>
import { ref } from 'vue';
import { login } from "@/api/user";
import { setToken } from "@/utils/auth";
import { useRouter } from 'vue-router';
const router = useRouter();

const username = ref('');
const password = ref('');
const checked = ref(false);

const handleSubmit = async () => {
    const params = {
        username: username.value,
        password: password.value,
    };
    const formData = new FormData();
    formData.append('username', params.username);
    formData.append('password', params.password);

    const data = await login(formData)
    if(data.code === 200){
        setToken(data.data.token)
        router.push({ name: 'Home' });
    }
};
</script>

<template>
    <div class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center  min-w-[100vw] overflow-hidden">
        <div class="flex flex-col items-center justify-center">
            <div
                style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full bg-surface-0 dark:bg-surface-900 py-20 px-8 sm:px-20" style="border-radius: 53px">
                    <div class="text-center mb-8">
                        <van-image width="100" height="100" src="/favicon.ico" />
                        <h1 class="text-xl font-bold">SkyAnime</h1>
                    </div>

                    <van-form @submit="handleSubmit">
                        <van-cell-group inset>
                            <van-field v-model="username" name="用户名" label="用户名" placeholder="用户名"
                                :rules="[{ required: true, message: '请填写用户名' }]" />
                            <van-field v-model="password" type="password" name="密码" label="密码" placeholder="密码"
                                :rules="[{ required: true, message: '请填写密码' }]" />
                        </van-cell-group>
                        <div style="margin: 16px;">
                            <van-button round block type="primary" native-type="submit">
                                提交
                            </van-button>
                        </div>
                    </van-form>
                </div>
            </div>
        </div>
    </div>
</template>
