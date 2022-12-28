from flask import Flask,render_template,request,send_file,after_this_request
from pytube import YouTube
import os


server = Flask(__name__)

@server.route("/")
def index():
    return render_template("index.html")
@server.route("/video",methods=["POST"])
def video():
    PROGRESSIVE_VIDEO = {
    5: ("240p", "64kbps"),
    6: ("270p", "64kbps"),
    13: ("144p", None),
    17: ("144p", "24kbps"),
    18: ("360p", "96kbps"),
    22: ("720p", "192kbps"),
    34: ("360p", "128kbps"),
    35: ("480p", "128kbps"),
    36: ("240p", None),
    37: ("1080p", "192kbps"),
    38: ("3072p", "192kbps"),
    43: ("360p", "128kbps"),
    44: ("480p", "128kbps"),
    45: ("720p", "192kbps"),
    46: ("1080p", "192kbps"),
    59: ("480p", "128kbps"),
    78: ("480p", "128kbps"),
    82: ("360p", "128kbps"),
    83: ("480p", "128kbps"),
    84: ("720p", "192kbps"),
    85: ("1080p", "192kbps"),
    91: ("144p", "48kbps"),
    92: ("240p", "48kbps"),
    93: ("360p", "128kbps"),
    94: ("480p", "128kbps"),
    95: ("720p", "256kbps"),
    96: ("1080p", "256kbps"),
    100: ("360p", "128kbps"),
    101: ("480p", "192kbps"),
    102: ("720p", "192kbps"),
    132: ("240p", "48kbps"),
    151: ("720p", "24kbps"),
    300: ("720p", "128kbps"),
    301: ("1080p", "128kbps"),
   }


    DASH_VIDEO = {
    # DASH Video
    133: ("240p", None),  # MP4
    134: ("360p", None),  # MP4
    135: ("480p", None),  # MP4
    136: ("720p", None),  # MP4
    137: ("1080p", None),  # MP4
    138: ("2160p", None),  # MP4
    160: ("144p", None),  # MP4
    167: ("360p", None),  # WEBM
    168: ("480p", None),  # WEBM
    169: ("720p", None),  # WEBM
    170: ("1080p", None),  # WEBM
    212: ("480p", None),  # MP4
    218: ("480p", None),  # WEBM
    219: ("480p", None),  # WEBM
    242: ("240p", None),  # WEBM
    243: ("360p", None),  # WEBM
    244: ("480p", None),  # WEBM
    245: ("480p", None),  # WEBM
    246: ("480p", None),  # WEBM
    247: ("720p", None),  # WEBM
    248: ("1080p", None),  # WEBM
    264: ("1440p", None),  # MP4
    266: ("2160p", None),  # MP4
    271: ("1440p", None),  # WEBM
    272: ("4320p", None),  # WEBM
    278: ("144p", None),  # WEBM
    298: ("720p", None),  # MP4
    299: ("1080p", None),  # MP4
    302: ("720p", None),  # WEBM
    303: ("1080p", None),  # WEBM
    308: ("1440p", None),  # WEBM
    313: ("2160p", None),  # WEBM
    315: ("2160p", None),  # WEBM
    330: ("144p", None),  # WEBM
    331: ("240p", None),  # WEBM
    332: ("360p", None),  # WEBM
    333: ("480p", None),  # WEBM
    334: ("720p", None),  # WEBM
    335: ("1080p", None),  # WEBM
    336: ("1440p", None),  # WEBM
    337: ("2160p", None),  # WEBM
    394: ("144p", None),  # MP4
    395: ("240p", None),  # MP4
    396: ("360p", None),  # MP4
    397: ("480p", None),  # MP4
    398: ("720p", None),  # MP4
    399: ("1080p", None),  # MP4
    400: ("1440p", None),  # MP4
    401: ("2160p", None),  # MP4
    402: ("4320p", None),  # MP4
    571: ("4320p", None),  # MP4
    694: ("144p", None),  # MP4
    695: ("240p", None),  # MP4
    696: ("360p", None),  # MP4
    697: ("480p", None),  # MP4
    698: ("720p", None),  # MP4
    699: ("1080p", None),  # MP4
    700: ("1440p", None),  # MP4
    701: ("2160p", None),  # MP4
    702: ("4320p", None),  # MP4
    }

    DASH_AUDIO = {
    # DASH Audio
    139: (None, "48kbps"),  # MP4
    140: (None, "128kbps"),  # MP4
    141: (None, "256kbps"),  # MP4
    171: (None, "128kbps"),  # WEBM
    172: (None, "256kbps"),  # WEBM
    249: (None, "50kbps"),  # WEBM
    250: (None, "70kbps"),  # WEBM
    251: (None, "160kbps"),  # WEBM
    256: (None, "192kbps"),  # MP4
    258: (None, "384kbps"),  # MP4
    325: (None, None),  # MP4
    328: (None, None),  # MP4
}

    ITAGS = {
    **PROGRESSIVE_VIDEO,
    **DASH_VIDEO,
    **DASH_AUDIO,
}
    form_data= request.form
    link=form_data["url"]
    yt=YouTube(link)
    title=yt.title
    thumbnail=yt.thumbnail_url
    st=yt.streams.filter(progressive=True)

    dictav={}
    for stm in st:
        itag=int(stm.itag)

        if itag in ITAGS:
            res, bitrate = ITAGS[itag]
            if(res):
                dictav[itag]=res
        else:
            res, bitrate = None, None
    dicta={}
    st=yt.streams.filter(only_audio=True)
    for stm in st:
        itag=int(stm.itag)
        dicta[itag]=stm.abr

                
      
    dictv={}
    st=yt.streams.filter(adaptive=True)
    for stm in st:
        itag=int(stm.itag)

        if itag in ITAGS:
            res, bitrate = ITAGS[itag]
            if(res):
                dictv[itag]=res
        else:
            res, bitrate = None, None     
    
    return render_template("video.html",title=title,thumbnail=thumbnail,url=link,dictav=dictav,dicta=dicta,dictv=dictv)
@server.route("/download",methods=["POST"])
def download():
    form_data= request.form
    # return form_data
    link=form_data["url"]
    yt=YouTube(link)
    if(form_data["V"]=="b"):
        stm=yt.streams.get_by_itag(int(form_data["ovquality"]))
    elif(form_data["V"]=="a"):
        stm=yt.streams.get_by_itag(int(form_data["oquality"]))
    else:
        stm=yt.streams.get_by_itag(int(form_data["vquality"]))



    f=stm.download()
    return f
    # @after_this_request
    # def remove_file(response):
    #     try:
    #         os.remove(f)
            
    #     except Exception as error:
    #         print("Error removing or closing downloaded file handle")
    #     return response

    # return send_file(f, as_attachment=True) 
@server.route("/downloadfile",methods=["POST"])
def downloadf():
    f=request.form['filename']
    @after_this_request
    def remove_file(response):
        try:
            os.remove(f)
            
        except Exception as error:
            print("Error removing or closing downloaded file handle")
        return response
    return send_file(f, as_attachment=True)

server.run(debug=True)