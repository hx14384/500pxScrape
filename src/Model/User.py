
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

This file contains a model class for user.

Author: JeffXu
Last edited: Feb 2019
"""

class User(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, nickName, userId):
        self.nickName = nickName
        self.userId = userId

def make_User(nickName, userId):
    #print(nickName)
    #print(userId)
    user = User(nickName, userId)
    return user
