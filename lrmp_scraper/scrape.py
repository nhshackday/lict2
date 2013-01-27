#!/usr/bin/env python
# coding=utf8
import Queue
import os
import sys
import requests
import re
import datetime
import time
import pprint
import multiprocessing

proxies = { "http": "http://localhost:8888/" }
proxies = None

#  Parameters:	
#  method – method for the new Request object.
#  url – URL for the new Request object.
#  params – (optional) Dictionary or bytes to be sent in the query string for the Request.
#  data – (optional) Dictionary, bytes, or file-like object to send in the body of the Request.
#  headers – (optional) Dictionary of HTTP Headers to send with the Request.
#  cookies – (optional) Dict or CookieJar object to send with the Request.
#  files – (optional) Dictionary of ‘name’: file-like-objects (or {‘name’: (‘filename’, fileobj)}) for multipart encoding upload.
#  auth – (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
#  timeout – (optional) Float describing the timeout of the request.
#  allow_redirects – (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.
#  proxies – (optional) Dictionary mapping protocol to the URL of the proxy.
#  verify – (optional) if True, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
#  stream – (optional) if False, the response content will be immediately downloaded.
#  cert – (optional) if String, path to ssl client cert file (.pem). If Tuple, (‘cert’, ‘key’) pair.

def chunks(l, n):
	""" Yield successive n-sized chunks from l.
	"""
	for i in xrange(0, len(l), n):
		yield l[i:i+n]

def fail(msg, resp):
	print "%s :("
	pprint.pprint(resp.status_code)
	pprint.pprint(resp.headers)
	pprint.pprint(resp.text)
	sys.exit(1)

def gents():
	dt = datetime.datetime.now()
	return "%i" % (time.mktime(dt.timetuple()))

def gents_milli():
	dt = datetime.datetime.now()
	return "%i" % (time.mktime(dt.timetuple()) * 1000 + (dt.microsecond / 1000))

def gen_request_params(session=None, swec=2, ids=[]):
	return {
		"s_1_1_2_0":        str(ids[0]) if len(ids)>0 else "",
		"s_1_1_4_0":        str(ids[1]) if len(ids)>1 else "",
		"s_1_1_5_0":        str(ids[2]) if len(ids)>2 else "",
		"s_1_1_6_0":        str(ids[3]) if len(ids)>3 else "",
		"s_1_1_7_0":        str(ids[4]) if len(ids)>4 else "",
		"s_1_1_8_0":        str(ids[5]) if len(ids)>5 else "",
		"s_1_1_9_0":        str(ids[6]) if len(ids)>6 else "",
		"s_1_1_10_0":       str(ids[7]) if len(ids)>7 else "",
		"s_1_1_11_0":       str(ids[8]) if len(ids)>8 else "",
		"s_1_1_3_0":        str(ids[9]) if len(ids)>9 else "",
		"SWEFo":            "SWEForm1_0",
		"SWEField":         "s_1_1_20_0",
		"SWENeedContext":   "true",
		"SWENoHttpRedir":   "true",
		"W":                "t",
		"SWECmd":           "InvokeMethod",
		"SWEMethod":        "NewQuerySearch",
		"SWERowIds":        "",
		"SWESP":            "false",
		"SWEVI":            "",
		"SWESPNR":          "",
		"SWEPOC":           "",
		"SWESPNH":          "",
		"SWEH":             "",
		"SWETargetView":    "",
		"SWEDIC":           "false",
		"_sn":              session,
		"SWEReqRowId":      "0",
		"SWEView":          "GMC WEB Doctor Multiple Search",
		"SWEC":             2,
		"SWERowId":         "VRId-0",
		"SWETVI":           "",
		"SWEW":             "",
		"SWEBID":           str(swec),
		"SWEM":             "",
		"SRN":              "",
		"SWESPa":           "",
		"SWETS":            gents_milli(),
		"SWEContainer":     "",
		"SWEWN":            "",
		"SWEKeepContext":   "0",
		"SWEApplet":        "GMC WEB Health Provider Multiple Search Applet",
		"SWETA":            "",
	}


def scrape(queue):
	try:
		chunk = queue.get_nowait()
	except Queue.Empty, e:
		return

	# login #1
	resp = requests.request(
			method="GET",
			url="http://webcache.gmc-uk.org/gmclrmp_enu/start.swe?SWECmd=GotoView&SWEView=GMC+WEB+Doctor+Search&SWEApplet=GMC+WEB+Health+Provider+Search+Applet",
			headers = {
				"Referer": "http://www.gmc-uk.org/doctors/register/LRMP.asp",
			},
			proxies = proxies
			)
	if resp.status_code != 200:
		fail("Getting session failed", resp)
	sn = re.search('<input type = "hidden" name="_sn" value="([^"]*)">', resp.text)
	if not sn:
		fail("Could not find session number", resp)
	session = sn.group(1)
	print "Got session: %s" % session

	# login #2
	params = {
		"SWECmd": "GotoView",
		"_sn": session,
		"SWEView": "GMC+WEB+Doctor+Search",
		"SRN": "",
		"SWEHo": "webcache.gmc-uk.org",
		"SWETS": gents(),
		"SWEApplet": "GMC WEB Health Provider Search Applet",
	}
	resp = requests.request(
			method="GET",
			params=params,
			url="http://webcache.gmc-uk.org/gmclrmp_enu/start.swe",
			proxies=proxies,
			)
	if resp.status_code != 200:
		fail("Request for SWEBID failed", resp)
	m = re.search("<script language=\"javascript\">navigator.id = \"([0-9]*)\";</script>", resp.text)
	if not m:
		fail("Could not find SWEBID", resp)
	swebid = m.group(1)
	print "Got SWEBID: %s" % swebid

	# dummy request because... just because
	swec = 1
	resp = requests.request(
			method="POST",
			url="http://webcache.gmc-uk.org/gmclrmp_enu/start.swe",
			proxies = proxies,
			data = gen_request_params(swec=swec, session=session),
			)

	while True:
		fn_num = "%06i" % chunk
		fn_nums = list(chunks(fn_num,2))
		fn_nums[-1] += ".html"
		fn = os.path.join("data", *fn_nums)
		if os.path.exists(fn):
			print "skipping for ids %06ix" % (chunk)
		else:
			if not os.path.exists(os.path.dirname(fn)):
				os.makedirs(os.path.dirname(fn))

			swec = swec + 1
			print "sending request for ids %06ix" % (chunk)
			id_chunk = range(chunk * 10, (chunk+1)*10)
			id_strs = ["%07i" % i for i in id_chunk]
			resp = requests.request(
					method="POST",
					url="http://webcache.gmc-uk.org/gmclrmp_enu/start.swe",
					proxies = proxies,
					data = gen_request_params(swec=swec, session=session, ids=id_strs),
					)

			f = open(fn, "w")
			f.write(resp.text.encode('utf-8'))
			f.close()
		try:
			chunk = queue.get_nowait()
		except Queue.Empty, e:
			return


if len(sys.argv) == 3:
	if sys.argv[1] == "launch":
		prefix=int(sys.argv[2])

		if prefix > 9:
			print "Prefix too big"
			sys.exit(1)

		q = multiprocessing.Queue()
		for chunk in range(prefix*100000, (prefix+1)*100000):
			q.put(chunk)

		pool = multiprocessing.Pool(1000, scrape, [q])
		pool.close()
		pool.join()

	else:
		start = int(sys.argv[1])
		end = int(sys.argv[2])
		q = multiprocessing.Queue()
		for chunk in range(start, end):
			q.put(chunk)

		pool = multiprocessing.Pool(10, scrape, [q])
		pool.close()
		pool.join()



