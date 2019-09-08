### Question #:1
What options are available when creating custom roles? (select all that apply)
- **Restrict search terms**
- Whitelist search terms
- **Limit the number of concurrent search jobs
- **Allow or restrict indexes that can be searched**

Question #:2 
Where should apps be located on the deployment server that the clients pull from? 
A. $SFLUNK_KOME/etc/apps
B. $SPLUNK_HCME/etc/sear:ch
C. $SPLUNK_HCME/etc/master-apps 
D. $SPLUNK HCME/etc/deployment-apps 

Question #:3 
In case of a conflict between a whitelist and a blacklist input setting, which one is used? 
A. Blacklist B. Whitelist C. They cancel each other out. 
D. Whichever is entered into the configuration first. 

Question #:4 
Which of the following are supported options when configuring optional network inputs? 
A. Metadata override, sender filtering options, network input queues (quantum queues) 
B. Metadata override, sender filtering options, network input queues (memory/persistent queues) 
C. Filename override, sender filtering options, network output queues (memory/persistent queues) 
D. Metadata override, receiver filtering options, network input queues (memory/persistent queues) 

How would you configure your distsearch conf to allow you to run the search below? 
sourcetype=access_combined status=200 action=purchase splunk_setver_group=HOUSTON 
A.
￼
B 
￼
C
￼
D
￼
 
Question #:6 
Which Splunk component consolidates the individual results and prepares reports in a distributed environment? 
A. Indexers B. Forwarder 
C. Search head 
D. Search peers 

Question #:7 
Where can scripts for scripted inputs reside on the host file system? (select all that apply) 
A. $SFLUNK_HOME/bin/scripts B. $SPLUNK_HOME/etc/apps/bin C. $SPLUNK_HOME/etc/system/bin 
D. $SPLUNK_HOME/etc/apps/<your_app>/bin_ 

Question #:8 
The universal forwarder has which capabilities when sending data? (select all that apply) 
A. Sending alerts B. Compressing data C. Obfuscating/hiding data 
D. Indexer acknowledgement 

Question #:9 
Which of the following are supported configuration methods to add inputs on a forwarder? (select all that apply) 
A. CLI B. Edit inputs . conf C. Edit forwarder.conf D. Forwarder Management 

Question #:10 
When configuring monitor inputs with whitelists or blacklists, what is the supported method of filtering the lists? 
A. Slash notation B. Regular expression C. Irregular expression D. Wildcard-only expression 

Question #:11 
Local user accounts created in Splunk store passwords in which file? 
A. $ SFLUNK_KOME/etc/passwd B. $ SFLUNK_KCME/etc/authentication C. $ S?LUNK_HCME/etc/users/passwd.conf 
D. $ SPLUNK HCME/etc/users/authentication.conf 

Question #:12 
Which forwarder type can parse data prior to forwarding? 
A. Universal forwarder B. Heaviest forwarder C. Hyper forwarder 
D. Heavy forwarder 

Question #:13 
Which of the following is valid distribute search group? 
A) 
￼
 B) 
￼
C)
￼
D)
￼
 
Question #:14 
For single line event sourcetypes. it is most efficient to set SHOULD_linemerge to what value? 
A. True 
B. False C. <regex string> D. Newline Character 

Question #:15 
When running the command shown below, what is the default path in which deployment server. conf is created? splunk set deploy-poll deployServer:port 
A. SFLUNK_HOME/etc/deployment B. SPLUNK_HOME/etc/system/local C. SPLUNK_HOME/etc/system/default 
D. SPLUNK_KOME/etc/apps/deployment 

Question #:16 
Which of the following indexes come pre-configured with Splunk Enterprise? (select all that apply) 
A. _license B. _lnternal C. _external 
D. _thefishbucket 


Question #:17 
Which Splunk indexer operating system platform is supported when sending logs from a Windows universal forwarder? 
A. Any OS platform B. Linux platform only C. Windows platform only. 
D. None of the above. 

Question #:18 
Which of the following statements describe deployment management? (select all that apply) 
A. Requires an Enterprise license 
B. Is responsible for sending apps to forwarders. C. Once used, is the only way to manage forwarders D. Can automatically restart the host OS running the forwarder. 

Question #:19 
How often does Splunk recheck the LDAP server? 
A. Every 5 minutes B. Each time a user logs in C. Each time Splunk is restarted 
D. Varies based on LDAP_refresh setting. 

Question #:20 
What is the correct order of steps in Duo Multifactor Authentication? 
A)
1 Request Login 2. Connect to SAML server 3 Duo MFA 4 Create User session 5 Authentication Granted  6. Log into Splunk  
B)
1. Request Login 2 Duo MFA 3. Authentication Granted  4 Connect to SAML server  5. Log into Splunk 6. Create User session 

C)
1 Request Login 
2 Check authentication / group mapping 
3 Authentication Granted 4. Duo MFA 5. Create User session 
6. Log into Splunk 

D. 
1 Request Login 
2 Duo MFA 3. Check authentication / group mapping 
4 Create User session 5. Authentication Granted 6 Log into Splunk 

Question #:21 
In which Splunk configuration is the SEDCMD used? 
A. props, conf B. inputs.conf C. indexes.conf 
D. transforms.conf 


Question #:22 
Which Splunk component performs indexing and responds to search requests from the search head? 
A. Forwarder B. Search peer C. License master 
D. Search head cluster 

Question #:23 
In which phase of the index time process does the license metering occur? 
A. input phase B. Parsing phase C. Indexing phase 
D. Licensing phase 

Question #:25 
Which setting in indexes. conf allows data retention to be controlled by time? 
A. maxDaysToKeep B. moveToFrozenAfter C. maxDataRetentionTime 
D. frozenTimePeriodlnSecs 

Question #:26 
Which optional configuration setting in inputs .conf allows you to selectively forward the data to specific indexer(s)? 
A. _TCP_ROUTING B. _INDEXER_LIST C. _INDEXER_GROUP 
D. _INDEXER ROUTING 

Question #:27 
Which valid bucket types are searchable? (select all that apply) 
A. Hot buckets B. Cold buckets C. Warm buckets 
D. Frozen buckets 

Question #:28 
In this source definition the MAX_TIMESTAMP_LOOKHEAD is missing. Which value would fit best? 
￼
￼
Event example: 

A. MAX_TIMESTAMP_L0CKAHEAD = 5 
B. MAX_TIMESTAMP_LOOKAHEAD - 10 
C. MAX_TIMESTAMF_LOOKHEAD = 20 
D. MAX TIMESTAMP LOOKAHEAD - 30 

Question #:29 
In which scenario would a Splunk Administrator want to enable data integrity check when creating an index? 
A. To ensure that hot buckets are still open for writes and have not been forced to roll to a cold state B. To ensure that configuration files have not been tampered with for auditing and/or legal purposes C. To ensure that user passwords have not been tampered with for auditing and/or legal purposes. 
D. To ensure that data has not been tampered with for auditing and/or legal purposes 

Question #:30 
To set up a Network input in Splunk, what needs to be specified'? 
A. File path. B. Username and password C. Network protocol and port number. 
D. Network protocol and MAC address. 

Question #:31 
What is required when adding a native user to Splunk? (select all that apply) 
A. Password B. Username C. Full Name 
D. Default app 


Question #:32 
Which Splunk component does a search head primarily communicate with? 
A. Indexer B. Forwarder C. Cluster master 
D. Deployment server 

Question #:33 
User role inheritance allows what to be inherited from the parent role? (select all that apply) 
A. Parents B. Capabilities C. Index access 
D. Search history 

Question #:34 
Which of the following apply to how distributed search works? (select all that apply) 
A. The search head dispatches searches to the peers B. The search peers pull the data from the forwarders. C. Peers run searches in parallel and return their portion of results. 
D. The search head consolidates the individual results and prepares reports 


Question #:35 
How do you remove missing forwarders from the Monitoring Console? 
A. By restarting Splunk. 
B. By rescanning active forwarders. C. By reloading the deployment server. D. By rebuilding the forwarder asset table. 

Question #:36 
What is the difference between the two wildcards ... and - for the monitor stanza in inputs,.conf? 
A. … is not supported in monitor stanzas 
B. There is no difference, they are interchangable and match anything beyond directory boundaries. 
C. * matches anything in that specific directory path segment, whereas ... recurses through subdirectories as well.  D. … matches anything in that specific directory path segment, whereas - recurses through subdirectories as well.  
Question #:37 
Which layers are involved in Splunk configuration file layering? (select all that apply) 
A. App context B. User context C. Global context 
D. Forwarder context 

Question #:38 
What is the default character encoding used by Splunk during the input phase? 
A. UTF-8  B. UTF-16  C. EBCDIC  D. ISO 8859 

Question #:39 
Which option accurately describes the purpose of the HTTP Event Collector (HEC)? 
A. A token-based HTTP input that is secure and scalable and that requires the use of forwarders 
B. A token-based HTTP input that is secure and scalable and that does not require the use of forwarders. 
C. An agent-based HTTP input that is secure and scalable and that does not require the use of forwarders. 
D. A token-based HTTP input that is insecure and non-scalable and that does not require the use of forwarders.  
Question #:40 
What are the minimum required settings when creating a network input in Splunk? 
A. Protocol, port number B. Protocol, port, location C. Protocol, username, port 
D. Protocol, IP. port number 

Question #:41 
Which of the following are methods for adding inputs in Splunk? (select all that apply) 
A. CLI 
B. Splunk Web C. Editing inputs. conf 
D. Editing monitor. conf 

Question #:42 
Which Splunk forwarder type allows parsing of data before forwarding to an indexer? 
A. Universal forwarder B. Parsing forwarder C. Heavy forwarder 
D. Advanced forwarder 

Question #:43 
Which of the following statements apply to directory inputs? {select all that apply) 
A. All discovered text files are consumed.  B. Compressed files are ignored by default  C. Splunk recursively traverses through the directory structure.  D. When adding new log files to a monitored directory, the forwarder must be restarted to take them into account.  
Question #:44 
You update a props. conf file while Splunk is running. You do not restart Splunk and you run this command: 
splunk btoo1 props list —debug
What will the output be? 
A. list of all the configurations on-disk that Splunk contains.  B. A verbose list of all configurations as they were when splunkd started.  C. A list of props. conf configurations as they are on-disk along with a file path from which the configuration is located  D. A list of the current running props, conf configurations along with a file path from which the configuration was made  

This file has been manually created on a universal forwarder 
￼
￼
A new Splunk admin comes in and connects the universal forwarders to a deployment server and deploys the same app with a new 
￼
 

Which file is now monitored? A. /var/log/messages B. /var/log/maillog C. /var/log/maillog and /var/log/messages 
D. none of the above 

Question #:46 
Within props. conf, which stanzas are valid for data modification? (select all that apply) 
A. Host 
B. Server C. Source D. Sourcetype 

Question #:47 
The priority of layered Splunk configuration files depends on the file's: 
A. Owner B. Weight C. Context 
D. Creation time 

Question #:48 
How does the Monitoring Console monitor forwarders? 
A. By pulling internal logs from forwarders. B. By using the forwarder monitoring add-on C. With internal logs forwarded by forwarders. 
D. With internal logs forwarded by deployment server. 

Question #:49 
What type of data is counted against the Enterprise license at a fixed 150 bytes per event? 
A. License data B. Metrics data C. Internal Splunk data 
D. Internal Windows logs 

Question #:50 
When deploying apps, which attribute in the forwarder management interface determines the apps that clients install? 
A. App Class 
B. Client Class 
C. Server Class 
D. Forwarder Class 

Question #:51 
Which of the following are required when defining an index in indexes. conf? (select all that apply) 
A. coldPath B. homePath C. frozenPath 
D. thawedPath 

Question #:52 
What are the required stanza attributes when configuring the transforms. conf to manipulate or remove events? 
A. REGEX, DEST. FORMAT B. REGEX. SRC_KEY, FORMAT C. REGEX, DEST_KEY, FORMAT 
D. REGEX, DEST_KEY FORMATTING 

Question #:53 
Which authentication methods are natively supported within Splunk Enterprise? (select all that apply) 
A. LDAP 
B. SAML C. RADIUS D. Duo Multifactor Authentication 


Question #:54 
During search time, which directory of configuration files has the highest precedence? 
A. $SFLUNK_KOME/etc/system/local B. $SPLUNK_KCME/etc/system/default C. $SPLUNK_HCME/etc/apps/app1/local 
D. $SPLUNK HCME/etc/users/admin/local 

Question #:55 
Which Splunk component distributes apps and certain other configuration updates to search head cluster members? 
A. Deployer B. Cluster master C. Deployment server D. Search head cluster master 

Question #:56 
Which Splunk component requires a Forwarder license? 
A. Search head B. Heavy forwarder C. Heaviest forwarder 
D. Universal forwarder 

Question #:57 
Which parent directory contains the configuration files in Splunk? 
A. SSFLUNK_KOME/etc B. SSPLUNK_HCME/var C. SSPLUNK_HOME/conf 
D. SSPLUNK_HOME/default 

 Question #:58 
Which of the following enables compression for universal forwarders in outputs. conf ? 
A) 
￼
B) 
￼
C) 
￼
 
D)
￼
 

Question #:59 
Which of the following authentication types requires scripting in Splunk? 
A. ADFS 
B. LDAP 
C. SAML 
D. RADIUS 

Question #:60 
Where are license files stored? A. $SPLUNK_HOME/etc/secure B. $SPLUNK_HOME/etc/system C. $SPLUNK_HOME/etc/licenses D. $SPLUNK_HOME/etc/apps/licenses 

￼
 


