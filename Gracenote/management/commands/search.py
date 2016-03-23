# coding: utf-8
'''

音楽データ収集バッチ

Created on 2016/03/23
Updated on 2016/03/23

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

#import GracenoteAppException  # @UnresolvedImport
import pygn


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = "<target_id target_id ...>"
    help = u"トラック名/アーティスト名をキーにGracenoteから音楽情報を取得するバッチプログラムです。"

    def handle(self, *args, **options):
        logger.info("[start] " + __name__)

        try:

            # Gracenote Auth Logic
            _clientID = st.API_CLIENT_ID  # Enter your Client ID from developer.gracenote.com here
            _userID = pygn.register(_clientID)  # Get a User ID from pygn.register() - Only register once per end-user

            # Read inputFile and put into List per line (contains CR+LF)
            f = codecs.open(st.MZ_LST_FILE, "r", "utf-8")
            lineList = f.readlines()
            f.close()

            # Search music data per line
            for line in lineList:
                line = line.rstrip()
                lm = line.split("\t")
                _track = lm[0].encode()
                _artist = lm[1].encode()
                logger.info("TrackReq=" + _track + "\t" + "ArtistReq=" + _artist)

                result = pygn.search(clientID=_clientID, userID=_userID, artist=_artist, track=_track)
                resultString = json.dumps(result, sort_keys=True, indent=4)
                logger.debug(resultString)

                genre1TEXT = "-"
                genre2TEXT = "-"
                genre3TEXT = "-"
                mood1TEXT = "-"
                mood2TEXT = "-"
                tempo1TEXT = "-"
                tempo2TEXT = "-"
                albumArtistName = "-"
                trackTitle = "-"
                chkAlbumArtistName = "-"
                chkTrackTitle = "-"
                albumYear = "-"

                # Parsing resultString
                dictMZdata = json.loads(resultString, "utf-8")
                logger.info("dictMZdata=" + str(dictMZdata))

                if dictMZdata is not None:
                    if dictMZdata["genre"].has_key("1"): genre1TEXT = dictMZdata["genre"]["1"]["TEXT"]
                    if dictMZdata["genre"].has_key("2"): genre2TEXT = dictMZdata["genre"]["2"]["TEXT"]
                    if dictMZdata["genre"].has_key("3"): genre3TEXT = dictMZdata["genre"]["3"]["TEXT"]
                    if dictMZdata["mood"].has_key("1") : mood1TEXT = dictMZdata["mood"]["1"]["TEXT"]
                    if dictMZdata["mood"].has_key("2") : mood2TEXT = dictMZdata["mood"]["2"]["TEXT"]
                    if dictMZdata["tempo"].has_key("1"): tempo1TEXT = dictMZdata["tempo"]["1"]["TEXT"]
                    if dictMZdata["tempo"].has_key("2"): tempo2TEXT = dictMZdata["tempo"]["2"]["TEXT"]
                    if dictMZdata.has_key("album_artist_name"): albumArtistName = dictMZdata["album_artist_name"]
                    if dictMZdata.has_key("track_title"): trackTitle = dictMZdata["track_title"]
                    if dictMZdata.has_key("album_year"): albumYear = dictMZdata["album_year"]

#                    if(trackTitle != _track): chkTrackTitle = trackTitle
#                    if(albumArtistName != _artist): chkAlbumArtistName = albumArtistName
                    chkTrackTitle = trackTitle
                    chkAlbumArtistName = albumArtistName
                    logger.info("TrackRes=" + trackTitle + "\t" +  "ArtistRes=" + albumArtistName)
                else:
                    logger.info("TrackRes=" + "None" + "\t" +  "ArtistRes=" + "None")

                print(chkTrackTitle + "\t"
                      + chkAlbumArtistName + "\t"
                      + genre1TEXT + "\t"
                      + genre2TEXT + "\t"
                      + genre3TEXT + "\t"
                      + mood1TEXT + "\t"
                      + mood2TEXT + "\t"
                      + tempo1TEXT + "\t"
                      + tempo2TEXT + "\t"
                      + albumYear)

#        except GracenoteAppException as he:
#            logger.error(he.errmsg)
#            (errtype, errval, errtrace) = sys.exc_info()
#            hemsg = st.EMS_BODY.format(str(errtype), str(errval), str(traceback.format_tb(errtrace)))
#            logger.error(hemsg)

        except Exception:
            logger.error(st.EMS_SYSTEMERR.format(st.ECD_SYSTEMERR))
            (errtype, errval, errtrace) = sys.exc_info()
            hemsg = st.EMS_BODY.format(str(errtype), str(errval), str(traceback.format_tb(errtrace)))
            logger.error(hemsg)

        else:
             logger.info("batch executed successfully!")

        finally:
            logger.info("[end] " + __name__)
