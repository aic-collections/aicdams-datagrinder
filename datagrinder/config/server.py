import cherrypy

from datagrinder.config import host

conf = {
	'global': {
		'log.access_file': '/var/log/datagrinder/access.log',
		'log.error_file': '/var/log/datagrinder/error.log',
		'server.max_request_body_size': host.max_req_size,
		'server.socket_host': host.listen_addr,
		'server.socket_port': host.listen_port,
	},
	'/': {
		'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
		#'request.methods_with_bodies': ('POST', 'PUT', 'PATCH'),
	}
}

