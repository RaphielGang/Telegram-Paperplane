#Author=@blank_x
#!/usr/bin/python3
import sys, urbandict, urllib

if len(sys.argv) >= 2:
	if len(sys.argv) == 2:
		tud=sys.argv[1]
	else:
		ttud=' '.join(sys.argv)
		tttud=len(sys.argv[0]) + 1
		tud=ttud[tttud:]
else:
	tud=input('What to look up? ')
langi='en'
wasfine=True
httper=False
try:
	mean=urbandict.define(tud)
except urllib.error.HTTPError:
	wasfine=False
	httper=True
except:
	wasfine=False
if wasfine == True:
	print('Meaning of ' + tud + ':')
	print(mean[0]['def'])
	print('\nNow for some (probably useless) examples:')
	print(mean[0]['example'])
else:
	if httper == False:
		print('An error occured.')
		print('Now deal with this very informative error message.')
	else:
		print('I got an HTTP Error!')
		print(tud + ' probably doesn\'t even exist.')

