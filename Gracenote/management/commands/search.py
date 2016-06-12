# coding: utf-8
'''

音楽情報収集バッチ

Created on 2016/03/23
Updated on __updated__

@author: openkannyu
'''
from __future__ import print_function

import codecs
import json
import logging
import re
import sys
import traceback

from django.conf import settings as st
from django.core.management.base import BaseCommand
import requests

from Gracenote.management.bean.ResultData import ResultData
from Gracenote.management.exception.GracenoteAppExcepion import GracenoteAppExcepion
from Gracenote.management.util.GracenoteUtil import GracenoteUtil
import pygn


logger = logging.getLogger( __name__ )

class Command( BaseCommand ):
  args = "<target_id target_id ...>"
  help = u"トラック名/アーティスト名をキーにGracenoteから音楽情報を取得するバッチです"

  def handle( self, *args, **options ):
    logger.info( "[start] " + __name__ )

    try:
      # Gracenote Auth Logic
      _clientID = st.GR_API_CLIENT_ID
      _userID = pygn.register( _clientID )


      # Read inputFile and put into List per yline (contains CR+LF)
      f = codecs.open( st.MZ_LST_FILE, "r", "utf-8" )
      ylineList = f.readlines()
      f.close()


      # Search music data per yline
      for yline in ylineList:
        rd = ResultData()
        strRc = "0"
        strLc = "0"

        # search youtube API
        video_id = ""
        yline = yline.rstrip()
        ylineArray = re.split(r'v=', yline)
        if(len(ylineArray)>1): video_id = ylineArray[1]

        headers = {}
        headers.update(st.YT_API_CONTENT_TYPE)
        payload = {"key" : st.YT_API_KEY, "part" : st.YT_API_PART,"id" : video_id}
        logger.info("headers=" + str(st.YT_API_CONTENT_TYPE))
        logger.info("payload=" + str(payload))

        r = requests.get(st.YT_API_URI, headers=headers, params=payload, verify=False, timeout=(st.YT_API_CONN_TIMEOUT, st.YT_API_READ_TIMEOUT))
        logger.info("REQUEST_URL=" + r.url)
        logger.info("HTTP_STATUS=" + str(r.status_code))
        logger.debug("HTTP_RESPONSE=" + r.text)

        if r.status_code != st.HTTP_OK:
            raise GracenoteAppExcepion(st.ECD_API_SVRERR,st.EMS_API_SVRERR.format(st.ECD_API_SVRERR, r.text))

        # youtubeデータParse処理
        dictYTdata = json.loads(r.text, "utf-8")
        logger.debug("dictYTdata=" + str(dictYTdata))
  
  
        # youtubeデータ整形処理
        strTitle = ""
        for record in dictYTdata["items"]:
            strTitle = record["snippet"]["title"]

        (line_track, line_artist) = GracenoteUtil.convertTitle(strTitle)
        logger.info( "Line_Track: " + line_track + "\t" + "Line_Artist: " + line_artist )

        #search Left
        _track = line_track
        _artist = line_artist
        resultJson = pygn.search( clientID = _clientID, userID = _userID, artist = _artist, track = _track )
        resultString = json.dumps( resultJson, sort_keys = True, indent = 4 )
        logger.debug( resultString.decode( 'unicode_escape' ))
        logger.info( "Left Track Search: " + "TrackReq=" + _track + "\t" + "ArtistReq=" + _artist )

        rdL = ResultData()
        rdL.loadResult(resultString)

        if(rdL.trackTitle.lower() == _track.lower()): rdL.mcount = rdL.mcount + 1
        if(rdL.albumArtistName.lower() == _artist.lower()): rdL.mcount = rdL.mcount + 1
        logger.debug( "rdL.trackTitle.lower(): " + rdL.trackTitle.lower() + "\t" + "_track.lower(): " + _track.lower() )
        logger.debug( "rdL.albumArtistName.lower(): " + rdL.albumArtistName.lower() + "\t" + "_artist.lower(): " + _artist.lower() )

        #search Right
        _track = line_artist
        _artist = line_track
        resultJson = pygn.search( clientID = _clientID, userID = _userID, artist = _artist, track = _track )
        resultString = json.dumps( resultJson, sort_keys = True, indent = 4 )
        logger.debug( resultString.decode( 'unicode_escape' ))
        logger.info( "Right Track Search: " + "TrackReq=" + _track + "\t" + "ArtistReq=" + _artist )

        rdR = ResultData()
        rdR.loadResult(resultString)

        if(rdR.trackTitle.lower() == _track.lower()): rdR.mcount = rdR.mcount + 1
        if(rdR.albumArtistName.lower() == _artist.lower()): rdR.mcount = rdR.mcount + 1
        logger.debug( "rdR.trackTitle.lower(): " + rdR.trackTitle.lower() + "\t" + "_track.lower(): " + _track.lower() )
        logger.debug( "rdR.albumArtistName.lower(): " + rdR.albumArtistName.lower() + "\t" + "_artist.lower(): " + _artist.lower() )


        # Count Point LR
        logger.info( "rdL.mcount: " + str(rdL.mcount) + "\t" + "rdR.mcount: " + str(rdR.mcount) )
        if(rdR.mcount > rdL.mcount):
          rd = rdR
          strRc = str(rdR.mcount)
          strLc = str(rdL.mcount)
          logger.info( "TrackRes=" + rdR.trackTitle + "\t" + "ArtistRes=" + rdR.albumArtistName )
        elif(rdL.mcount<>0):
          rd = rdL
          strRc = str(rdR.mcount)
          strLc = str(rdL.mcount)
          logger.info( "TrackRes=" + rdL.trackTitle + "\t" + "ArtistRes=" + rdL.albumArtistName )
        else:
          logger.info( "TrackRes=" + "None" + "\t" + "ArtistRes=" + "None" )


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
              + strLc + "\t"
              + strRc
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
