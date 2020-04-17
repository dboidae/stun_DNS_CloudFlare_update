#!/usr/bin/python3
#
import os
import json
import logging
import sys
import socket
import CloudFlare
import random
import stun

def setup_logging(log_level):
    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)
    h = logging.StreamHandler(sys.stdout)
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s \n"
    h.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)
    if log_level.lower() == 'info'   : logger.setLevel(logging.INFO)
    if log_level.lower() == 'warning': logger.setLevel(logging.WARNING) 
    if log_level.lower() == 'error'  : logger.setLevel(logging.ERROR)
    return logger

def init_cfg():
    config = os.environ
    return(config)

def str2bool(v):
  return v.lower() in ("yes", "true", "1")

def check_stun(host_ip):
    return stun.get_ip_info(stun_host=host_ip)

def get_stun_ip(logger, config, destination_IP_list, source_server_list):
    for i in range(int(config['EXEC_stun_source_attempt'])):
        server = random.choice(source_server_list)
        logger.warning(server)
        IP_list = getIPx(server)
        if not set(IP_list)&set(destination_IP_list):
            for ip in IP_list:
                logger.info(ip)
                if not check_stun(ip)[1]:
                    logger.info('stun IP is not in ative state - lets skip it')
                else:
                    return ip
    return False

def cf_DNS_update(logger, config, cf, IP_list):
    cf_DNS_records = json.loads(json.dumps(cf.zones.dns_records.get(config['EXEC_CF_zone_ID'])))
    logger.info(cf_DNS_records)
    for DNS_record in cf_DNS_records:
        if DNS_record['name'] == config['EXEC_stun_destination']:
            logger.info(DNS_record['content'])
            if DNS_record['content'] in IP_list:
                logger.info('found')
                IP_list.remove(DNS_record['content'])
            else:
                DNS_record['content'] = IP_list[0]
                IP_list.remove(IP_list[0])
                logger.warning(DNS_record)
                if not str2bool(config['EXEC_CF_zone_update_dry_run']):
                    update_record = cf.zones.dns_records.put(config['EXEC_CF_zone_ID'], DNS_record['id'], data=DNS_record)
                    logger.warning(update_record)
                else:
                    logger.warning('dry run - nothing changed')
    return

def getIPx(d):
    try:
        data = socket.gethostbyname_ex(d)
        return data[2]
    except Exception:
        return False

def lambda_handler(event, context):
    config = init_cfg()
    logger = setup_logging(config['EXEC_log_level'])
    stun_source_list = config['EXEC_stun_source'].split(',')
    logger.info(stun_source_list)
    IP_list = getIPx(config['EXEC_stun_destination'])
    if not IP_list:
        logger.error('DNS dig error')
        return False
    logger.info(IP_list)
    if IP_list:
        i = 0
        for ip in IP_list:
            logger.warning(ip)
            if not check_stun(ip)[1]:
                logger.info('stun IP is not in ative state - lets remove it from DNS')
                new_IP = get_stun_ip(logger, config, IP_list, stun_source_list)
                logger.info(new_IP)
                if new_IP:
                    IP_list[i] = new_IP
            i = i + 1
    logger.warning(IP_list)
    cf=CloudFlare.CloudFlare(token=config['EXEC_CF_API_token'])
    cf_DNS_update(logger, config, cf, IP_list)
    return 
