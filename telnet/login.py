#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

from chaofeng import EndInterrupt,Timeout,asynchronous
from chaofeng.g import mark
from chaofeng.ui import VisableInput,Password,DatePicker
import chaofeng.ascii as ac
from libframe import BaseFrame, BaseAuthedFrame
from model import manager, RegistedError, LoginError
from datetime import datetime
import config
from collections import deque

@mark('welcome')
class WelcomeFrame(BaseFrame):

    def initialize(self):
        self.write(ac.clear)
        self.session.charset = 'gbk'
        print 'Connect :: %s : %s' % (self.session.ip, self.session.port)
        self.render('welcome')
        self.try_login_iter()

    def try_login_iter(self):
        passwd_reader = self.load(Password)
        with Timeout(config.data['MAX_TRY_LOGIN_TIME'] , EndInterrupt):
            while True :
                self.write(config.str['PROMPT_INPUT_USERID'])
                userid = self.readline()
                self.write('\r\n')
                if not userid:
                    continue
                if userid == 'new' :
                    self.goto('register')
                elif userid == 'guest':
                    self.write(config.str['PROMPT_GUEST_UNABLE_TO_USE'])
                    continue
                else:
                    passwd = passwd_reader.readln(prompt=config.str['PROMPT_INPUT_PASSWD'])
                print (userid, passwd)
                self.try_login(userid, passwd)

    @asynchronous
    def auth(self,userid,passwd):
        try:
            authobj = manager.auth.login(userid,passwd,self.session.ip)
        except LoginError as e:
            self.writeln(e.message)
            return False
        else:
            self.session.user = authobj
            self.session.stack = deque(maxlen=config.data['MAX_STACK_DEEP'])  #!!!!
            self.session.history = deque(maxlen=config.data['MAX_HISTORY_DEEP'])
            self.session.messages = [u'逸仙时空 argo.sysu.edu.cn']
            return authobj
                
    def try_login(self,userid,passwd):
        authobj = self.auth(userid,passwd)
        if authobj :
            self.goto('main')

@mark('register')
class RegisterFrame(BaseFrame):

    def initialize(self):
        self.render('register')
        passwd_reader = self.load(Password)
        with Timeout(config.data['MAX_TRY_REGISTER_TIME'] ,EndInterrupt) :
            while True :
                self.write(config.str["PROMPT_INPUT_USERID_REG"])
                userid = self.readline()
                if userid is False:
                    self.cancel()
                self.write('\r\n')
                if self.check_userid(userid) :
                    break
            while True :
                passwd = passwd_reader.readln(prompt=config.str['PROMPT_INPUT_PASSWD_REG'])
                if passwd is False:
                    self.cancel()
                if self.check_passwd(passwd) : 
                    self.register(userid,passwd)
        self.close()

    def check_userid(self,userid):
        try:
            manager.auth.check_userid(userid)
        except RegistedError as e:
            self.writeln(e.message)
            return False
        else:
            return True
    
    def check_passwd(self,passwd):
        if (not passwd) or (len(passwd) < 3):
            self.writeln(u'密码太短，请多于3个字符')
            return False
        return True
        
    def register(self,userid,passwd):
        manager.auth.register(userid,passwd,firsthost=self.session.ip)
        self.render('register_succ', userid=userid)
        self.pause()
        self.goto('welcome')
    
    def cancel(self):
        self.write(config.str["PROMPT_CANCEL"])
        self.pause()
        self.goto('welcome')

@mark('first_login')
class FirstLoginFrame(BaseAuthedFrame):

    def initialize(self):
        self.goto('help','index')
