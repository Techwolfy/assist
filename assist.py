from contextlib import closing
import urllib
import html5lib
import urlparse

university = "UCI"

#document
with closing(urllib.urlopen("http://www.assist.org/web-assist/" + university + ".html")) as f:
	document = html5lib.parse(f, namespaceHTMLElements=False)

#schools
schools = []
for node in document.iter("select"):
	if(node.attrib["name"] == "oia"):
		for option in node.findall("option"):
			if(not option.attrib["value"].startswith("articulationAgreement")):
				continue
			schoolurl = urlparse.urlparse(option.attrib["value"])
			schools.append([urlparse.parse_qs(schoolurl.query)["oia"][0], int(urlparse.parse_qs(schoolurl.query)["dir"][0])])

#ay
for node in document.iter("select"):
	if(node.attrib["name"] == "ay"):
		ayurl = urlparse.urlparse(node.find("option").attrib["value"])
		ay = urlparse.parse_qs(ayurl.query)["ay"][0]

for school in schools:
	url = "http://web2.assist.org/cgi-bin/REPORT_2/Rep2.pl?agreement=aa&event=19&sidebar=false&rinst=left&mver=2&kind=4&dt=2&dir=" + str(school[1])
	if dir == 1:
		url += "&sia=" + university + "&ria=" + school[0]
	else:
		url += "&sia=" + school[0] + "&ria=" + university
	url += "&ia=" + university + "&oia=" + school[0]
	url += "&aay=" + ay + "&ay=" + ay
	print(school[0] + "...")
	urllib.urlretrieve(url, "report/" + school[0] + ".html")
