# coding: utf-8
'''

Gracenoteアプリケーション例外クラス

Created on 2016/03/23

@author: openkannyu
'''


class GracenoteAppExcepion( Exception ):

    def __init__( self, errcd, errmsg ):
        self.errcd = errcd
        self.errmsg = errmsg
