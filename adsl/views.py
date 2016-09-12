# <coding:utf-8>
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.generic import View
from . import models


class CADSLTraffic(View):
    def get(self, request, *args, **kwargs):
        object_result = models.notify.objects.all()
        return render(request, 'adsl/bar.html', {'notifications': object_result})


class CADSLQuery(View):
    def get(self, request, *args, **kwargs):
        if not request.method == 'GET':  # and request.is_ajax():
            return render_to_response()
        str_ip = request.GET.get('ip')
        str_interface = request.GET.get('interface')


class CADSLInput(View):
    def get(self, request, *args, **kwargs):
        if not request.method == 'GET':  # and request.is_ajax():
            return render_to_response()

        str_data = request.GET.get('data')
        dict_data = eval(str_data)
        str_msg = ''
        for str_ip, dict_interface in dict_data.iteritems():
            for str_interface, dict_info in dict_interface.iteritems():
                if 'up_total' in dict_info:
                    int_up_total = dict_info['up_total']
                else:
                    int_up_total = 0

                if 'down_total' in dict_info:
                    int_down_total = dict_info['down_total']
                else:
                    int_down_total = 0

                if 'equrrdment' in dict_info:
                    str_equrrdment = dict_info['equrrdment']
                else:
                    str_equrrdment = None

                if 'purpose' in dict_info:
                    str_purpose = dict_info['purpose']
                else:
                    str_purpose = None
                print str_ip, str_interface, int_up_total, int_down_total, str_equrrdment, str_purpose
                object_info = models.info(ip=str_ip, interface=str_interface, purpose=str_purpose,
                                          equrrdment=str_equrrdment, up_total=int_up_total,
                                          down_total=int_down_total)
                object_info.save()
                # str_msg += '{0} {1} {2} {3} {4} {5}\n'.format(str_ip, str_interface, int_up_total, int_down_total,
                #                                               str_equrrdment, str_purpose)
        return render_to_response()
