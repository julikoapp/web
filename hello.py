def wsgi_application(environ, start_response):
	status = '200 OK'
	data = b"Hello, World!\n"
	headers = [
		('Content-Type', 'text/plain'),
		('Content-Length', str(len(data)))
	]
	start_response(status, headers)
	return "\n".join(environ.get('QUERY_STRING').split("&"))
