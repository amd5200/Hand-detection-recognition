#!/usr/bin/python
# coding: utf -8                   #加上這行才能key中文 要import urllib2
import urllib2
"""
This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
Hand detection by: R.O.C Taiwan Harry Lin
"""
import sys
import cv2.cv as cv
import cv2
from optparse import OptionParser
import serial
import time

#建立一个鼠标和键盘对象
from pymouse import PyMouse
from pykeyboard import PyKeyboard
m = PyMouse()
k = PyKeyboard()

#-------------------espeak---------------------------------
import os # Linux Befehle os.system(...)
import getpass # Username auslesen getpass.getuser()

os.system("espeak -v zh+f3 -s 140 歡迎使用手部辨識系統 ")   #女聲 可選擇f2~f5四種音調
time.sleep(0.1)

# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned
# for accurate yet slow object detection. For a faster operation on real video
# images the settings are:
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
# min_size=<minimum possible face size

min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0
#arduino=serial.Serial('/dev/ttyUSB0',9600)


#创建一个矩形，来让我们在图片上写文字，参数依次定义了文字类型，高，宽，字体厚度等。
font=cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 4)

#width = 160 #leave None for auto-detection
#height = 120 #leave None for auto-detection
#width = 320 #leave None for auto-detection
#height = 240 #leave None for auto-detection
width = 640 #leave None for auto-detection
height = 480 #leave None for auto-detection
middle_w = 2 #Cross Center width 十字中心歸零校正,數字越大線往左
middle_h = 2 #Cross Center height 十字中心歸零校正,數字越大線往上

def detect_and_draw(img, cascade):
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                   cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

######   若解析度有改變，下面劃線座標亦隨之改變##############
    cv.Line(img, (width/middle_w,0),(width/middle_w,height), (0,10,255),3) 
    cv.Line(img, ((width/middle_w-20),(height/middle_h-10)),((width/middle_w-20),(height/middle_h+10)), (0,10,255),2)
    cv.Line(img, ((width/middle_w+20),(height/middle_h-10)),((width/middle_w+20),(height/middle_h+10)), (0,10,255),2) 
    cv.Line(img, (0,height/middle_h),(width,height/middle_h), (0,10,255),3) 
    cv.Line(img, ((width/middle_w-10),(height/middle_h-20)),((width/middle_w+10),(height/middle_h-20)), (0,10,255),2)
    cv.Line(img, ((width/middle_w-10),(height/middle_h+20)),((width/middle_w+10),(height/middle_h+20)), (0,10,255),2)
    #cv.ShowImage("camera", img)

#######虛擬按鍵#################################################
    TestStr = "==>"
    cv.PutText(img, TestStr , ((width*6/7),(height*4/7)), font, (0,0,255)) 
    TestStr = "<=="
    cv.PutText(img, TestStr , ((width*1/7),(height*4/7)), font, (0,0,255)) 
     
    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
##################################################################################################3333
                cx = (int(x * image_scale) + int((x + w) * image_scale)) / 2
                cy = (int(y * image_scale) + int((y + h) * image_scale)) / 2
                print cx, cy

#将文字框加入到图片中，(5,30)定义了文字框左顶点在窗口中的位置，最后参数定义文字颜色

                if cx <= (width*7/7) and cx >= (width*6/7) and cy <= (height*4/7) and cy >= (height*3/7) :
                     TestStr = "OK!"
                     cv.PutText(img, TestStr , (5,30), font, (0,0,255)) 
                     #k.tap_key('e')   #偵測後自動key in 'e' 字元
                     #k.tap_key(k.tab_key)
                     #k.tap_key(k.function_keys[5])  # Tap F5 全螢幕圖片
                     k.tap_key(k.left_key) #偵測後自動 key in 方向鍵左
                     #os.system("espeak -v zh+f3 -s 140 okay ")   #女聲 可選擇f2~f5四種音調
                     #time.sleep(0.5)
                if cx <= (width*2/7) and cx >= (width*1/7) and cy <= (height*4/7) and cy >= (height*3/7) :
                     TestStr = "OK!"
                     cv.PutText(img, TestStr , (5,30), font, (0,0,255)) 
                     #k.tap_key('e')   #偵測後自動key in 'e' 字元
                     #k.tap_key(k.tab_key)
                     #k.tap_key(k.function_keys[5])  # Tap F5 全螢幕圖片
                     #m.click(cx, cy, 1, n = 1)  #左鍵點擊cx,cy座標點1次
                     k.tap_key(k.right_key) #偵測後自動 key in 方向鍵右
                     #os.system("espeak -v zh+f3 -s 140 okay ")   #女聲 可選擇f2~f5四種音調
                     #time.sleep(0.5)
                else:
                     TestStr = "serching...."
                     cv.PutText(img, TestStr , (160,30), font, (0,255,0))
                     m.move(cx, cy)    #移動鼠標到cx,cy座標點
                     #m.click(cx, cy, 1, n = 1)  #左鍵點擊cx,cy座標點1次
                     #m.click(cx, cy, 1, n = 2)  #左鍵點擊cx,cy座標點2次
                     #m.click(cx, cy, 2, n = 1)  #右鍵點擊cx,cy座標點一次

#################################################################################################################
                '''
                if cx < img.width*3/ 7 :
                     arduino.write('4')
                     print '4'
		if cx < img.width*2/ 7 :
                     arduino.write('44')
                     print '4'
		if cx < img.width/ 7 :
                     arduino.write('4444')
                     print '44'

                if cx > img.width*4 / 7 :
                     arduino.write('6')
                     print '6'
                if cx > img.width*5/ 7 :
                     arduino.write('66')
                     print '6'
                if cx > img.width*6/ 7 :
                     arduino.write('6666')
                     print '66'
                if cy < img.height*3/ 7:
                     arduino.write('2')
                     print '2'
                if cy < img.height*2/ 7:
                     arduino.write('22')
                     print '2'
                if cy < img.height/ 7:
                     arduino.write('2222')
                     print '222'
                if cy > img.height*4 / 7:
                     arduino.write('8')
                     print '8'
                if cy > img.height*5 / 7:
                     arduino.write('88')
                     print '8'
                if cy > img.height*6 / 7:
                     arduino.write('8888')
                     print '888'
		break
                '''
######################################################

    cv.ShowImage("result", img)

if __name__ == '__main__':

    #cascade = cv.Load("haarcascade_eye_tree_eyeglasses.xml")
    #cascade = cv.Load("haarcascade_frontalface_alt.xml")
    #cascade = cv.Load("cars3.xml")
    cascade_ok = cv.Load("haarcascade_okaygesture.xml")
    #cascade = cv.Load("hand.xml")
    #cascade = cv.Load("fist.xml")
    #cascade = cv.Load("haarcascade_vickygesture.xml")
    cascade = cv.Load("closed_frontal_palm.xml")
    #cascade = cv.Load("palm.xml")
    #cascade = cv.Load("smile.xml")

    capture = cv.CreateCameraCapture(2)                   # camera   NO. 0, 1, 2
    print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)

    cv.NamedWindow("result", 1)
    frame = cv.QueryFrame(capture)
    
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 

    if capture:
        frame_copy = None
        while True:
            frame = cv.QueryFrame(capture)

            if not frame:
                #print 'hehe'
                #cv.WaitKey(0)
                continue#break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)

            detect_and_draw(frame_copy, cascade)

            if cv.WaitKey(10) == 27:
                break

    cv.DestroyWindow("result")
