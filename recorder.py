import cv2
from motion_detect import m_d

class recorder:
    file_name = "static/video/video.avi"
    frames_per_second = 240

    def save_frame(self, out, frame):
        frame = m_d.output_frame2
        out.write(frame)

    def startRecording(self):
        global m_d
        out = cv2.VideoWriter(self.file_name, cv2.VideoWriter_fourcc(*'XVID'), self.frames_per_second, (800,450))
        while True:
            self.save_frame(out, m_d.output_frame2)

        #out.release()


handler = recorder()
