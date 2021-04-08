import threading
import web_app
import cv2
from motion_detect import motionDetect, m_d
import database_handler
import recorder
import time

def delayed_start():
    time.sleep(3)
    recorder.handler.startRecording()

def init():
    global m_d
    database_handler.init_db()
    database_handler.debugDb()
    motion_detect_compare_thread = threading.Thread(target=m_d.start_analysis)
    motion_detect_compare_thread.start()
    web_app_thread = threading.Thread(target=web_app.start)
    web_app_thread.start()
    #recorder_thread = threading.Thread(target=delayed_start)
    #recorder_thread.start()

init()


