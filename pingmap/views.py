from django.shortcuts import render_to_response
#<coding:utf-8>
#!/usr/bin/env python
def index(req):
    return render_to_response('pingmap.html')

