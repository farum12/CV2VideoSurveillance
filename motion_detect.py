import datetime
import imutils
import cv2
import numpy as np
from database_handler import getLastSetting

class motionDetect:
    frame_width = 800
    first_frame = None
    # videoAddress for camera is 0
    # http://208.139.200.133/mjpg/video.mjpg
    # http://192.168.1.53:8000/stream.mjpg
    video_stream = cv2.VideoCapture("http://208.139.200.133/mjpg/video.mjpg")
    output_frame = np.zeros([frame_width, frame_width, 3], dtype=np.uint8)
    output_frame2 = np.zeros([frame_width, frame_width, 3], dtype=np.uint8)
    ticks=0
    settings = None

    def put_timestamp(self, frame):
        if (self.settings.displayTimestamp == "yes"):
            cv2.putText(frame,
                        datetime.datetime.now().strftime("%a %d/%m/%Y %H:%M:%S"),
                        (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_DUPLEX, 0.35, (0, 0, 255), 1)

    def put_area_mark(self, frame, area ,text,x,y):
        cv2.putText(frame, area, (x, y), cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 0, 255), 2)
        cv2.putText(frame, text, (x, y+15), cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 0, 255), 2)

    def save_outputs(self, frame):
        #cv2.imwrite("static/img/sysfeed.jpg", frame)
        self.output_frame = cv2.imencode('.jpg', frame)[1].tobytes()
        self.output_frame2 = frame

    def no_analysis(self):
        frame =  self.video_stream.read()
        frame = frame[1]
        frame = imutils.resize(frame, width=self.frame_width)
        self.put_timestamp(frame)
        self.save_outputs(frame)

    def two_area_analysis(self, vertical):
        if(self.settings.area1 == 'True'):
            detect_first_area = True
        else:
            detect_first_area = False
        if (self.settings.area2 == 'True'):
            detect_second_area = True
        else:
            detect_second_area = False
        frame = self.video_stream.read()
        frame = frame[1]
        if(detect_first_area):
            text_ar1 = "No movement"
        else:
            text_ar1 = "Detection turned off"
        if (detect_second_area):
            text_ar2 = "No movement"
        else:
            text_ar2 = "Detection turned off"

        frame = imutils.resize(frame, width=self.frame_width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if self.first_frame is None or (self.ticks > self.settings.maxTicks):
            self.first_frame = gray
            self.ticks = 0

        frameDelta = cv2.absdiff(self.first_frame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            if cv2.contourArea(c) < self.settings.sensitivity:
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            # perform verification for 1st Area
            if(vertical):
                if(detect_first_area and x < int(frame.shape[1]/2)):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (255, 0, 255), 2)
                    # verify movement for the 1st Area
                    text_ar1 = "Movement"
                    detected_movement = True
                # perform verification for 2nd Area
                if (detect_second_area and x > int(frame.shape[1]/2)):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (255, 0, 255), 2)
                    # verify movement for the 1st Area
                    text_ar2 = "Movement"
            else:
                if (detect_first_area and y < int(frame.shape[0]/2)):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (255, 0, 255), 2)
                    # verify movement for the 1st Area
                    text_ar1 = "Movement"
                    detected_movement = True
                    # perform verification for 2nd Area
                if (detect_second_area and y > int(frame.shape[0]/2)):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (255, 0, 255), 2)
                    # verify movement for the 1st Area
                    text_ar2 = "Movement"

        self.put_area_mark(frame, "Area 1", text_ar1, 10, 20)
        if(vertical):
            self.put_area_mark(frame, "Area 2", text_ar2,
                               int(frame.shape[1]/2) + 10, 20)
        else:
            self.put_area_mark(frame, "Area 2", text_ar2,
                               10, int(frame.shape[0]/2) + 20)
        if(self.settings.displayBoundaries == 'yes'):
            if(vertical):
                cv2.line(frame, (int(frame.shape[1]/2), 0),
                         (int(frame.shape[1]/2), frame.shape[0]),
                         (255, 0, 255), 2, 8, 0)
            else:
                cv2.line(frame, (0, int(frame.shape[0]/2)),
                         (int(frame.shape[1]), int(frame.shape[0]/2)),
                         (255, 0, 255),
                         2, 8, 0)
        cv2.putText(frame, "Counter no:" + str(self.ticks),
                    (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_DUPLEX, 0.35,
                    (0, 0, 255), 1)
        self.put_timestamp(frame)
        self.ticks = self.ticks + 1
        self.save_outputs(frame)

    def three_area_analysis(self, vertical):
        if (self.settings.area1 == 'True'):
            detect_first_area = True
        else:
            detect_first_area = False
        if (self.settings.area2 == 'True'):
            detect_second_area = True
        else:
            detect_second_area = False
        if (self.settings.area3 == 'True'):
            detect_third_area = True
        else:
            detect_third_area = False
        frame = self.video_stream.read()
        frame = frame[1]
        if(detect_first_area):
            text_ar1 = "No movement"
        else:
            text_ar1 = "Detection turned off"
        if (detect_second_area):
            text_ar2 = "No movement"
        else:
            text_ar2 = "Detection turned off"
        if (detect_third_area):
            text_ar3 = "No movement"
        else:
            text_ar3 = "Detection turned off"


        frame = imutils.resize(frame, width=self.frame_width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if self.first_frame is None or (self.ticks > self.settings.maxTicks):
            self.first_frame = gray
            self.ticks = 0

        frameDelta = cv2.absdiff(self.first_frame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            if cv2.contourArea(c) < self.settings.sensitivity:
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            if(vertical):
                if(detect_first_area and x < int(frame.shape[1]/3)):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (255, 0, 255), 2)
                    # verify movement for the 1st Area
                    text_ar1 = "Movement"
                    detected_movement = True
                # perform verification for 2nd Area
                if (detect_second_area and x > int(frame.shape[1]/3) and x < int(frame.shape[1]*2/3)):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (255, 0, 255), 2)
                    # verify movement for the 1st Area
                    text_ar2 = "Movement"
                # perform verification for 3rd Area
                if (detect_third_area and x > int(frame.shape[1] * 2 / 3)):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (255, 0, 255), 2)
                    # verify movement for the 1st Area
                    text_ar3 = "Movement"
            else:
                if (detect_first_area and y < int(frame.shape[0] / 3)):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (255, 0, 255), 2)
                    # verify movement for the 1st Area
                    text_ar1 = "Movement"
                    detected_movement = True
                    # perform verification for 2nd Area
                if (detect_second_area and y > int(frame.shape[0] / 3) and y < int(frame.shape[0] * 2 / 3)):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (255, 0, 255), 2)
                    # verify movement for the 1st Area
                    text_ar2 = "Movement"
                    # perform verification for 3rd Area
                if (detect_third_area and y > int(frame.shape[0] * 2 / 3)):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (255, 0, 255), 2)
                    # verify movement for the 1st Area
                    text_ar3 = "Movement"

        self.put_area_mark(frame, "Area 1", text_ar1, 10, 20)
        if (vertical):
            self.put_area_mark(frame, "Area 2", text_ar2,
                               int(frame.shape[1]/3) + 10, 20)
            self.put_area_mark(frame, "Area 3", text_ar3,
                               int(frame.shape[1]*2/3) + 10, 20)
        else:
            self.put_area_mark(frame, "Area 2", text_ar2, 10,
                               int(frame.shape[0]/3) + 20)
            self.put_area_mark(frame, "Area 3", text_ar3, 10,
                               int(frame.shape[0]*2/3) + 20)

        if(self.settings.displayBoundaries == 'yes'):
            if (vertical):
                cv2.line(frame, (int(frame.shape[1] / 3), 0),
                         (int(frame.shape[1] / 3), frame.shape[0]),
                         (255, 0, 255),
                         2, 8, 0)
                cv2.line(frame, (int(frame.shape[1]*2/3), 0),
                         (int(frame.shape[1]*2/3), frame.shape[0]),
                         (255, 0, 255), 2, 8, 0)
            else:
                cv2.line(frame, (0, int(frame.shape[0]/3)),
                         (int(frame.shape[1]), int(frame.shape[0]/3)),
                         (255, 0, 255),
                         2, 8, 0)
                cv2.line(frame, (0, int(frame.shape[0]*2/3)),
                         (int(frame.shape[1]), int(frame.shape[0]*2/3)),
                         (255, 0, 255),
                         2, 8, 0)

        cv2.putText(frame, "Counter no:" + str(self.ticks),
                    (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_DUPLEX, 0.35,
                    (0, 0, 255), 1)
        self.put_timestamp(frame)
        self.ticks = self.ticks + 1
        self.save_outputs(frame)


    def simple_analysis(self):
        frame = self.video_stream.read()
        frame = frame[1]
        text = "No movement"
        frame = imutils.resize(frame, width=self.frame_width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        #reset the comparision frame to prevent false positives
        if self.first_frame is None or (self.ticks > self.settings.maxTicks):
            self.first_frame = gray
            self.ticks = 0

        # calculate the odds between present frame and comparision frame
        frameDelta = cv2.absdiff(self.first_frame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # ignore countours with small area
            if cv2.contourArea(c) < self.settings.sensitivity:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
            text = "Detected"



        # Put information about detected movement and put timestamp
        cv2.putText(frame, "Movement Status: {}".format(text),
                    (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Counter no:" + str(self.ticks),
                    (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_DUPLEX,
                    0.35, (0, 0, 255), 1)
        self.put_timestamp(frame)
        self.ticks = self.ticks + 1
        self.save_outputs(frame)
        #cv2.imshow("Security Feed", self.output_frame)
        #key = cv2.waitKey(1) & 0xFF

    def start_analysis(self):
        while True:
            self.settings = getLastSetting()
            if(self.settings.analysisMode == "noAn"):
                self.no_analysis()
            elif(self.settings.analysisMode == "simple"):
                self.simple_analysis()
            elif (self.settings.analysisMode == "2areaVert"):
                self.two_area_analysis(True)
            elif (self.settings.analysisMode == "3areaVert"):
                self.three_area_analysis(True)
            elif (self.settings.analysisMode == "2areaHor"):
                self.two_area_analysis(False)
            elif (self.settings.analysisMode == "3areaHor"):
                self.three_area_analysis(False)
            else:
                self.no_analysis()

    def display_window(self):
        while True:
            cv2.imshow("Security Feed", np.array(self.output_frame))
            key = cv2.waitKey(1) & 0xFF

    #def get_frame(self):
    #    return self.output_frame

m_d = motionDetect()