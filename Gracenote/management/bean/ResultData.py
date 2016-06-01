# coding: utf-8
'''

Gracenote検索結果クラス

Created on 2016/03/28

@author: openkannyu
'''
import json
import logging

import pygn


logger = logging.getLogger( __name__ )


class ResultData( object ):


    def __init__( self ):
      self.genre1TEXT = "-"
      self.genre2TEXT = "-"
      self.genre3TEXT = "-"
      self.mood1TEXT = "-"
      self.mood2TEXT = "-"
      self.tempo1TEXT = "-"
      self.tempo2TEXT = "-"
      self.albumArtistName = "-"
      self.trackTitle = "-"
      self.albumYear = "-"
      self.mcount = 0

    def loadResult(self, resultString):
      # Parsing resultString
      dictMZ = json.loads( resultString, "utf-8" )
      logger.debug( "dictMZ=" + str( dictMZ ).decode( 'unicode_escape' ))

      if dictMZ is not None:
         if dictMZ["genre"].has_key( "1" ): self.genre1TEXT = dictMZ["genre"]["1"]["TEXT"]
         if dictMZ["genre"].has_key( "2" ): self.genre2TEXT = dictMZ["genre"]["2"]["TEXT"]
         if dictMZ["genre"].has_key( "3" ): self.genre3TEXT = dictMZ["genre"]["3"]["TEXT"]
         if dictMZ["mood"].has_key( "1" ) : self.mood1TEXT = dictMZ["mood"]["1"]["TEXT"]
         if dictMZ["mood"].has_key( "2" ) : self.mood2TEXT = dictMZ["mood"]["2"]["TEXT"]
         if dictMZ["tempo"].has_key( "1" ): self.tempo1TEXT = dictMZ["tempo"]["1"]["TEXT"]
         if dictMZ["tempo"].has_key( "2" ): self.tempo2TEXT = dictMZ["tempo"]["2"]["TEXT"]
         if dictMZ.has_key( "album_artist_name" ): self.albumArtistName = dictMZ["album_artist_name"]
         if dictMZ.has_key( "track_title" ): self.trackTitle = dictMZ["track_title"]
         if dictMZ.has_key( "album_year" ): self.albumYear = dictMZ["album_year"]
         logger.debug( "dictMZ is not None")
      else:
         logger.debug( "dictMZ is None")

      return self
