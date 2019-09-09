### Question #:1
What options are available when creating custom roles? (select all that apply)
- **Restrict search terms**
- Whitelist search terms
- **Limit the number of concurrent search jobs**
- **Allow or restrict indexes that can be searched**

### Question #:2 
Where should apps be located on the deployment server that the clients pull from? 
- $SFLUNK_KOME/etc/apps
- $SPLUNK_HCME/etc/search
- $SPLUNK_HCME/etc/master-apps 
- **$SPLUNK HCME/etc/deployment-apps**

### Question #:3 
In case of a conflict between a whitelist and a blacklist input setting, which one is used? 
- Blacklist
- **Whitelist**
- They cancel each other out. 
- Whichever is entered into the configuration first. 

### Question #:4 
Which of the following are supported options when configuring optional network inputs? 
-  Metadata override, sender filtering options, network input queues (quantum queues) 
-  **Metadata override, sender filtering options, network input queues (memory/persistent queues)**
-  Filename override, sender filtering options, network output queues (memory/persistent queues) 
-  Metadata override, receiver filtering options, network input queues (memory/persistent queues) 

### Question #:5
How would you configure your distsearch conf to allow you to run the search below? 
sourcetype=access_combined status=200 action=purchase splunk_setver_group=HOUSTON 
```
[distributedSearch]
servers = nyc1:8089, nyc2:8089, houston1:8089, houston2:8089

[distributedSearch:NYC]
default = false
servers = nyc1:8089, nyc2:8089

[distributedSearch:HOUSTON]
default = false
servers = houston1:8089, houston2:8089
```

### Question #:6 
Which Splunk component consolidates the individual results and prepares reports in a distributed environment? 
- Indexers
- Forwarder 
- **Search head**
- Search peers 

### Question #:7 
Where can scripts for scripted inputs reside on the host file system? (select all that apply) 
- **$SFLUNK_HOME/bin/scripts**
- $SPLUNK_HOME/etc/apps/bin
- **$SPLUNK_HOME/etc/system/bin**
- $SPLUNK_HOME/etc/apps/<your_app>/bin_ 

### Question #:8 
The universal forwarder has which capabilities when sending data? (select all that apply) 
- Sending alerts
- **Compressing data**
- Obfuscating/hiding data 
- **Indexer acknowledgement**

### Question #:9 
Which of the following are supported configuration methods to add inputs on a forwarder? (select all that apply) 
- **CLI**
- **Edit inputs . conf**
- Edit forwarder.conf
- Forwarder Management 

### Question #:10 
When configuring monitor inputs with whitelists or blacklists, what is the supported method of filtering the lists? 
- Slash notation
- **Regular expression**
- Irregular expression
- Wildcard-only expression 

### Question #:11 
Local user accounts created in Splunk store passwords in which file? 
- **$SPLUNK_HOME/etc/passwd**
- $SPLUNK_HOME/etc/authentication
- $SPLUNK_HOME/etc/users/passwd.conf 
- $SPLUNK_HOME/etc/users/authentication.conf 

### Question #:12 
Which forwarder type can parse data prior to forwarding? 
- Universal forwarder
- Heaviest forwarder
- Hyper forwarder 
- **Heavy forwarder**

Question #:13 
Which of the following is valid distribute search group? 
```
[distributedSearch:Paris]
default = false
servers = server1:8089, server2:8089
```
 
### Question #:14 
For single line event sourcetypes. it is most efficient to set SHOULD_linemerge to what value? 
- True 
- **False**
- \<regex string\>
- Newline Character 

### Question #:15 
When running the command shown below, what is the default path in which deployment server.conf is created?
> splunk set deploy-poll deployServer:port
- SFLUNK_HOME/etc/deployment
- **SPLUNK_HOME/etc/system/local**
- SPLUNK_HOME/etc/system/default 
- SPLUNK_KOME/etc/apps/deployment 

### Question #:16 
Which of the following indexes come pre-configured with Splunk Enterprise? (select all that apply) 
- _license
- **_internal**
- _external 
- **_thefishbucket**


### Question #:17 
Which Splunk indexer operating system platform is supported when sending logs from a Windows universal forwarder? 
- **Any OS platform**
- Linux platform only
- Windows platform only. 
- None of the above. 

### Question #:18 
Which of the following statements describe deployment management? (select all that apply) 
- **Requires an Enterprise license**
- **Is responsible for sending apps to forwarders**
- Once used, is the only way to manage forwarders
- **Can automatically restart the host OS running the forwarder.**

### Question #:19 
How often does Splunk recheck the LDAP server? 
- Every 5 minutes
- **Each time a user logs in**
- Each time Splunk is restarted 
- Varies based on LDAP_refresh setting. 

### Question #:20 
What is the correct order of steps in Duo Multifactor Authentication? 
> A
> > 1. Request Login
> > 2. Connect to SAML server
> > 3. Duo MFA
> > 4. Create User session
> > 5. Authentication Granted
> > 6. Log into Splunk

>  B
> > 1. Request Login 
> > 2. Duo MFA
> > 3. Authentication Granted 
> > 4. Connect to SAML server 
> > 5. Log into Splunk
> > 6. Create User session 

> **C**
> > 1. Request Login 
> > 2. Check authentication / group mapping 
> > 3. Authentication Granted
> > 4. Duo MFA
> > 5. Create User session 
> > 6. Log into Splunk 

> D 
> > 1. Request Login 
> > 2. Duo MFA
> > 3. Check authentication / group mapping 
> > 4. Create User session
> > 5. Authentication Granted
> > 6. Log into Splunk 

### Question #:21 
In which Splunk configuration is the SEDCMD used? 
- **props, conf**
- inputs.conf
- indexes.conf 
- transforms.conf 

### Question #:22 
Which Splunk component performs indexing and responds to search requests from the search head? 
- Forwarder
- **Search peer**
- License master 
- Search head cluster 

### Question #:23 
In which phase of the index time process does the license metering occur? 
- input phase
- Parsing phase
- **Indexing phase**
- Licensing phase 

### Question #:25 
Which setting in indexes.conf allows data retention to be controlled by time? 
- maxDaysToKeep
- moveToFrozenAfter
- maxDataRetentionTime
- **frozenTimePeriodlnSecs**

### Question #:26 
Which optional configuration setting in inputs .conf allows you to selectively forward the data to specific indexer(s)? 
- **_TCP_ROUTING**
- _INDEXER_LIST
- _INDEXER_GROUP 
- _INDEXER ROUTING 

### Question #:27 
Which valid bucket types are searchable? (select all that apply) 
- **Hot buckets**
- Cold buckets
- **Warm buckets** 
- Frozen buckets 

Question #:28 
In this source definition the MAX_TIMESTAMP_LOOKHEAD is missing. Which value would fit best? 
￼` TIME_FORMAT = %Y-%m-%d %H:%M:%S.%3N %z `
￼
Event example: 

- MAX_TIMESTAMP_L0CKAHEAD = 5 
- MAX_TIMESTAMP_LOOKAHEAD - 10 
- MAX_TIMESTAMF_LOOKHEAD = 20 
- **MAX TIMESTAMP LOOKAHEAD - 30**

### Question #:29 
In which scenario would a Splunk Administrator want to enable data integrity check when creating an index? 
- To ensure that hot buckets are still open for writes and have not been forced to roll to a cold state
- To ensure that configuration files have not been tampered with for auditing and/or legal purposes
- To ensure that user passwords have not been tampered with for auditing and/or legal purposes. 
- **To ensure that data has not been tampered with for auditing and/or legal purposes**

### Question #:30 
To set up a Network input in Splunk, what needs to be specified? 
- File path.
- Username and password
- **Network protocol and port number.**
- Network protocol and MAC address. 

### Question #:31 
What is required when adding a native user to Splunk? (select all that apply) 
- **Password**
- **Username**
- Full Name 
- Default app 


### Question #:32 
- ch Splunk component does a search head primarily communicate with? 
- **Indexer**
- Forwarder
- Cluster master 
- Deployment server 

### Question #:33 
User role inheritance allows what to be inherited from the parent role? (select all that apply) 
- Parents
- **Capabilities**
- **Index access**
- Search history 

### Question #:34 
Which of the following apply to how distributed search works? (select all that apply) 
- **The search head dispatches searches to the peers**
- The search peers pull the data from the forwarders.
- **Peers run searches in parallel and return their portion of results.**
- **The search head consolidates the individual results and prepares reports**


### Question #:35 
How do you remove missing forwarders from the Monitoring Console? 
- By restarting Splunk. 
- By rescanning active forwarders.
- By reloading the deployment server.
- **By rebuilding the forwarder asset table.**

### Question #:36 
What is the difference between the two wildcards ... and * for the monitor stanza in inputs.conf? 
- … is not supported in monitor stanzas 
- There is no difference, they are interchangable and match anything beyond directory boundaries. 
- **\* matches anything in that specific directory path segment, whereas ... recurses through subdirectories as well.**
- … matches anything in that specific directory path segment, whereas * recurses through subdirectories as well.

### Question #:37 
Which layers are involved in Splunk configuration file layering? (select all that apply) 
- **App context**
- **User context**
- **Global context**
- Forwarder context 

### Question #:38 
What is the default character encoding used by Splunk during the input phase? 
- **UTF-8**
- UTF-16
- EBCDIC
- ISO 8859 

### Question #:39 
Which option accurately describes the purpose of the HTTP Event Collector (HEC)? 
- A token-based HTTP input that is secure and scalable and that requires the use of forwarders 
- **A token-based HTTP input that is secure and scalable and that does not require the use of forwarders.**
- An agent-based HTTP input that is secure and scalable and that does not require the use of forwarders. 
- A token-based HTTP input that is insecure and non-scalable and that does not require the use of forwarders.  

### Question #:40 
What are the minimum required settings when creating a network input in Splunk? 
- **Protocol, port number**
- Protocol, port, location
- Protocol, username, port 
- Protocol, IP. port number 

### Question #:41 
Which of the following are methods for adding inputs in Splunk? (select all that apply) 
- **CLI**
- **Splunk Web**
- **Editing inputs. conf**
- Editing monitor. conf 

### Question #:42 
Which Splunk forwarder type allows parsing of data before forwarding to an indexer? 
- Universal forwarder
- Parsing forwarder
- **Heavy forwarder**
- Advanced forwarder 

### Question #:43 
Which of the following statements apply to directory inputs? {select all that apply) 
- **All discovered text files are consumed.**
- Compressed files are ignored by default
- **Splunk recursively traverses through the directory structure.**
- When adding new log files to a monitored directory, the forwarder must be restarted to take them into account.

### Question #:44 
You update a props. conf file while Splunk is running. You do not restart Splunk and you run this command: 
> splunk btoo1 props list —debug
What will the output be? 
- list of all the configurations on-disk that Splunk contains.
- A verbose list of all configurations as they were when splunkd started.
- **A list of props. conf configurations as they are on-disk along with a file path from which the configuration is located**
- A list of the current running props, conf configurations along with a file path from which the configuration was made

### Question #:45
This file has been manually created on a universal forwarder 
￼> /opt/splunkforwarder/etc/apps/my_TA/local/inputs.conf
￼```
[monitor:///var/log/messages]
```
A new Splunk admin comes in and connects the universal forwarders to a deployment server and deploys the same app with a new 
￼￼> /opt/splunkforwarder/etc/apps/my_TA/local/inputs.conf
￼```
[monitor:///var/log/maillog]
```
 
Which file is now monitored?
- /var/log/messages
- **/var/log/maillog**
- /var/log/maillog and /var/log/messages 
- none of the above 

### Question #:46 
Within props. conf, which stanzas are valid for data modification? (select all that apply) 
- **Host**
- Server
- **Source**
- **Sourcetype** 

### Question #:47 
The priority of layered Splunk configuration files depends on the file's: 
- Owner
- Weight
- **Context**
- Creation time 

### Question #:48 
How does the Monitoring Console monitor forwarders? 
- By pulling internal logs from forwarders.
- By using the forwarder monitoring add-on
- **With internal logs forwarded by forwarders.**
- With internal logs forwarded by deployment server. 

### Question #:49 
What type of data is counted against the Enterprise license at a fixed 150 bytes per event? 
- License data
- **Metrics data**
- Internal Splunk data 
- Internal Windows logs 

### Question #:50 
When deploying apps, which attribute in the forwarder management interface determines the apps that clients install? 
- App Class 
- Client Class 
- **Server Class**
- Forwarder Class 

### Question #:51 
Which of the following are required when defining an index in indexes. conf? (select all that apply) 
- **coldPath**
- **homePath**
- frozenPath 
- **thawedPath**

### Question #:52 
What are the required stanza attributes when configuring the transforms. conf to manipulate or remove events? 
- REGEX, DEST. FORMAT
- REGEX. SRC_KEY, FORMAT
- **REGEX, DEST_KEY, FORMAT**
- REGEX, DEST_KEY FORMATTING 

###Question #:53 
Which authentication methods are natively supported within Splunk Enterprise? (select all that apply) 
- **LDAP**
- **SAML**
- RADIUS
- **Duo Multifactor Authentication**


### Question #:54 
During search time, which directory of configuration files has the highest precedence? 
- **$SFLUNK_KOME/etc/system/local**
- $SPLUNK_KCME/etc/system/default
- $SPLUNK_HCME/etc/apps/app1/local 
- $SPLUNK HCME/etc/users/admin/local 

### Question #:55 
Which Splunk component distributes apps and certain other configuration updates to search head cluster members? 
- **Deployer**
- Cluster master
- Deployment server
- Search head cluster master 

### Question #:56 
Which Splunk component requires a Forwarder license? 
- Search head
- **Heavy forwarder**
- Heaviest forwarder 
- Universal forwarder 

### Question #:57 
Which parent directory contains the configuration files in Splunk? 
- **$SPLUNK_HOME/etc**
- $SPLUNK_HOME/var
- $SPLUNK_HOME/conf 
- $SPLUNK_HOME/default 

### Question #:58 
Which of the following enables compression for universal forwarders in outputs. conf ? 
￼```
[tcpout]
defaultGroupt = my_indexers
compressed = true
```

### Question #:59 
Which of the following authentication types requires scripting in Splunk? 
- ADFS 
- LDAP 
- SAML 
- **RADIUS **

### Question #:60 
Where are license files stored?
- $SPLUNK_HOME/etc/secure
- $SPLUNK_HOME/etc/system
- **$SPLUNK_HOME/etc/licenses**
- $SPLUNK_HOME/etc/apps/licenses 

￼
 


