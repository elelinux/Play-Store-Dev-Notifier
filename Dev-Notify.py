#!/usr/bin/env python
#
# Written by lithid

import gtk
import pygtk
import urllib2
import re
import sys
import subprocess

SITE = "https://play.google.com"
	
main_label = gtk.Label()
scroll = gtk.ScrolledWindow()
frame = gtk.Frame()
table = gtk.Table(2, 1, False)
entryBox = gtk.Entry()

class test():

	def main(self):
		def update(self, DEV):
			try:
				devLink = DEV.split("+")
			except:
				devLink = DEV

			for i in table.get_children():
				print "Removing: %s" % i
				table.remove(i)

			number = -12
			count = 0

			while True:
				number+=12
				URL = "https://play.google.com/store/apps/developer?id=%s&start=%s&num=12" % (DEV, number)
				try:
					htmlpage = urllib2.urlopen(URL).read()
				except IOError:
					print "End of app parsing, exiting"
					break

				alllinks = re.findall('<a href=\".*?%s\">.*?%s</a>' % (devLink, devLink),htmlpage)
			
				chk = len(alllinks)
				if chk == 0:
					break

				for lines in alllinks:
					i = lines.split("\"")
					x = i[11]
					y = i[1]
					img = i[9]
					if x == "/" or "num-pagination" in x:
						pass
					else:
						count+=1
						event = gtk.EventBox()
						image = gtk.Image()
						frameNew = gtk.Frame()
						label = gtk.Label("%s" % x)
						label.show()
						tableNew = gtk.Table(2, 1, False)
						tableNew.show()
						tableNew.attach(event, 0, 1, 0, 1, xpadding=5, ypadding=5)
						tableNew.attach(label, 0, 1, 1, 2, xpadding=5, ypadding=5)
						frameNew.add(tableNew)
						frameNew.show()
						imgurl = urllib2.urlopen(img)
						loader = gtk.gdk.PixbufLoader()
						loader.write(imgurl.read())
						loader.close()
						image.set_from_pixbuf(loader.get_pixbuf())
						image.show()
						linkage = "%s%s" % (SITE, y)
						event.connect("button_press_event", open_url, linkage)
						event.add(image)
						event.show()
						table.attach(frameNew, 0, 1, count-1, count, xpadding=5, ypadding=5)

						if len(devLink) == 2:
							main_label.set_markup("Developer: <b>%s %s</b> Count: <b>%s</b>" % (devLink[0], devLink[1], count))
						elif len(devLink) == 1:
							main_label.set_markup("Developer: <b>%s</b> Count: <b>%s</b>" % (devLink[0], count))
						else:
							main_label.set_markup("Developer: <b>None</b> Count: <b>0</b>")

		def open_url(self, event, arg):
			subprocess.call(('xdg-open', arg))
			
		def run_entry(self):
			i = entryBox.get_text()
			update(self, i)

		dialog = gtk.Dialog("Play Store Dev Notifier", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_size_request(400, 400)
		dialog.set_resizable(False)

		main_label.show()
		main_label.set_markup("Developer: <b>None</b> Count: <b>0</b>")
		dialog.vbox.pack_start(main_label, True, True, 5)
		
		entryBox.show()
		entryBox.connect("activate", run_entry)
		dialog.vbox.pack_start(entryBox, True, True, 5)

		table.show()
		scroll.set_size_request(400, 300)
		scroll.add_with_viewport(table)
		scroll.show()
		frame.add(scroll)
		frame.show()
		dialog.vbox.pack_start(frame, True, True, 0)
					
		dialog.run()
		dialog.destroy()

if __name__ == "__main__":
	test().main()
