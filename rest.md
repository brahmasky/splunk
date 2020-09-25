## adding proxy
- curl -k -u admin:password https://localhost:8089/services/server/httpsettings/proxysettings -d name="proxyConfig"
- curl -k -u admin:password https://localhost:8089/services/server/httpsettings/proxysettings/proxyConfig -d no_proxy="test"
- curl -k -u admin:password https://localhost:8089/services/properties/ui-prefs/default/display.prefs.enableMetaData -d value="0"


## HEC
curl  http://localhost:8088/services/collector/event -H "Authorization: Splunk 123-123-123" -d '{"event": "hello paco"}'

```
| rest splunk_server=<indexer> /servicesNS/-/-/configs/conf-indexes
| search disabled=0 
| fields eai:acl.app eai:appName title path maxDataSize maxTotalDataSizeMB  maxHotBuckets frozenTimePeriodInSecs 
``` 
``` 
| rest splunk_server=<indexer> /servicesNS/-/-/configs/conf-indexes
| search disabled=0
| fields eai:acl.app eai:appName title path maxDataSize maxTotalDataSizeMB  maxHotBuckets  frozenTimePeriodInSecs
| eval cm = "cm7"
| fields cm eai:acl.app eai:appName title path maxDataSize maxTotalDataSizeMB  maxHotBuckets  frozenTimePeriodInSecs
| collect index=<index_summary> source=discovery:indexes testmode=true
```
```
|rest splunk_server=<<SH>> serviceNS/-/-/configs/conf-server
```

## update conf file property
- curl -k -u admin:<PWD> https://localhost:8089/servicesNS/nobody/myapp/configs/conf-default-mode/ -d name=pipeline:scheduler -d disabled=true
- curl -k -u admin:<PWD> --request DELETE https://localhost:8089/servicesNS/nobody/myapp/configs/conf-default-mode/pipeline:scheduler
