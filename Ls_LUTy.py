import os, sys, base64, zipfile
import pybox_v1 as pybox

class Ls_LUTy(pybox.BaseClass):
	def initialize(self):
		self.set_img_format('exr')
		self.set_in_socket(0, 'Front', '/tmp/Ls_LUTyfront.exr')
		self.set_in_socket(1, 'Normal', '/tmp/Ls_LUTytarget.exr')
		self.remove_in_socket(1)
		self.set_out_socket(0, 'Result', '/tmp/Ls_LUTyresult.exr')
		self.remove_out_socket(1)
		self.add_global_elements(pybox.create_popup('Mode', ['Match Macbeth target image', 'Match synthetic Macbeth values'], row=1, col=0))
		self.add_global_elements(pybox.create_toggle_button('Analyze', False, False, row=1, col=1))
		self.add_global_elements(pybox.create_file_browser('Save in folder...', '/opt/Autodesk/project', 'ctf', '/opt/Autodesk/project', row=1, col=3))
		self.add_global_elements(pybox.create_popup('Save format', ['CTF', 'Matchbox ColourMatrix', 'Nuke ColorMatrix', 'All available formats'], row=0, col=3))
		self.set_ui_pages(pybox.create_page('Setup'))
		self.set_state_id('execute')

		print("\n\ninit")

	def execute(self):
		print("exec")
		for change in self.get_ui_changes():
			if(change['name'] == 'Analyze'):
				print self.get_global_element_value('Analyze')


# Decode, write, unzip and import our supporting libraries, since there is no way to package extra files with a Pybox without hardcoding their paths
libfolder = '/tmp/Ls_LUTylibs'
libzip = libfolder + '.zip'
f = open(libzip, 'w')
f.close()
z = zipfile.ZipFile(libzip)
if(not os.path.exists(libfolder)):
	os.makedirs(libfolder)
z.extractall(libfolder)
z.close()
os.unlink(libzip)
sys.path.append(libfolder)
sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python')
import OpenEXR, numpy

p = Ls_LUTy(sys.argv[1])
p.dispatch()
p.write_to_disk(sys.argv[1])