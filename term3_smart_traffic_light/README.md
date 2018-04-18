We designed the smart traffic light to help the neighbourhood the cut down the total CO2 emission by achieving
the following functions:
1. if there is no car on lane1 and no car on lane two, both of the traffic light would dim so as to cut down electricity cost.
2. if there is car on road1 and there is no car on road2, the traffic light for road1 will be green to let the car pass, and save unnessary carbon dioxide emission
3. the system will record how many cars have passed by during a certain period for analysis of the road condition and further adjustment of the distribution for the traffic light
4. the red light will act normally if there is no car

we simulate the whole scenario using two roads, road1 and road2. each have a traffic light

how we achieve this:
thymio_1.py (run on Rpi) controls thymio1 on road1
the thymio will stop according to the traffic light color obtanined from the firebase. but it will stop only until the black line at the crossing road and there is red light.
otherwise it will continue moving

thymio_2.py (run on Rpi) controls thymio2 on road2
same function as thymio_2.py

KIVY_GUI.py (run on computer)
shows the information obtained from the firebase:
the road1 and road2 condition (whether there is thymio) on firebase
if there is thymio on the road then the button is red otherwise the button is green

traffic_light.py (run on Rpi)
get the road condition ( whether there is thymio or not) and update the corresponding changed color of the red light onto the firebase.
if there is car the corresponding light on the given road should be turned green. and update on the corresponding traffic light controled by the Rpi

color_detection_red.py and object_detection_webcam.py
using machine learnning algo to detect whether there is a thymio( car ) on the road, and upload the road condition onto the firebase

machine learning:
using faster_rcnn model established by tensorflow, to train the neural net on GTX 1070.
the code package can be find here if you want to use the trained model.
https://www.dropbox.com/sh/565jqna54vtm7en/AACn-baVOl4WvX8ajgOTs9x_a?dl=0
follow the tutorial:
https://www.youtube.com/watch?v=Rgpfk6eYxJA&t=1065s
the result is robust, and can detect thymio in all aspects and all kinds of condition, such as shaded.

used opencv to detect color cause we cannot ditinguish the direction of the thymio(which road is the thymio at) if only use rcnn.
