import cherrypy
rest_conf = {
	'/': {
		'tools.json_out.on': False,
		'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
		'request.methods_with_bodies': ('POST', 'PUT', 'PATCH'),
	}
}

