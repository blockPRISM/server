from django.conf.urls import patterns
from django.conf.urls import url

from .views import (
    FacebookPublicKeyView,
    # GMailPublicKeyView,
)

urlpatterns = patterns('',
    url(r'^facebook/$', FacebookPublicKeyView.as_view(), name='facebook'),
    # url(r'^gmail/$', GMailPublicKeyView.as_view(), name='gmail')
)