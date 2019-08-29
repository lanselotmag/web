
def app(env,start_response):
	start_response('200 OK',[('Content-type','text/plain')])
	#body = ['\r\n'.join(env['QUERY_STRING'].split('&'))]
	body =  [bytes(i+'\n','ascii') for i in env['QUERY_STRING'].split('&')]
	return body
