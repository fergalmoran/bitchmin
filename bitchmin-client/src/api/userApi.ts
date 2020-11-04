import axios, { AxiosResponse, AxiosRequestConfig } from 'axios';
import { Api } from '@/api/apiBase';

import { apiConfig } from '@/api/config';
import { ApiResult, DataApiResult } from '@/api/apiResult';
import { User } from '@/models';

export class UserApi extends Api {
    constructor(config: AxiosRequestConfig) {
    // NEVER FORGET THE SUPER
        super(config);
    }

    public async getUser(): Promise<User> {
        const result = await this.get<DataApiResult<User>>('/user');
        return result.data.payload || { fullName: '' };
    }
}
export const userApi = new UserApi(apiConfig);
