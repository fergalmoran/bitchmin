import { Api } from '@/api/apiBase';
import { AxiosRequestConfig, AxiosResponse } from 'axios';
import { apiConfig } from '@/api/config';
import { ApiResult, DataApiResult } from '@/api/apiResult';
import { DnsHost } from '@/models/dnsHost';
import { DnsZone } from '@/models/dnsZone';

export class DnsApi extends Api {
    constructor(config: AxiosRequestConfig) {
        super(config);
    }

    public async updateDnsRecord(
        zoneId: number,
        hostName: string,
        ipAddress: string
    ): Promise<DataApiResult<DnsHost>> {
        const result = await this.post<ApiResult,
            any,
            AxiosResponse<DataApiResult<DnsHost>>>('/dns/host/', {
            // eslint-disable-next-line @typescript-eslint/camelcase
                zone_id: zoneId,
                name: hostName,
                ip: ipAddress
            });
        return result.data;
    }

    public async deleteDnsRecord(
        hostName: string
    ): Promise<number> {
        const result = await this.delete(`/dns/?host=${hostName}`);
        return result.status;
    }

    public async refreshDnsRecord(
        hostName: string,
        ip: string
    ): Promise<DataApiResult<DnsHost>> {
        const result = await this.post<ApiResult,
            any,
            AxiosResponse<DataApiResult<DnsHost>>>(
                '/dns/refresh', {
                    host: hostName,
                    ip
                }
            );
        return result.data;
    }

    public async verifyDnsRecord(
        hostName: string,
        ip: string
    ): Promise<DataApiResult<string>> {
        const result = await this.post<ApiResult,
            any,
            AxiosResponse<DataApiResult<string>>>('/dns/check/', {
                host: hostName,
                ip
            });
        return result.data;
    }

    public async getZones(): Promise<DnsZone[]> {
        const result = await this.get<DnsZone[]>('/dns/zones');
        return result.data;
    }

    public async getDnsRecords(): Promise<DnsHost[]> {
        const result = await this.get<DnsHost[]>('/dns/list');
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
