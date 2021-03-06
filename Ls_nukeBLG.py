# This is a Flame Pybox handler which applies a Baselight BLG grade
# It spawns a Nuke process which uses the Baselight Editions plugin
# 
# lewis@lewissaunders.com

import os, sys
nukebin = '/Applications/Nuke10.5v5/Nuke10.5v5.app/Contents/MacOS/Nuke10.5v5'
frontreadyfifo = '/tmp/Ls_nukeBLGfrontready'
framefile = '/tmp/Ls_nukeBLGframe'
resultreadyfifo = '/tmp/Ls_nukeBLGresultready'
blg = '/tmp/Ls_nukeBLG.blg.exr'

if('nuke' in sys.modules):
	# We're being run from the Nuke process - set up the tree
	r = nuke.createNode('Read', 'file /tmp/Ls_nukeBLGfront.exr', False)
	f = nuke.createNode('FrameRange', 'first_frame 1 last_frame 999999', False)
	b = nuke.createNode('Baselight', '', False)
	w = nuke.createNode('Write', 'file /tmp/Ls_nukeBLGresult.exr', False)
	while(True):
		# Block waiting for the fifo to be opened by Flame, render, then open the other fifo to signal back
		open(frontreadyfifo, 'r').close()
		ff = open(framefile, 'r')
		frame = int(ff.read())
		ff.close()
		r.knob('reload').execute()
		if(os.path.exists(blg)):
			b.knob('blg_file').setValue(blg)
		else:
			b.knob('blg_file').setValue('')
		b.knob('reload').execute()
		nuke.execute(w, frame, frame)
		print "Ls_nukeBLG: rendered frame %04d" % frame
		open(resultreadyfifo, 'w').close()

import pybox_v1 as pybox
class nukeBLG(pybox.BaseClass):
	def initialize(self):
		self.set_img_format('exr')
		self.set_in_socket(0, 'Front', '/tmp/Ls_nukeBLGfront.exr')
		self.remove_in_socket(2)
		self.set_out_socket(0, 'Result', '/tmp/Ls_nukeBLGresult.exr')
		self.remove_out_socket(1)
		self.add_global_elements(pybox.create_file_browser('Open BLG...', '/', 'exr', '/'))
		self.set_ui_pages(pybox.create_page('Ls_nukeBLG', 'Browser'))
		self.set_state_id('execute')

		# Create the two FIFOs anew.  We use these to coordinate the Flame and Nuke processes
		for f in (frontreadyfifo, resultreadyfifo):
			if os.path.exists(f):
				os.unlink(f)
			os.mkfifo(f)

		# Clean up from a possible previous instance
		os.system('pkill -f /tmp/Ls_nukeBLG.py')
		os.system('rm -f ' + blg)
		# Make a copy of the current file because Flame moves it
		os.system('cp -f ' + __file__ + ' /tmp/Ls_nukeBLG.py')
		# Start Nuke pointed to our copy of this file. Baselight requires USER and HOME to be set
		os.system('USER=t HOME=/tmp ' + nukebin + ' -it /tmp/Ls_nukeBLG.py &')

	def execute(self):
		for change in self.get_ui_changes():
			if(change['name'] == 'Open BLG...'):
				newblg = self.get_global_element_value('Open BLG...')
				# Link the chosen BLG file into /tmp for Nuke to pick up
				os.system('ln -sf "' + newblg + '" ' + blg)
				return
		# Write the frame number to disk so Nuke can pick it up
		frame = self.get_frame()
		f = open(framefile, 'w')
		f.write(str(frame))
		f.close()
		# Hit the fifo to wake our Nuke up, then wait for the signal that it's done
		open(frontreadyfifo, 'w').close()
		open(resultreadyfifo, 'r').close()

	def teardown(self):
		# Kill our Nuke process
		os.system('pkill -f /tmp/Ls_nukeBLG.py')

# From here we're run by Flame on each frame
p = nukeBLG(sys.argv[1])
p.dispatch()
p.write_to_disk(sys.argv[1])
