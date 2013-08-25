from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound
import requests
import json

from .models import (
    PublicKey,
    Facebook,
    GMail
)


class FacebookPublicKeyView(View):
    facebook_url = 'https://graph.facebook.com/me/?oauth_token={}'

    def get(self, request):
        if 'facebook_id' in request.GET:
            facebook_id = request.GET['facebook_id']
            try:
                public_key_obj = Facebook.objects.get(facebook_id=facebook_id).public_key
                return HttpResponse(public_key_obj.public_key)
            except Facebook.DoesNotExist:
                return HttpResponseNotFound(u'Key not found')
        else:
            return HttpResponseServerError(u'Variable facebook_id not set.')

    def post(self, request):
        if not 'facebook_id' in request.POST:
            return HttpResponseServerError(u'Variable facebook_id not set.')
        if not 'public_key' in request.POST:
            return HttpResponseServerError(u'Variable public_key not set.')
        if not 'access_token' in request.POST:
            return HttpResponseServerError(u'Variable access_token not set.')
        facebook_id = request.POST['facebook_id']
        access_token = request.POST['access_token']
        public_key = request.POST['public_key']
        # check facebook authentication
        response = requests.get(self.facebook_url.format(access_token))
        if response.ok:
            facebook_user = json.loads(response.text)
            if facebook_user['username'] == facebook_id or facebook_user['id'] == facebook_id:
                try:
                    Facebook.objects.get(facebook_id=facebook_id)
                    return HttpResponseServerError(u'There is already a public key available for this facebook id.')
                except Facebook.DoesNotExist:
                    public_key_obj, _ = PublicKey.objects.get_or_create(public_key=public_key)
                    Facebook(facebook_id=facebook_id, public_key=public_key_obj).save()
                    return HttpResponse(public_key_obj.public_key)
            else:
                return HttpResponseServerError(u'User names do not match.')
        else:
            return HttpResponseServerError(u'Facebook authentication failed.')


class GMailPublicKeyView(View):
    def get(self, request):
        if 'gmail_hash' in request.GET:
            public_key_obj = get_object_or_404(GMail, gmail_hash=request.GET['gmail_hash']).public_key
            return HttpResponse(public_key_obj.public_key)
        else:
            return HttpResponseServerError(u'Variable gmail_hash not set.')

    def post(self, request):
        if not 'gmail_hash' in request.POST:
            return HttpResponseServerError(u'Variable gmail_hash not set.')
        if not 'public_key' in request.POST:
            return HttpResponseServerError(u'Variable public_key not set.')
        gmail_hash = request.POST['gmail_hash']
        public_key = request.POST['public_key']
        try:
            GMail.objects.get(gmail_hash=gmail_hash)
            return HttpResponseServerError(u'There is already a public key available for this gmail email.')
        except GMail.DoesNotExist:
            public_key_obj, _ = PublicKey.objects.get_or_create(public_key=public_key)
            GMail(gmail_hash=gmail_hash, public_key=public_key_obj).save()
            return HttpResponse(public_key_obj.public_key)