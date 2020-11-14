using System;
using System.Linq;
using System.Net;
using DnsClient;
using DnsClient.Protocol;

Console.WriteLine("Testing lookup");

var endpoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 10053);
var client = new LookupClient(endpoint);

for (int i = 1; i <= 10; i++) {
    var host = $"host-{i}.bitchmints.com";
    Console.WriteLine($"Performing lookup for {host}");
    var results = client
        .Query(host, QueryType.A)
        .Answers
        .ARecords();

    if (results.Any()) {
        foreach (var aRecord in results) {
            Console.WriteLine($"\tDomain: {aRecord.DomainName} resolved to {aRecord.Address}");
        }
    } else {
        Console.WriteLine($"\tDomain: {host} was not found");
    }
}
