import http.server, os, sys
os.chdir('/Users/saswata/Documents/GitHub/upcore-website')

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.split('?')[0].split('#')[0]
        if path == '/':
            return os.path.join(os.getcwd(), 'index.html')
        # cleanUrls: try path.html first
        candidate = os.path.join(os.getcwd(), path.lstrip('/'))
        if os.path.isfile(candidate):
            return candidate
        if os.path.isfile(candidate + '.html'):
            return candidate + '.html'
        return candidate
    def log_message(self, fmt, *args):
        print(fmt % args)

port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
with http.server.HTTPServer(('', port), Handler) as s:
    s.serve_forever()
