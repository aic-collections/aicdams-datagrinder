import cherrypy

from datagrinder.config.host import shell_bin, gmagick_bin, exiftool_bin
from datagrinder.config.presets import si_presets
from datagrinder.modules.asset import Asset


class StaticImage(Asset):
	'''Static Image class.

	This class runs and manages Image actions.
	'''

	exposed = True

	presets = si_presets

	default_mimetype = 'image/jpeg'

	base_args = [shell_bin, '-c']

	gmagick_cmd_head = gmagick_bin + ' convert'

	gmagick_args = ''

	gmagick_cmd_tail = '- -' # Pipe in and out

	exiftool_cmd_head = exiftool_bin

	exiftool_args = ''

	exiftool_cmd_tail = '-' # Pipe in


	def _action_format(self, fmt):
		'''Set output format.'''
		self.gmagick_args += ' -format ' + fmt


	def _action_resize(self, size):
		'''Resize (resample) image.'''
		self.gmagick_args += ' -resize ' + size


	def _action_crop(self, geom):
		'''Crop image.'''
		self.gmagick_args += ' -crop ' + geom


	def _action_color_space(self, model):
		'''Set image color space.'''
		self.gmagick_args += ' -colorspace ' + model


	def _action_color_profile(self, prof):
		'''Set image color profile.
		
		@TODO Not currently functioning. The profile will a name referencing an ICC file.
		'''
		self.gmagick_args += ' -profile ' + prof


	def _action_flatten(self, flatten):
		'''Flatten image layers.'''
		if flatten:
			self.gmagick_args += ' -flatten'


	def _action_quality(self, quality):
		'''Set image compression quality.'''
		self.gmagick_args += ' -quality ' + quality


	def _action_metadata(self, set):
		''' @TODO Use exiftool'''
		pass



	def _validate_ds(self):
		'''Validates that the datastream is not empty and is a valid image.
		
		@TODO Add image validation.
		'''
		
		if not self._ds:
			raise cherrypy.HTTPError(
				'400 Bad Request',
				'Provided datastream or link to resource contains no data.'
			)


	def _apply_actions(self, actions):
		''' Loop over single actions and apply them according to a prefixed order. '''

		self.gmagick_args, self.exiftool_args, gmagick_cmd, exiftool_cmd, args = '','','','',''

		# Gather arguments.
		for action in actions.keys():
			if not actions[action] == False:
				cherrypy.log('Setting option {} to {}.'.format(action, actions[action]))
				eval('self._action_{}(\'{}\')'.format(action, actions[action]))

		if self.gmagick_args:
			gmagick_cmd = '{} {} {}'.format(self.gmagick_cmd_head, self.gmagick_args, self.gmagick_cmd_tail)

		if self.exiftool_args:
			exiftool_cmd = '{} {} {}'.format(self.exiftool_cmd_head, self.exiftool_args, self.exiftool_cmd_tail)

		# Determine which tools to run.
		if gmagick_cmd:
			cmd = gmagick_cmd
			if exiftool_cmd:
				cmd += ' | ' + exiftool_cmd
		elif exiftool_cmd:
			cmd = exiftool_cmd
		else:
			raise cherrypy.HTTPError(
				'400 Bad Request',
				'No actions found.'
			)

		cherrypy.log('Assigning self.args.')
		self.args = self.base_args + [cmd]
		
		
