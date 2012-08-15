#!/usr/bin/env python

import logging.config
logging.config.fileConfig("config_logging.ini")

import logging
logger=logging.getLogger("http_monitor")
try:
	import urllib2
	import ConfigParser
	config=ConfigParser.SafeConfigParser()
	config.read(["config.ini", "config_custom.ini"])
	url=config.get("general","url")
	with open(config.get("general","template")) as fh:
		template=fh.read()
	resp=urllib2.urlopen(url)
	page=resp.read()
	resp.close()
	if page!=template:
		logger.warn("content is not ok")
	else:
		logger.info("content is ok")
except:
	import traceback
	s=traceback.format_exc()
	logger.critical(s)

