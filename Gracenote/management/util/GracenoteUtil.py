'''
Created on 2016/06/09

@author: kannyu
'''

class GracenoteUtil(object):
    '''
    classdocs
    '''

    def __init__(self, params):
      pass;
   
    @staticmethod
    def convertTitle(line):
      line = line.replace( u"／" , u"/")\
                 .replace( u"－" , u"-")\
                 .replace( u"-+" , u"-")\
                 .replace( u"　" , u" ")\
                 .replace( u" +" , u" ")\
                 .replace( u"（" , u"\\(")\
                 .replace( u"［" , u"\\[")\
                 .replace( u"）" , u"\\)")\
                 .replace( u"］" , u"\\]")

      # Common Pattern
      cm_ptn01 = u"\\(.*\\)"
      cm_ptn02 = u"\.avi|\.mkv|\.mpg|\.iso|\.wmv|\.mp4|\.asf|\.m4v|\.rmvb"
      cm_ptn03 = u" - 19[0-9][0-9] \[Brazil\]$"
      cm_ptn04 = u" - 19[0-9][0-9] \[Soul-Jazz\]$"
      cm_ptn05 = u" - Jazz Funk$"
      cm_ptn06 = u" - Jazz Fusion$"
      cm_ptn07 = u"^A JazzMan Dean Upload - "
      cm_ptn08 = u"^A FLG Maurepas upload - "
  
      line = re.sub(cm_ptn01, "", line)
      line = re.sub(cm_ptn02, "", line)
      line = re.sub(cm_ptn03, "", line)
      line = re.sub(cm_ptn04, "", line)
      line = re.sub(cm_ptn05, "", line)
      line = re.sub(cm_ptn06, "", line)
      line = re.sub(cm_ptn07, "", line)
      line = re.sub(cm_ptn08, "", line)
  
      # Track Pattern
      line_track = copy.copy(line)
  
      tr_ptn01 = u".*『(.*)』.*"
      tr_ptn02 = u".*「(.*)」.*"
      tr_ptn03 = u".*\"(.*)\".*"
      tr_ptn04 = u".*/(.*)"
      tr_ptn05 = u".* - (.*)"
  
      line_track = re.sub(tr_ptn01 , u"\\1" , line_track)
      line_track = re.sub(tr_ptn02 , u"\\1" , line_track)
      line_track = re.sub(tr_ptn03 , u"\\1" , line_track)
      line_track = re.sub(tr_ptn04 , u"\\1" , line_track)
      line_track = re.sub(tr_ptn05 , u"\\1" , line_track)

      tr_ptn06 = u"【.*】"
      tr_ptn07 = u"\\(.*\\)"
      tr_ptn08 = u"\\[.*\\]"
      tr_ptn09 = u"[1-2][0-9][0-9][0-9]"
      tr_ptn10 = u"^　+"
      tr_ptn11 = u"^ +"
      tr_ptn12 = u" +$"
      tr_ptn13 = u"　+$"
      tr_ptn14 = u"\".*"

      line_track = re.sub(tr_ptn06 , u"" , line_track)
      line_track = re.sub(tr_ptn07 , u"" , line_track)
      line_track = re.sub(tr_ptn08 , u"" , line_track)
      line_track = re.sub(tr_ptn09 , u"" , line_track)
      line_track = re.sub(tr_ptn10 , u"" , line_track)
      line_track = re.sub(tr_ptn11 , u"" , line_track)
      line_track = re.sub(tr_ptn12 , u"" , line_track)
      line_track = re.sub(tr_ptn13 , u"" , line_track)
      line_track = re.sub(tr_ptn14 , u"" , line_track)


      # Artist Pattern
      line_artist = copy.copy(line)

      ar_ptn01 = u"(.*)/.*"
      ar_ptn02 = u"(.*) - .*"
  
      line_artist = re.sub(ar_ptn01 , u"\\1" , line_artist)
      line_artist = re.sub(ar_ptn02 , u"\\1" , line_artist)

      ar_ptn03 = u"『.*"
      ar_ptn04 = u"「.*"
      ar_ptn05 = u"【.*"
      ar_ptn06 = u"\".*"
      ar_ptn07 = u"\\(.*"
      ar_ptn08 = u"\\[.*"
      ar_ptn09 = u"[1-2][0-9][0-9][0-9]"
      ar_ptn10 = u"^　+"
      ar_ptn11 = u"^ +"
      ar_ptn12 = u" +$"
      ar_ptn13 = u"　+$"

      line_artist = re.sub(ar_ptn03 , u"" , line_artist)
      line_artist = re.sub(ar_ptn04 , u"" , line_artist)
      line_artist = re.sub(ar_ptn05 , u"" , line_artist)
      line_artist = re.sub(ar_ptn06 , u"" , line_artist)
      line_artist = re.sub(ar_ptn07 , u"" , line_artist)
      line_artist = re.sub(ar_ptn08 , u"" , line_artist)
      line_artist = re.sub(ar_ptn09 , u"" , line_artist)
      line_artist = re.sub(ar_ptn10 , u"" , line_artist)
      line_artist = re.sub(ar_ptn11 , u"" , line_artist)
      line_artist = re.sub(ar_ptn12 , u"" , line_artist)
      line_artist = re.sub(ar_ptn13 , u"" , line_artist)

      return (line_track, line_artist)
