# coding: utf-8
'''

音楽情報収集バッチ

Created on 2016/03/23
Updated on 2016/03/28

@author: openkannyu
'''
from __future__ import print_function

import codecs
import json
import logging
import sys
import traceback

from django.conf import settings as st
from django.core.management.base import BaseCommand

from Gracenote.management.bean.ResultData import ResultData
from Gracenote.management.exception.GracenoteAppExcepion import GracenoteAppExcepion


logger = logging.getLogger( __name__ )

class Command( BaseCommand ):
  args = "<target_id target_id ...>"
  help = u"トラック名/アーティスト名をキーにGracenoteから音楽情報を取得するバッチです"

  def handle( self, *args, **options ):
    logger.info( "[start] " + __name__ )

    try:

      # Gracenote Auth Logic
      _clientID = st.API_CLIENT_ID
      _userID = pygn.register( _clientID )

      # Read inputFile and put into List per line (contains CR+LF)
      f = codecs.open( st.MZ_LST_FILE, "r", "utf-8" )
      lineList = f.readlines()
      f.close()

      # Search music data per line
      for line in lineList:
          line = line.rstrip()
          lm = line.split( "\t" )

          #search Left
          _trackL = lm[0]
          _artistL = lm[1]
          logger.info( "Left Track Search: " + "TrackReq=" + _trackL + "\t" + "ArtistReq=" + _artistL )

          rdL = ResultData()
          rdL.search( clientID = _clientID, userID = _userID, artist = _artistL, track = _trackL )

          #search Right
          _trackR = lm[1]
          _artistR = lm[0]
          logger.info( "Right Track Search: " + "TrackReq=" + _trackR + "\t" + "ArtistReq=" + _artistR )

          rdR = ResultData()
          rdR.search( clientID = _clientID, userID = _userID, artist = _artistR, track = _trackR )

          logger.info( "rdL.mcount: " + str(rdL.mcount) + "\t" + "rdR.mcount: " + str(rdR.mcount) )
          if(rdR.mcount > rdL.mcount):
            rd = rdR
            logger.info( "TrackRes=" + rdR.trackTitle + "\t" + "ArtistRes=" + rdR.albumArtistName )
          elif(rdL.mcount<>0):
            rd = rdL
            logger.info( "TrackRes=" + rdL.trackTitle + "\t" + "ArtistRes=" + rdL.albumArtistName )
          else:
            rd = None
            logger.info( "TrackRes=" + "None" + "\t" + "ArtistRes=" + "None" )

          if rd is not None:
            print( rd.trackTitle + "\t"
                  + rd.albumArtistName + "\t"
                  + rd.genre1TEXT + "\t"
                  + rd.genre2TEXT + "\t"
                  + rd.genre3TEXT + "\t"
                  + rd.mood1TEXT + "\t"
                  + rd.mood2TEXT + "\t"
                  + rd.tempo1TEXT + "\t"
                  + rd.tempo2TEXT + "\t"
                  + rd.albumYear + "\t"
                  + str(rdL.mcount) + "\t"
                  + str(rdR.mcount)
                  )
          else:
            print( "-" + "\t"
                  + "-" + "\t"
                  + "-" + "\t"
                  + "-" + "\t"
                  + "-" + "\t"
                  + "-" + "\t"
                  + "-" + "\t"
                  + "-" + "\t"
                  + "-" + "\t"
                  + "-" + "\t"
                  + str(rdL.mcount) + "\t"
                  + str(rdR.mcount)
                  )

    except GracenoteAppExcepion as ge:
        logger.error( ge.errmsg )
        ( errtype, errval, errtrace ) = sys.exc_info()
        hemsg = st.EMS_BODY.format( str( errtype ), str( errval ), str( traceback.format_tb( errtrace ) ) )
        logger.error( hemsg )

    except Exception:
        logger.error( st.EMS_SYSTEMERR.format( st.ECD_SYSTEMERR ) )
        ( errtype, errval, errtrace ) = sys.exc_info()
        hemsg = st.EMS_BODY.format( str( errtype ), str( errval ), str( traceback.format_tb( errtrace ) ) )
        logger.error( hemsg )

    else:
        logger.info( "batch executed successfully!" )

    finally:
        logger.info( "[end] " + __name__ )
