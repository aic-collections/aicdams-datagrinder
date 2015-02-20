import mimetypes

from abc import ABCMeta,abstractmethod

import cherrypy
import requests

from datagrinder.core.engine import Engine


class Asset(metaclass=ABCMeta):
    ''' Top-level abstract class that handles Assets. '''

    exposed = True

    add_mimetypes = (
        ('image/psd', '.psd'),
        ('image/x-psd', '.psd'),
        ('image/vnd.adobe.photoshop', '.psd'),
        # [...]
    )

    default_mimetype = 'application/octet-stream'

    presets = {}

    args = []

    async = False


    def __init__(self):
        for mt, ext in self.add_mimetypes:
            mimetypes.add_type(mt, ext)
        self.auth_str = cherrypy.request.headers['Authorization']\
            if 'Authorization' in cherrypy.request.headers\
            else None
        #cherrypy.log.error('Auth string: ' + self.auth_str)

        self._args = []


    @property
    def _selfdoc(self):
        return  {
            'methods' : {
                'POST' : {
                    'description' : 'Initiate a conversion process with a provided file. Process can be synchronous or asynchronous.',
                    'params' : [
                        {
                            'name' : 'src',
                            'datatype' : 'string',
                            'required' : False,
                            'description' : 'Source URL. Alternative to "data".'
                        },
                        {
                            'name' : 'data',
                            'datatype' : 'binary',
                            'required' : False,
                            'description' : 'Source file datastream. Alternative to "src".'
                        },
                        {
                            'name' : 'async',
                            'datatype' : 'boolean',
                            'required' : False,
                            'default' : 'false',
                            'description' : '''Whether the process happens asynchronously.

                            If set to "false", the webapp returns only after conversion has been completed. Recommended for small source files (<2Mb).

                            If "true", the application returns immediately after the source file has been received and validated.
                            Process completion is notified in the default JMS channel.
                            '''
                        },
                        {
                            'name' : '<action name>',
                            'datatype' : 'mixed',
                            'required' : False,
                            'description' : '''Parameter name should match one of the allowed actions (see \'allowed_actions\' list below).
                            Parameter value should be set accordingly (@TODO)'''
                        },
                        {
                            'allowed_actions' : self.allowed_actions,
                        },
                        {
                            'presets' : self.presets,
                        },
                    ],
                },
            },
        }


    @property
    def allowed_actions(self):
        '''Actions allowed for this resource.'''
        actions = set()
        for m in self.__dir__():
            if m[:8] == '_action_' and hasattr(eval('self.' + m), '__call__'):
                actions.add(m[8:])
        return list(actions)



    ## * * * HTTP METHODS * * *

    def OPTIONS(self):
        '''Self-documentation.

        Display methods grouped by HTTP verb, available actions and presets.
        '''
        return self._selfdoc


    @cherrypy.config(**{'tools.json_out.on': False})
    def POST(self, src=None, data=None, async=False, **actions):
        '''Process a file based on presets or a user-defined list of actions.'''

        cherrypy.log('\n')
        cherrypy.log('****************************')
        cherrypy.log('Starting conversion process.')
        cherrypy.log('****************************\n')

        self.async = async

        ## Check input data.
        ## No datastream provided.
        if data==None:
            ## No source URL provided.
            if src==None:
                raise cherrypy.HTTPError(
                    '400 Bad Request',
                    'No data or source URL provided. Please consult datagrinder API documentation.'
                )
            ## Source provided.
            else:
                ## Get data from remote URL.
                self._ds = requests.get(src)
                self._ds.raise_for_status()
        ## Datastream provided.
        else:
            ## Get data from datastream.
            self._ds = data.file

        dstream_info = self._validate_ds()

        ## If preset value is set, ignore all other operations.
        if 'preset' in actions.keys():
            preset = actions['preset']
            if preset in self.presets.keys():
                actions = self.presets[preset]
            else:
                raise cherrypy.HTTPError(
                    '400 Bad Request',
                    'Preset value "{}" is not valid. Check your request parameters.'.format(preset)
                )

        self._validate_actions(actions)
        self._apply_actions(actions)

        #cherrypy.log('Actions: {}'.format(actions))
        return self._process()




    ## * * * PRIVATE METHODS * * *

    @abstractmethod
    def _validate_ds(self):
        '''Validates a datastream.

        Override this method with a resource-specific one.
        '''
        pass


    @abstractmethod
    def _apply_actions(self, actions):
        ''' Loop over single actions and apply them according to a prefixed order. '''
        pass


    def _guess_file_ext(self, mimetype):
        return mimetypes.guess_extension(mimetype) or ''


    def _apply_preset(self, preset):
        '''Applies a preset in @sa presets and adds options to the GM command accordingly.'''
        ''' @TODO '''
        preset_actions = self.presets[preset]

        actions = []

        for action in preset_actions.keys():
            actions.append('{}={}'.format(action,preset_actions[action]))

        return actions


    def _validate_actions(self, actions):
        '''Validate actions.'''

        for action in actions.keys():
            if action not in self.allowed_actions:
                raise cherrypy.HTTPError(
                    '400 Bad Request',
                    'Action {} is not valid. Check your request parameters.'.format(action)
                )


    def _process(self):
        '''Sends command to subprocess.'''

        if self.async:
            out = Engine.fork_and_callback(self.args, self._ds)
        else:
            out = Engine.process_stream(self.args, self._ds)

        #cherrypy.tree.apps[''].config.update({'/' : {'tools.json_out.on': False}}) # Output binary
        cherrypy.response.status = 201
        cherrypy.response.headers['content-type'] = self.default_mimetype # @TODO

        return out

