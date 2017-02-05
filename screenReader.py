import cv2
import ImageGrab

class Size(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
'''
class Screen(object):
    def __init__(self, size):
        if not size:
            self.getCoordinatesFromUser()
        self._size = size
        self._imageCapture = CaptureImage(self._size)

    def getCoordinatesFromUser(self):
        pass

    def takeScreenshot(self):
        self._imageCapture.capture()

    def findArtifactOnScreen(self, artifact):
        pass

    def findMultipleArtifacts(self, artifacts):
        pass
        #This should return set of X,Y of found artifacts
'''
class CaptureImage(object):
    def __init__(self, size):
        self.x = size.x
        self.y = size.y
        self.x2 = size.x + size.w
        self.y2 = size.y + size.h
        self._image = None

    @property
    def image(self):
        return self._image

    def capture(self):
        self._image = ImageGrab.grab(bbox=self.box())
        self._image.save('test.png')

    def box(self):
        return self.x, self.y, self.x2, self.y2