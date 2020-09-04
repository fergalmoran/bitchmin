import { Api } from '@/api/apiBase';
import { AxiosRequestConfig, AxiosResponse } from 'axios';
import { apiConfig } from '@/api/config';
import { ApiResult, DataApiResult } from '@/api/apiResult';
import { DnsRecord } from '@/models/dnsRecord';

export class DnsApi extends Api {
  constructor(config: AxiosRequestConfig) {
    // NEVER FORGET THE SUPER
    super(config);
  }

  public async updateDnsRecord(
    hostName: string,
    ipAddress: string,
  ): Promise<DataApiResult<DnsRecord>> {
    const result = await this.post<
            ApiResult,
            any,
            AxiosResponse<DataApiResult<DnsRecord>>
        >('/dns/', {
          host: hostName,
          ip: ipAddress,
        });
    return result.data;
  }

  public async deleteDnsRecord(
    hostName: string,
  ): Promise<number> {
    const result = await this.delete(`/dns/?host=${hostName}`);
    return result.status;
  }

  public async refreshDnsRecord(
    hostName: string,
    ip: string,
  ): Promise<DataApiResult<DnsRecord>> {
    const result = await this.post<
            ApiResult,
            any,
            AxiosResponse<DataApiResult<DnsRecord>>
        >('/dns/refresh', {
          host: hostName,
          ip,
        });
    return result.data;
  }

  public async verifyDnsRecord(
    hostName: string,
    ip: string,
  ): Promise<DataApiResult<string>> {
    const result = await this.post<
            ApiResult,
            any,
            AxiosResponse<DataApiResult<string>>
        >('/dns/check/', {
          host: hostName,
          ip,
        });
    return result.data;
  }

  public async getDnsRecords(): Promise<DnsRecord[]> {
    const result = await this.get<DnsRecord[]>('/dns/list');
    return result.data;
  }

  public async getMyIP(): Promise<string> {
    const result = await this.get<DataApiResult<string>>('/dns/myip');
    return result.data.payload || 'Unknown IP';
  }

  public async getHeaders(): Promise<any> {
    const result = await this.get<DataApiResult<any>>('/dns/headers');
    return result.data.payload;
  }
}
export const dnsApi = new DnsApi(apiConfig);
