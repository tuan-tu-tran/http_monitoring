#!/usr/bin/env python

import logging.config
logging.config.fileConfig("config_logging.ini")

import logging
logger=logging.getLogger("http_monitor")

def configure_mail(config):
	handler=logging.handlers.SMTPHandler(
		config.get("mail","host"),
		config.get("mail","from"),
		config.get("mail","to"),
		config.get("mail","subject"),
	)
	logger.addHandler(handler)
	handler.setLevel(logging.WARN)

try:
	import ConfigParser
	config=ConfigParser.SafeConfigParser()
	config.read(["config.ini", "config_custom.ini"])
	configure_mail(config)

	url=config.get("general","url")
	with open(config.get("general","template")) as fh:
		template=fh.read()
	import urllib2
	import datetime
	resp=urllib2.urlopen(url)
	page=resp.read()
	resp.close()
	if page!=template:
		log=logger.warn
		ok="not ok"
		extra="\nexpected %i chars, got %i chars"%(
			len(template),
			len(page),
		)
	else:
		log=logger.info
		ok="ok"
		extra=""
	msg="content at %s is %s for url: %s%s"%(
		datetime.datetime.now(),
		ok,
		url,
		extra,
	)
	log(msg)
except:
	import traceback
	s=traceback.format_exc()
	logger.critical(s)

