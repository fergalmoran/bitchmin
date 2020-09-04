import { Api } from './apiBase';
import { AxiosRequestConfig, AxiosResponse } from 'axios';
import {} from '@/models/interfaces/';
import { apiConfig } from './config';
import { AuthResult } from '@/models/interfaces';
import axios from 'axios';
import { UserLoginModel } from '@/models/interfaces/userLoginModel';
import store from '@/store';

export class AuthApi extends Api {
    constructor(config: AxiosRequestConfig) {
        // NEVER FORGET THE SUPER
        super(config);
    }

    public login(user: UserLoginModel): Promise<AxiosResponse<AuthResult>> {
        return this.post('/auth/login/', user);
    }
    public register(user: UserLoginModel) {
        return this.post('/auth/register/', user);
    }
}
export const authApi = new AuthApi(apiConfig);
