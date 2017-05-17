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

def main():
	import ConfigParser
	config=ConfigParser.SafeConfigParser()
	config.read(["config.ini", "config_custom.ini"])
	configure_mail(config)

	url=config.get("general","url")
	template = config.get("general","template")
	process(url, template)

def process(url, templateFile):
	import os
	if os.path.exists(templateFile):
		with open(templateFile) as fh:
			template=fh.read()
	else:
		template=None
	import urllib2
	import datetime
	resp=urllib2.urlopen(url)
	page=resp.read()
	resp.close()
	if template==None:
		with open(templateFile,"w") as fh:
			fh.write(page)
			logger.info("wrote content of %s to %s", url, templateFile)
		return
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

try:
	main()
except:
	import traceback
	s=traceback.format_exc()
	logger.critical(s)

