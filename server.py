import cherrypy

from cherrypy.process.plugins import Daemonizer, PIDFile

from datagrinder.config import host, server, app
from datagrinder.config.host import host
from datagrinder.modules import still_image


## Main Web app class.
#
# Contains the RESTful API and all its top-level locations.
class Webapp():
    exposed = True

    routes = {
        'si' : still_image.StillImage
        #@TODO Add other resource prefixes.
    }

    def GET(self):
        return {'message': 'Nothing to see here.'}


if __name__ == '__main__':
    cherrypy.config.update(server.conf)

    Daemonizer(cherrypy.engine).subscribe()
    PIDFile(cherrypy.engine, host['pidfile']).subscribe()

    # Set routes as class members as expected by Cherrypy
    for r in Webapp.routes:
        setattr(Webapp, r, Webapp.routes[r]())

    webapp = Webapp()
    cherrypy.tree.mount(webapp, '/', app.rest_conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
