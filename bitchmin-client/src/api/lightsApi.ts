import axios, { AxiosResponse, AxiosRequestConfig } from 'axios';
import { Api } from '@/api/apiBase';

import { apiConfig } from '@/api/config';
import { Light } from '@/models';
import { ApiResult, DataApiResult } from './apiResult';

export class LightsApi extends Api {
  constructor(config: AxiosRequestConfig) {
    // NEVER FORGET THE SUPER
    super(config);
  }

  async getLights(): Promise<Light[]> {
    const lights = await this.get<DataApiResult<Light[]>>(
      '/lights/getlights',
    );
    return lights.data.payload || [];
  }

  async changeBrightness(
    lightId: number,
    brightness: number,
  ): Promise<boolean> {
    const result = await this.post<
            ApiResult,
            any,
            AxiosResponse<ApiResult>
        >('/lights/setbrightness', {
          lightId,
          brightness,
        });
    return result.data.status === 'success';
  }

  async changeColour(
    lightId: number,
    colour: string,
  ): Promise<boolean> {
    const result = await this.post<
             ApiResult,
             any,
             AxiosResponse<ApiResult>
         >('/lights/changecolour', {
           lightId,
           rgbColour: colour,
         });
    return result.data.status === 'success';
  }
}
export const lightsApi = new LightsApi(apiConfig);
