import cv2
import sys

print(sys.argv)

global PREVIEW, INPUT, OUTPUT, clipLimit, tileGridSize
PREVIEW = False
INPUT = None
OUTPUT = None
clipLimit = 1.0
tileGridSize = 8

HELP = """
run: python(3) clach.py -i $NAME {params}
params: 
-h = print this message (help)
-i $NAME = input image path
-o $NAME = output image path
-p = preview image
-cl = (float) clipLimit parameter of cv2.CLAHE | default is 1.0
-gs = (int) tileGridSize parameter of cv2.CLAHE | default is 8 means (8 by 8 matrix)
"""


def exit_help():
    print(HELP)
    exit(0)


def parse_param(substring):
    global PREVIEW, INPUT, OUTPUT, clipLimit, tileGridSize
    if substring[0] == "-h":
        exit_help()
    elif substring[0] == "-i":
        INPUT = substring[1]
    elif substring[0] == "-o":
        OUTPUT = substring[1]
    elif substring[0] == "-p":
        PREVIEW = True
    elif substring[0] == "-cl":
        clipLimit = float(substring[1])
    elif substring[0] == "-gs":
        tileGridSize = int(substring[1])
    else:
        exit_help()


start_index = 0
if len(sys.argv) <= start_index:
    exit_help()
if "python" in sys.argv[start_index]:
    start_index += 1
    if len(sys.argv) <= start_index:
        exit_help()
if "clach.py" in sys.argv[start_index]:
    start_index += 1
    if len(sys.argv) <= start_index:
        exit_help()
start_index_old = None
while start_index < len(sys.argv):
    index = start_index
    if sys.argv[start_index].startswith("-"):
        index = start_index + 1
        while index < len(sys.argv):
            if sys.argv[index].startswith("-"):
                break
            index += 1
        parse_param(sys.argv[start_index:index])
    if start_index_old is None:
        start_index_old = index
    elif start_index_old != index:
        start_index_old = start_index
    else:
        break
    start_index = index

if INPUT is not None:
    image = cv2.imread(INPUT)
else:
    exit_help()

clahe = cv2.createCLAHE(clipLimit=clipLimit,
                        tileGridSize=(tileGridSize, tileGridSize))
channels = cv2.split(image)
for i in range(len(channels)):
    channels[i] = clahe.apply(channels[i])
image_CLAHE = cv2.merge(channels)

if OUTPUT is not None:
    cv2.imwrite(OUTPUT, image_CLAHE)

if PREVIEW:
    window_name = OUTPUT if OUTPUT is not None else "CLAHE " + INPUT
    window_name = "{press any key to close} " + window_name
    cv2.namedWindow(window_name)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow(window_name, 0, 0)
    cv2.imshow(window_name, image_CLAHE)
    cv2.waitKey(0)
