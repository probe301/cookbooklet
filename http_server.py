


"""
python2 命令行的简单 http 服务器
"""
# python -m SimpleHTTPServer


"""
python3 命令行的简单 http 服务器
"""
# python -m http.server




"""
python3 代码运行的简单 http 服务器
"""
import os
print(os.system('ipconfig'))

from http.server import HTTPServer, CGIHTTPRequestHandler
port = 8080
httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
print('Starting simple httpd on port:{}'.format(port))
httpd.serve_forever()



# 注意
# - Windows Server 需要调整 IE 默认安全级别, 或者换 Firefox 等
# - Linux 无图形界面时可以拿命令行传递文件, 如 wget 172.16.40.78:8000/file.txt save.txt
# - Linux 都自带 python, 临时传个文件这办法挺合适







"""
python 搭 FTP server
"""
# 需要 pip 安装 pyftpdlib 的库
# 然后 Windows 上找个想要分享的目录, 运行
# python -m pyftpdlib --port=2121 --write

# 然后 linux 里 wget curl 分别下载上传
# wget ftp://172.16.40.78:2121/windows_file.txt
# curl -T centos_file.txt ftp://172.16.40.78:2121







"""
flask simple demo
"""

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import Response
from flask import about

app = Flask(__name__)
@app.route('/')
@app.route('/index')
def index():
  user = {'nickname': 'myname'}
  return render_template("index.html",
                         title='Home',
                         user=user)

@app.route('/hello')
def hello():
  return 'Hello World'

@app.route('/task/<int:task_id>')
def get_task(task_id):
  ''' render json '''
  print('get /task/<task_id>' + str(task_id))
  return jsonify(from_db(task_id).to_dict())

@app.route('/topic/<int:topic_id>')
def list_by_topic(topic_id):
  ''' render html '''
  return render_template("topics.html", title='Topics', topic=from_db(topic_id))

@app.route('/rss')
def generate_feed():
  ''' render feed '''
  from feedgen.feed import FeedGenerator

  feed_name = 'feed_name'
  fg = FeedGenerator()
  fg.id('xxxurl/' + feed_name)
  fg.title(feed_name)
  fg.link(href='xxxurl/' + feed_name, rel='alternate')
  # fg.logo('http://ex.com/logo.jpg')
  fg.subtitle('by FeedGenerator')
  fg.link(href='xxxurl/' + feed_name + 'atom', rel='self')
  fg.language('zh-cn')

  for page in sorted(pages):
    fe = fg.add_entry()
    fe.id(page.metadata['url'])
    fe.title(page.metadata['title'])
    fe.link(href=page.metadata['url'])
    fe.description('\n\n' + page.to_html() + '\n')

  return fg.rss_str(pretty=True)
  # 或者
  if feed_path:
    return Response(open(feed_path, encoding='utf-8').read(), mimetype='application/xml')
  else:
    abort(404)
    # raise RuntimeError(f'cannot generate_feed {folder_name}')

# if __name__=="__main__":
#     app.run(debug=True, host='0.0.0.0', port=8080)






"""
带上传文件的 python http 服务, 运行这个脚本后, 
如果客户端有图形界面浏览器就能看到上传按钮, 
如果没图形界面, 可以用 wget curl 下载/上传

下载 wget 172.16.40.78:8000/windows_file.txt save_to_centos.txt
上传 curl -X POST http://172.16.40.78:8000 --form "file=@centos_file.txt"

https://gist.github.com/touilleMan/eb02ea40b93e52604938
"""

"""Simple HTTP Server With Upload.
This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.
see: https://gist.github.com/UniIsland/3346170
"""

__version__ = "0.1"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "bones7456"
__home_page__ = "http://li2z.cn/"

import os
import posixpath
import http.server
import urllib.request, urllib.parse, urllib.error
import cgi
import shutil
import mimetypes
import socket
import re
from io import BytesIO


class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET/HEAD/POST commands.
    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method. And can reveive file uploaded
    by client.
    The GET/HEAD/POST requests are identical except that the HEAD
    request omits the actual contents of the file.
    """

    server_version = "SimpleHTTPWithUpload/" + __version__

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        """Serve a POST request."""
        r, info = self.deal_post_data()
        print((r, info, "by: ", self.client_address))
        f = BytesIO()
        f.write(b'<!DOCTYPE html>')
        f.write(b"<html>\n<title>Upload Result Page</title>\n")
        f.write(b"<body>\n<h2>Upload Result Page</h2>\n")
        f.write(b"<hr>\n")
        if r:
            f.write(b"<strong>Success:</strong>")
        else:
            f.write(b"<strong>Failed:</strong>")
        f.write(info.encode())
        f.write(("<br><a href=\"%s\">back</a>" % self.headers['referer']).encode())
        f.write(b"<hr><small>Powerd By: bones7456, check new version at ")
        f.write(b"<a href=\"http://li2z.cn/?s=SimpleHTTPServerWithUpload\">")
        f.write(b"here</a>.</small></body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def deal_post_data(self):
        content_type = self.headers['content-type']
        if not content_type:
            return (False, "Content-Type header doesn't contain boundary")
        boundary = content_type.split("=")[1].encode()
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")

        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith(b'\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def send_head(self):
        """Common code for GET and HEAD commands.
        This sends the response code and MIME headers.
        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.
        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).
        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().
        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = BytesIO()
        displaypath = cgi.escape(urllib.parse.unquote(self.path))
        f.write(b'<!DOCTYPE html>')
        f.write(("<html>\n<title>Directory listing for %s</title>\n" % displaypath).encode())
        f.write(b'<meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
        f.write(("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath).encode())
        f.write(b"<hr>\n")
        f.write(b"<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write(b"<input name=\"file\" type=\"file\"/>")
        f.write(b"<input type=\"submit\" value=\"upload\"/></form>\n")
        f.write(b"<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write(('<li><a href="%s">%s</a>\n'
                    % (urllib.parse.quote(linkname), cgi.escape(displayname))).encode())
        f.write(b"</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.
        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)
        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = [_f for _f in words if _f]
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.
        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).
        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.
        """
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        """Guess the type of a file.
        Argument is a PATH (a filename).
        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.
        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.
        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })


def http_server_with_upload(HandlerClass=SimpleHTTPRequestHandler,
         ServerClass=http.server.HTTPServer):
    httpd = ServerClass(('', 8111), HandlerClass)
    sa = httpd.socket.getsockname()


    ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))

    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    print("Serving HTTP on http://{}:{}".format(ip, sa[1]))
    httpd.serve_forever()
    # http.server.test(HandlerClass, ServerClass)

if __name__ == '__main__':
    http_server_with_upload()


