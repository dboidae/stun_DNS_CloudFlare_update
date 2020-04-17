Stun DNS update script
=======
(lamdba function)/(stand alone script) for updateting CloudFlare DNS records for stun service 
it seems more prototype then real solution, anyway you may try use it for own risk. I wouldn't recommend run it (by cron) more often than "2 * your_DNS_record_TTL".

Local Installation
-
* Clone the git repo
* `npm install -g serverless`  (see details here http://serverless.com) - optional, for use inside AWS cloud 
* `pip install -r requirements.txt --target=./`
* copy environment.yml.example to environment.yml - optional
* copy environment.sh.example  to environment.sh

Deployment/update to AWS CloudeFormation - optional
-
* check and edit environment.yml file
* check and edit AWS_account settings (leave blank the VPC and subnet ID) in deploy.sh file - optional

Deployment to AWS - optional
-
* check and edit environment.yml file
* check and edit AWS_account, AWS_region, VPC, subnet settings in deploy.sh file
* run ./deploy.sh

Run localy
-
* check and edit environment.sh file
* run ./start.sh

Run Lambda - optional
-
* check and edit environment variables in AWS Lambda home screen
* create any 'test' event
* press 'test'


Overview (Lambda)/(script) function
-
* 1. Resolve 'stun destination' DNS record
* 2. Check IPs by stun agent
* 3. In case the IP for stun is out of service - select new IP from stun servers list, check it out and update the DNS record in CFlare

Operations and Testing Notes
-

Configuration file environment.yml (environment.sh for local run)
-
* Environment variables:

- EXEC_environment=local - auto settings for serveerless
- EXEC_log_level=info,warning or error
- EXEC_stun_destination=stun._my_.com - DNS name to check and update
- EXEC_stun_source=stun.counterpath.com,stun.zoiper.com,stun.pjsip.org,stun.stunprotocol.org,stun.t-online.de,stun.acrobits.cz,stun.twt.it,stun.webcalldirect.com,stun.1und1.de,stun.barracuda.com - list of free source stun service DNS names
- EXEC_stun_source_attempt=5 - attemps to chose random IP from source list ( IP must not exist in active destination DNS A records and be in service)
- EXEC_CF_API_token=my_API_token
- EXEC_CF_zone_ID=my_zone_id
- EXEC_CF_zone_update_dry_run=yes - dry run for DNS update by CFlare API 
