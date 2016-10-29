from webcam import Webcam
from detection import Detection
from audiorecord import AudioRecord
from audioanalysis import AudioAnalysis
from time import sleep
 
webcam = Webcam()
webcam.start()
  
detection = Detection()
audio_record = AudioRecord()
audio_analysis = AudioAnalysis()
 
while True:
     
    # girlfriend's question to Arkwood
    print "Do you still love me?"
 
    # get Arkwood's voice from microphone
    voice_file = audio_record.voice()
    is_yes = audio_analysis.is_yes(voice_file)
     
    # get Arkwoods's hand gesture from webcam
    image = webcam.get_current_frame()
    is_okay = detection.is_item_detected_in_image('haarcascade_okaygesture.xml', image.copy())
    is_vicky = detection.is_item_detected_in_image('haarcascade_vickygesture.xml', image.copy())
     
    # Arwood's answer to girlfriend
    if is_yes and is_okay:
        print "I love you!"
    elif is_yes and is_vicky:
        print "Like, I would die a thousand times just to kiss your feet. Whatever."
    else:
        print "Snooker's on TV. Can't you bother me later?"
 
    # give Arkwood a break before nagging him again
    sleep(30)
