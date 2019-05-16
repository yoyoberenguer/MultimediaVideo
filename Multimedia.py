import pygame
import cv2
from cv2 import COLOR_RGBA2BGR
import numpy
import math
import sys



# Wave algorithm both direction x, y
def wave_xy(texture_, rad1_, amplitude_):
    
    w, h = texture_.get_size()
    xblocks = range(0, w, amplitude_)
    yblocks = range(0, h, amplitude_)
    glitch = pygame.Surface((w, h), pygame.SRCALPHA)
    for x in xblocks:
        xpos = (x + (math.sin(rad1_ + x * 1 / (amplitude_ ** 2)) * amplitude_)) + amplitude_
        for y in yblocks:
            ypos = (y + (math.sin(rad1_ + y * 1 / (amplitude_ ** 2)) * amplitude_)) + amplitude_
            glitch.blit(texture_, (0 + x, 0 + y), (xpos, ypos, amplitude_, amplitude_))

    return glitch.convert()



def cobra():
    pygame.init()
    SCREEN = pygame.display.set_mode((800, 1024), 32)
    swoosh = pygame.mixer.Sound("Assets\\swoosh.ogg")
    impact = pygame.mixer.Sound("Assets\\Impact.ogg")
    gunshot = pygame.mixer.Sound("Assets\\GunShot.ogg")
    gunshot.set_volume(0.2)

    SCREEN_IMPACT1 = pygame.image.load('Assets\\Broken glass.png').convert_alpha()
    SCREEN_IMPACT1 = pygame.transform.scale(SCREEN_IMPACT1, (128, 128))

    SCREEN_IMPACT = pygame.image.load('Assets\\broken_screen_overlay.png').convert_alpha()
    SCREEN_IMPACT = pygame.transform.scale(SCREEN_IMPACT, (128, 128))

    surface_org = pygame.image.load("Assets\\Cobra1.png").convert()
    surface_org = pygame.transform.smoothscale(surface_org, (900, 1024)).convert()
    surface_org_x2 = pygame.transform.smoothscale(surface_org, (800 * 2, 1024 * 2)).convert()

    CLOCK = pygame.time.Clock()

    stop_game = False
    angle = 0
    scale = 1
    min_s = 1500
    angle_inc = 20
    surface = surface_org_x2.copy()
    stop = False
    angle1 = 0
    frame = 0

    global RECORDING, VIDEO
    
    while not stop_game:

        try:
            

            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if any(keys):
                stop_game = True

            if not stop:
                surface = pygame.transform.rotozoom(surface_org_x2.copy(), angle, scale)
            else:
                SCREEN.fill((0, 0, 0, 255))
                surface = wave_xy(surface_org.copy(), angle1, 10)

            rect = surface.get_rect(center=SCREENRECT.center)
            SCREEN.blit(surface, (SCREENRECT.centerx - int(rect.w / 2),
                                  SCREENRECT.centery - int(rect.h / 2)))

            frame += 1
            if not stop:
                if surface.get_width() > min_s:
                    angle += angle_inc
                    if angle % 80 == 0:
                        swoosh.play()
                else:
                    if angle != 0:
                        angle += angle_inc
                    else:
                        impact.play()
                        stop = True
            else:
                if not stop_game:
                    if frame == 80:
                        gunshot.play()
                        surface_org.blit(SCREEN_IMPACT1, (300, 400))
                    elif frame == 120:
                        gunshot.play()
                        surface_org.blit(SCREEN_IMPACT, (390, 250))
                    elif frame == 140:
                        gunshot.play()
                        surface_org.blit(SCREEN_IMPACT, (300, 170))

            angle %= 360
            angle1 += 0.1
            scale -= 0.05 if surface.get_width() > min_s else 0
            pygame.display.flip()

                
            if RECORDING:
                VIDEO.append(pygame.image.tostring(SCREEN, 'RGB', False))     
        
            pygame.event.clear()
            CLOCK.tick_busy_loop(30)
        
        except pygame.error:
                print('\n [-] Insufficient Memory to record string buffer !!!')
                stop_game = True
                RECORDING = False
                VIDEO = []
                
        
            

if __name__ == '__main__':

    # This algorithm is using pygame library to generate the game sprite animation,
    # For each new frame, the current display (SCREEN) is converted to a string buffer and pushed
    # into a python list (VIDEO), all the data are uncompressed and the memory can be filled very quickly
    # especially with FPS > 30 
    # After pressing ESCAPE, all the recorded frames are converted to pygame surfaces before being
    # compressed into an AVI file
    # ** NOTE: No sound will be added to the final AVI file.
    # If you want to contribute and add some code to generate an AVI file with sound stream;
    # feel free to post your own version.

    SCREENRECT = pygame.Rect(0, 0, 800, 1024)
    pygame.display.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.HWACCEL, 32)
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4095)

    STOP_GAME = False

    RECORDING = True   # Display recording allowed True | False
    VIDEO = []         # string buffer

    clock = pygame.time.Clock()
    FRAME = 0
    cobra()
    

    while not STOP_GAME:

        pygame.event.pump()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            STOP_GAME = True

        # *** UPDATE AND DRAW YOUR SPRITES HERE ***

        # Cap the speed at 60 FPS
        TIME_PASSED_SECONDS = clock.tick(30)

        pygame.display.flip()
      
        # Creates uncompress string that can be transferred with the 'fromstring' method in other Python imaging packages.
        # Some Python image packages prefer their images in bottom-to-top format (PyOpenGL for example).
        # If you pass True for the flipped argument, the string buffer will be vertically flipped.
        # The format argument is a string of one of the following values. Note that only 8-bit Surfaces can
        # use the "P" format. The other formats will work for any Surface.
        # Also note that other Python image packages support more formats than pygame.
        # P, 8-bit palettized Surfaces
        # RGB, 24-bit image
        # RGBX, 32-bit image with unused space
        # RGBA, 32-bit image with an alpha channel
        # ARGB, 32-bit image with alpha channel first
        # RGBA_PREMULT, 32-bit image with colors scaled by alpha channel
        # ARGB_PREMULT, 32-bit image with colors scaled by alpha channel, alpha channel first

        # UNCOMMENT THE LINE BELOW TO RECORD FRAMES FROM THIS LOOP
        """
        try:
            if RECORDING:
                VIDEO.append(pygame.image.tostring(SCREEN, 'RGB', False))
        except MemoryError:
            print('\n [-] Insufficient Memory to record string buffer !!!')      
            STOP_GAME = True
            RECORDING = False 
        """
        
        FRAME += 1
        pygame.event.clear()

    # Return the size of an object in bytes
    print('\n [+] VIDEO Object size : ', sys.getsizeof(VIDEO)) 
    print('\n [+] RECORDING AVI file ')
    # *** Record the video
    if RECORDING:

        # Parameters
        # filename	Name of the output video file.
        # fourcc	4-character code of codec used to compress the frames. For example,
        #               VideoWriter::fourcc('P','I','M','1') is a MPEG-1 codec, VideoWriter::fourcc('M','J','P','G')
        #               is a motion-jpeg codec etc. List of codes can be obtained at Video Codecs by FOURCC page.
        #               FFMPEG backend with MP4 container natively uses other values as fourcc code: see ObjectType,
        #               so you may receive a warning message from OpenCV about fourcc code conversion.
        # fps	Framerate of the created video stream.
        # frameSize	Size of the video frames.
        # isColor	If it is not zero, the encoder will expect and encode color frames,
        #               otherwise it will work with grayscale frames (the flag is currently supported on Windows only).
        # Tips:

        # With some backends fourcc=-1 pops up the codec selection dialog from the system.
        # To save image sequence use a proper filename (eg. img_%02d.jpg) and fourcc=0 OR fps=0.
        # Use uncompressed image format (eg. img_%02d.BMP) to save raw frames.
        # Most codecs are lossy. If you want lossless video file you need to use a
        # lossless codecs (eg. FFMPEG FFV1, Huffman HFYU, Lagarith LAGS, etc...)
        # If FFMPEG is enabled, using codec=0; fps=0; you can create an uncompressed (raw) video file.
        video = cv2.VideoWriter('YourVideoName.avi',
                                cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30,
                                (SCREENRECT.w, SCREENRECT.h), True)
                                #cv2.VideoWriter_fourcc('P','I','M','1'), 30,
                                #(SCREENRECT.w, SCREENRECT.h), True)
                                

        for event in pygame.event.get():
            pygame.event.clear()

        for image in VIDEO:
            
            image = numpy.frombuffer(image, numpy.uint8).reshape(SCREENRECT.h, SCREENRECT.w, 3)

            # Python: cv.CvtColor(src, dst, code) → None
            # Parameters:	
            # src – input image: 8-bit unsigned, 16-bit unsigned ( CV_16UC... ), or single-precision floating-point.
            # dst – output image of the same size and depth as src.
            # code – color space conversion code (see the description below).
            # dstCn – number of channels in the destination image; if the parameter is 0,
            #the number of the channels is derived automatically from src and code .`
            image = cv2.cvtColor(image, COLOR_RGBA2BGR)
            video.write(image)

        cv2.destroyAllWindows()
        video.release()
        
    pygame.quit()
