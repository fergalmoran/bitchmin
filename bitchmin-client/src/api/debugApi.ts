import axios, { AxiosResponse, AxiosRequestConfig } from 'axios';
import { Api } from '@/api/apiBase';

import { apiConfig } from '@/api/config';
import { ApiResult, DataApiResult } from '@/api/apiResult';
import { User } from '@/models';

export class DebugApi extends Api {
    constructor(config: AxiosRequestConfig) {
    // NEVER FORGET THE SUPER
        super(config);
    }

    public async getDebug(): Promise<string> {
        const result = await this.get<DataApiResult<string>>('/debug');
        return result.data.payload || '';
    }
}
export const debugApi = new DebugApi(apiConfig);
