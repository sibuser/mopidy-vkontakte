# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

import os
import json
import time
import shelve
import urllib
import urllib2
import cookielib

from urllib import urlencode
from urlparse import urlparse
from HTMLParser import HTMLParser

logger = logging.getLogger(__name__)


class FormParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = 'GET'

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == 'form':
            if self.form_parsed:
                raise RuntimeError('Second form on page')
            if self.in_form:
                raise RuntimeError('Already in form')
            self.in_form = True
        if not self.in_form:
            return
        attrs = dict((name.lower(), value) for name, value in attrs)
        if tag == 'form':
            self.url = attrs['action']
            if 'method' in attrs:
                self.method = attrs['method'].upper()
        elif tag == 'input' and 'type' in attrs and 'name' in attrs:
            if attrs['type'] in ['hidden', 'text', 'password']:
                self.params[attrs['name']] = attrs['value'] if 'value' \
                    in attrs else ''

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == 'form':
            if not self.in_form:
                raise RuntimeError('Unexpected end of <form>')
            self.in_form = False
            self.form_parsed = True


class VKSession(object):
    def __init__(self, config=None):
        super(VKSession, self).__init__()

        self.config = config

        self.email = self.config['vkontakte']['email']
        self.password = self.config['vkontakte']['password']
        self.client_id = self.config['vkontakte']['client_id']
        self.user_id, self.token, self.expires_in = self.load_session()

        self.playlist = None

        if self.expires_in == 0:
            self.login()
        logger.info('Mopidy uses Vkontakte Music')

    # Authorization form
    def login(self):
        logger.info('Login as %s', self.email)

        opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
            urllib2.HTTPRedirectHandler())

        opener_url = (
            'http://oauth.vk.com/oauth/authorize?' +
            'redirect_uri=http://oauth.vk.com/blank.html' +
            '&response_type=token&scope=audio&display=wap' +
            '&client_id={0}'.format(self.client_id)).encode('utf-8')

        response = opener.open(opener_url)
        doc = response.read()
        parser = FormParser()
        parser.feed(doc)
        parser.close()
        parser.params['email'] = self.email
        parser.params['pass'] = self.password
        response = opener.open(parser.url, urllib.urlencode(parser.params))
        doc, url = response.read(), response.geturl()

        if urlparse(url).path != '/blank.html':
            url = self.give_access(doc, opener)
        pairs = urlparse(url).fragment.split('&')
        answer = dict(self.split_key_value(kv_pair) for kv_pair in pairs)
        self.token, self.user_id, self.expires_in = answer['access_token'], \
            answer['user_id'], answer['expires_in']
        self.save_session()

    def split_key_value(self, kv_pair):
        kv = kv_pair.split('=')
        return kv[0], kv[1]

    def call_api(self, method, param=None):
        params = []
        if param:
            params.extend(param)
        params.append(('uid', self.user_id))
        params.append(('access_token', self.token))

        url = 'https://api.vk.com/method/%s?%s' % (method, urlencode(params))
        response = json.loads(urllib2.urlopen(url).read())
        try:
            return response['response']
        except KeyError:
            error_code = response['error']['error_code']
            if error_code == 5:
                logger.error(response['error']['error_msg'])
                self.login()
            else:
                logger.error(response['error']['error_msg'])
            return []

    # Permission request form
    def give_access(self, doc, opener):
        parser = FormParser()
        parser.feed(doc)
        parser.close()

        response = opener.open(parser.url, urllib.urlencode(parser.params))
        return response.geturl()

    def config_dir_check(self):
        self.config_dir_path = os.environ['HOME'] + '/.config/mopidy'
        if os.access(self.config_dir_path, os.F_OK):
            return True
        else:
            os.mkdir(self.config_dir_path)
            return False

    def config_file_check(self, config_file_path, mode):
        if not self.config_dir_check():
            return False
        if os.access(config_file_path, mode):
            return True
        else:
            return False

    def check_session(self, expires_in):
        if expires_in == 0 or expires_in - time.time() < 0:
                return 0
        else:
            return expires_in

    def load_session(self):
        sessionPath = os.environ['HOME'] + '/.config/mopidy/vkontakte.db'
        if self.config_file_check(sessionPath, os.R_OK):
            s = shelve.open(sessionPath, 'r')
            token = s.get('token'.encode('utf-8'), None)
            user_id = s.get('user_id'.encode('utf-8'), None)
            expires_in = s.get('expires_in'.encode('utf-8'), 0)
            s.close()
            return user_id, token, expires_in
        else:
            return None, None, 0

    def save_session(self):
        self.config_dir_check()
        sessionPath = os.environ['HOME'] + '/.config/mopidy/vkontakte.db'
        s = shelve.open(sessionPath, 'c')
        s['token'.encode('utf-8')] = self.token.encode('utf-8')
        s['user_id'.encode('utf-8')] = self.user_id.encode('utf-8')
        s['expires_in'.encode('utf-8')] = int(self.expires_in) + time.time()

        s.close()
