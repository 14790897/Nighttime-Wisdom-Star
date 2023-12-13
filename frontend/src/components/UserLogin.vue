<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card border-primary my-5">
                    <h2 class="mb-3">{{ $t('message.login') }}</h2>
                    <div class="card-body">
                        <form @submit.prevent="submitForm">
                            <div class="form-group">
                                <label for="username">Username</label>
                                <input id="username" v-model="username" type="text" class="form-control"
                                    placeholder="Username">
                            </div>
                            <div class="form-group">
                                <label for="password">Password</label>
                                <input id="password" v-model="password" type="password" class="form-control"
                                    placeholder="Password">
                            </div>
                            <button type="submit" class="btn btn-primary w-100">{{ $t('message.login') }}</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
    data() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        ...mapMutations(['setUsername']),
        async submitForm() {
            try {
                let response = await this.$http.post('/api/login', {
                    username: this.username,
                    password: this.password
                });
                if (response.data.status === 'success') {
                    this.setUsername(this.username);
                    this.$router.push({ name: 'Home' });
                } else {
                    // 显示登录失败的原因
                    alert(this.$t('message.loginFailed1') + ': ' + response.data.message);
                }
            } catch (error) {
                // 在这里处理错误，显示错误信息
                let errorMessage = error.response && error.response.data ? error.response.data.message : error.message;
                alert(this.$t('message.loginFailed2') + ': ' + errorMessage);
            }
        }
    }
}
</script>

<style scoped>
.container {
    margin-top: 100px;
}
</style>
