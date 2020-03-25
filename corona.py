import requests, sys, re, time, os
from optparse import OptionParser

def banner(help=False, about=False):
        os.system("clear")
        print ("""
 _   __                    _   _____
| | / /                   | | /  __ \  
| |/ /  __ ___      ____ _| | | /  \/ ___  _ __ ___  _ __   __ _
|    \ / _` \ \ /\ / / _` | | | |    / _ \| '__/ _ \| '_ \ / _` |
| |\  \ (_| |\ V  V / (_| | | | \__/\ (_) | | | (_) | | | | (_| |
\_| \_/\__,_| \_/\_/ \__,_|_|  \____/\___/|_|  \___/|_| |_|\__,_|
   AUTHOR: BILLAL FAUZAN      VERSION: 0.2     COVID-19 INFO
""")
        if help == True:
                print ("""
Command:
   ./corona.py {option}
   ./corona.py {country}

Options:
   -s, --save    = save result to file
   -h, --help    = Help
   -a, --about   = About
   -c, --country = show all country list
   -p, --provinsi= show all provinsi (indonesia only)

Country:
   Support All Country

Provinsi:
   ./corona.py -p all        = get all provinsi
   ./corona.py -p {provinsi} = get provinsi with name
""")
        if about == True:
                print ("""
Auhor      : Billal Fauzan
Version    : 0.2
Name       : Corona Virus Info (Covid-19 Info)
Thanks     : Allah Swt, and all my friends
From       : api.kawalcorona.com
Description: show information corona on all country
License    : MIT
""")

def get_information(country, save=False, path=None):
	print ("[!] Requests Get To URL", end="", flush=True)
	try:
		r = requests.get("https://api.kawalcorona.com").text
		print (" -> Success", end="", flush=True)
		print ("\n[!] Getting Information", end="", flush=True)
		get_country = re.findall('"Country_Region":"(.*?)"', r)
		data = '{"OBJECTID":(.*?),"Country_Region":"%s","Last_Update":(.*?),"Lat":(.*?),"Long_":(.*?),"Confirmed":(.*?),"Deaths":(.*?),"Recovered":(.*?),"Active":(.*?)}}'%(country)
		cari = re.search(data, r)
		print (" -> Success")
#	print (cari.group())
		last = str(cari.group(2))
		print ("[*] Country: "+country)
		print ("[*] Last Update: "+last)
		print ("[*] Confirmed: "+str(cari.group(5)))
		print ("[*] Death: "+str(cari.group(6)))
		print ("[*] Recovered: "+str(cari.group(7)))
		print ("[*] Active: "+str(cari.group(8)))
	except requests.exceptions.ConnectionError:
		print (" -> Failed", end="", flush=True)
		print ("\n[!] No Connected\n")

def provinsi(perintah):
	data = []
	provData = []
	banner()
	print ("[!] Requests Get To URL", end="", flush=True)
	try:
		req=requests.get('https://api.kawalcorona.com/indonesia/provinsi').json()
		print (" -> Success", end="", flush=True)
		print ("\n[!] Gettings Information", end="", flush=True)
		for x in req:
			data.append(x['attributes'])
		print (" -> Success\n", end="", flush=True)
		for a in data:
			prov = a["Provinsi"]
			if perintah == "all":
				print ("[*] Provinsi: "+prov)
				print ("[*] Confirmed: "+str(a['Kasus_Posi']))
				print ("[*] Recovered: "+str(a['Kasus_Semb']))
				print ("[*] Death: "+str(a['Kasus_Meni']))
			elif perintah.lower() in prov.lower():
				print ("[*] Provinsi: "+prov)
				print ("[*] Confirmed: "+str(a['Kasus_Posi']))
				print ("[*] Recovered: "+str(a["Kasus_Semb"]))
				print ("[*] Death: "+str(a['Kasus_Meni']))
	except requests.exceptions.ConnectionError:
		print (" -> Failed", end="", flush=True)
		print ("\n[!] No Connected\n")

def show_list():
	banner()
	try:
		o = open("list.txt", "r").read()
		for a in o.splitlines():
			print ("[*] "+str(a))
	except IOError:
		print ("[!] Requests Get To URL", end="", flush=True)
		r = requests.get("https://api.kawalcorona.com").text
		print (" -> Success", end="", flush=True)
		print ("\n[!] Getting Country\n", end="", flush=True)
		country = re.findall('"Country_Region":"(.*?)"', r)
		for coun in country:
			print ("[*] "+str(coun), end="", flush=True)
			buka = open("list.txt", "a")
			buka.write(coun+"\n")
			buka.close()
			print (" -> Success\n", end="", flush=True)

def main():
	save = None
	country = None
	parse = OptionParser(add_help_option=False, epilog="Corona Virus Information")
	parse.add_option("-s", "--save", help="Save Result", dest="save", action="store_false")
	parse.add_option("-h", "--help", help="Show All Commands", dest="help", action="store_true")
	parse.add_option("-a", "--about", help="About", dest="about", action="store_true")
	parse.add_option("-c", "--country", help="Show All Country", dest="country", action="store_true")
	parse.add_option("-p", "--provinsi", help="Show All Provinsi Indonesia (Indonesia Only)", dest="prov", action="store_true")
	opt, args = parse.parse_args()
	if opt.help == True:
		banner(help=True);sys.exit()
	elif opt.about == True:
		banner(about=True);sys.exit()
	elif opt.country == True:
		show_list()
	elif opt.prov == True:
		perintah = args[0]
		provinsi(perintah)
	elif opt.save == True:
		try:
			save = args[0]
		except IndexError:
			banner(about=False);sys.exit()
	else:
		try:
			country = sys.argv[1]
		except IndexError:
			banner(help=True);sys.exit()
	if country:
		banner()
		try:
			o = open("list.txt", "r").read()
			for a in o.splitlines():
				if country.lower() in a.lower():
					if save:
						get_information(a, save=True, path=save)
					else:
						get_information(a)
					break
#				else:
#					print ("[#] Country '%s' Not Found, Please Use -c to show all country list"%(country));break
		except IOError:
			print ("[#] File List Country Not Found, please configure")
			sys.exit()
main()
