# SPL useful for Splunk intelligence

# to get the Heavy Forwarder traffic volume
index=_internal sourcetype=splunkd group=tcpin_connections (connectionType=cooked OR connectionType=cookedSSL) fwdType=full guid=* 
| eval dest_uri = host.":".destPort 
| stats values(fwdType) as forwarder_type, latest(version) as version, values(arch) as arch, dc(dest_uri) as dest_count, values(os) as os, max(_time) as last_connected, sum(kb) as new_sum_kb, sparkline(avg(tcp_KBps), 1m) as avg_tcp_kbps_sparkline, avg(tcp_KBps) as avg_tcp_kbps, avg(tcp_eps) as avg_tcp_eps by hostname 


index=_internal sourcetype=splunkd group=tcpin_connections (connectionType=cooked OR connectionType=cookedSSL) fwdType=full guid=*
| eval gb = kb/1024/1024
| convert timeformat="%Y-%m-%d %H:%M:%S" ctime(_time) AS time
| stats latest(version) as version, values(os) as os, max(time) as last_connected, sum(gb) as "Traffic(GB)", sparkline(avg(tcp_KBps), 1m) as avg_tcp_kbps_spark, avg(tcp_KBps) as avg_tcp_kbps, avg(tcp_eps) as avg_tcp_eps by hostname
| addcoltotals "Traffic(GB)"

#Forwarders connecting directly to indexer, both UF and HF
index=_internal source=*metrics.log group=tcpin_connections 
    [ search index=_internal splunk_server=* earliest=-5m 
    | dedup splunk_server 
    | eval host=splunk_server 
    | fields host 
    | format] 
| stats values(os) as os values(version) as version values(hostname) as hostname values(guid) as guid values(fwdType) as fwdType values(ssl) as ssl values(connectionType) as connectionType by sourceIp

#Fowarders connection
index=_internal  group=tcp*_connections   sourcetype=splunkd 
| eval temp=split(lastIndexer,":") | eval forwardedtoport=mvindex(temp,1)
| eval LastTime=strftime(_time, "%c") 
| eventstats dc(group) as GROUP  by host
| eval isIF=if(GROUP==2,"yes","no")
| eval ingest_pipe=if(isnull(ingest_pipe),"1",ingest_pipe)
| stats  max(LastTime) as LastTime  values(lastIndexer) as "Forwared To"  values(host) as "Receiving Host" values(forwardedtoport) as "Receiving Port" values(connectionType) as "Conn Type" values(ssl) as "SSL Enabled"  values(fwdType) as fwdType values(isIF) as "Receiving Host is IF"  max(tcp_KBps) as "max tcp_KBps by Receiving Host"  by hostname ingest_pipe
| appendcols [search index=_internal group=per_source_thruput series=*splunkd.log 
| stats max(kbps) as maxkbps avg(kbps) as avgkbps-fwd perc25(kbps) as perc25kbps-fwd median(kbps) as mediamkbps-fwd perc75(kbps) as perc75kbps-fwd perc90(kbps) as pertc90kbps-fwd by host | rename host as hostname]
| foreach *kbps* [eval <<FIELD>>=round('<<FIELD>>', 5)]
| search hostname=SOMEHOST


### Data routing by cluster
```
index=_internal  group=tcpout_connections  tcp_KBps>0 host= <<HF_SERVER>>
| rex field=name "(?<tcp_group>[\w\-]+):(?<dst_ip>\d+.\d+.\d+.\d+:\d+):\d+"
| timechart span=1m avg(tcp_KBps) by tcp_group
```

### Logit Hourly License Usage 
```
index=_internal host=auirsspl015* source=*license_usage.log* type=Usage 
| eval GB = round(b/1024/1024/1024,5) 
| eval platform=if(pool == "logit-aws", "AWS", "legacy")
| timechart usenull=f span=1h sum(GB) as GB by platform
| addtotals
| eval percent = AWS/Total
```

### connection to indexers
```
index=_internal source=*metrics.log* group=tcpin_connections host=<INDEXERS>
| dedup hostname destPort 
| table _time hostname version fwdType ack os sourceIp destPort ssl 
| sort version
```

### indexing distribution
```
index=_internal host=gen-idx* sourcetype=splunkd source=*metrics.log component=Metrics group=queue 
| eval fill_perc = round(current_size_kb / max_size_kb * 100) 
| eval agg_fill_perc = case(match(name, "aggqueue"), fill_perc) 
| eval parsing_fill_perc = case(match(name, "parsingqueue*"), fill_perc) 
| eval index_fill_perc = case(match(name, "indexqueue*"), fill_perc) 
| eval typing_fill_perc = case(match(name, "typingqueue*"), fill_perc) 
| timechart span=5m perc90(index_fill_perc) by host useother=f
```

### blocked output
```
index=_internal sourcetype = splunkd host=* source=*splunkd.log blocked seconds 
| rex field=_raw "Forwarding to output group (?<output_group>\S+)\shas been blocked for (?<block_seconds>\d+)\sseconds" 
| where block_seconds > 300
| eval cluster = case(output_group == "splunkssl", "AWS", output_group LIKE "%luster%2", "Cluster02", output_group == "default-autolb-group", "Cluster01", output_group LIKE "%luster%1", "Cluster01")
| table _time host cluster block_seconds
```

### missing indexes events
```
| rest /services/messages 
| table title message severity timeCreated_iso published server splunk_server author
| rex field=message "So far received events from (?<missing_indexes>\d+) missing"
| where missing_indexes > 0
```
