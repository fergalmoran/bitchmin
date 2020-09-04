import axios, { AxiosResponse } from 'axios';
import { Api } from '@/api/apiBase';
import { AxiosRequestConfig } from 'axios';
import { apiConfig } from '@/api/config';
import { ApiResult, DataApiResult } from '@/api/apiResult';
import { User } from '@/models/interfaces';

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
