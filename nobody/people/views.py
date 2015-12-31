# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404

from nobody.libs.mc import cache
from nobody.libs.logger import send_log
from magnet.tasks import test_task
# from analysis.alg.kmeans import k_means
# from analysis.draw import plot_2d

from models import DoubanPeople, DoubanGroup

_MC_KEY_VIEW_PEOPLE = "/people/get_people/%s/:view"


def get_peoples(request):
    peoples = DoubanPeople.get_all()
    output = '<br />'.join([people.name for people in peoples])
    output += '<br /> %s' % len(peoples)
    # TODO 这里是不是使用序列化， 就不用这么麻烦的转，就是model对象->字符串转换.
    return HttpResponse(output)


# @cache(_MC_KEY_VIEW_PEOPLE % "{pk}")
def get_people(request, pk):
    people = DoubanPeople.get(pk=pk)

    if people:
        return HttpResponse(people.name)
    else:
        raise Http404("Not Found it.")


# def analysis_people_by_kmeans(request):
#     peoples = DoubanPeople.filter(id__lt=10000)
#
#     data = [[people.id, len(people.name), len(people.location)] for people in peoples]
#
#     train_data = [_[1:] for _ in data]
#
#     labels, predict_func = k_means(train_data, 6)
#
#     _buffer = plot_2d(predict_func, train_data, labels, 'k-means', ['name_length', 'location_length'])
#
#     return HttpResponse(_buffer.getvalue(), mimetype='image/png')
