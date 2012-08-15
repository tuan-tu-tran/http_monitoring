#!/usr/bin/env python

import logging.config
logging.config.fileConfig("config_logging.ini")
logger=logging.getLogger("http_monitor")
try:
	import urllib2
	import ConfigParser
	config=ConfigParser.SafeConfigParser()
	config.read("config.ini")
	url=config.get("general","url")
	resp=urllib2.urlopen(url)
	page=resp.read()
	resp.close()
except:
	import traceback
	s=traceback.format_exc()
	logger.critical(s)

