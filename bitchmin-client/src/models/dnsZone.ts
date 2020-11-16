import { DnsHost } from '@/models/dnsHost';

export interface DnsZone {
    id: number;
    zone: string;
    hosts: DnsHost[];
}
