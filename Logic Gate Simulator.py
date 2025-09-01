#imports
import pygame, sys
from button_modified import Button
import pickle
import time
import os
from binaryConvert import binaryConvert

#clock pulse variables set
finalTime = 0
clockPulse = None
activeGate = None
fileName = None

#stack lists set
undoStack = []
redoStack = []

#pygame initialised
pygame.init()

#screen instantiated
SCREEN = pygame.display.set_mode((1280, 720))

#counts set
count = 0
lastCountChange = 0

#background image loaded for main menu
BG = pygame.image.load("Background.png")

#colours set
WHITE = "#FFFBFC"
BLACK = "#010400"
BLUE = "#4392F1"
RED = "#AE0E2E"
#930E29
GREEN = "#7CA982"
GREY = "#967D69"

#font creation
def get_font1(size): 
    return pygame.font.Font("font1.ttf", size)
def get_font2(size):
    return pygame.font.Font("font2.ttf", size)
def get_font3(size):
    return pygame.font.Font("font3.otf", size)

#logicArray and fileName parameters are used to return the user to their document once they have saved or go back
def saveAsInterface(logicArray, fileName):
    pygame.display.set_caption("Save As")
    #font for user text
    baseFont = get_font3(32)
    userText = ""
    #text input is shown to user in a rectangle
    inputRect = pygame.Rect(390,315,200,40)
    colour = pygame.Color(WHITE)
    while True:
        saveAs_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(BLACK)
        saveFile_TEXT = get_font2(45).render("Enter New File Name", True, WHITE)
        saveFile_RECT = saveFile_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(saveFile_TEXT, saveFile_RECT)
        saveFileBack = Button(pos=(100, 675), text_input="BACK", font=get_font2(35), base_color=WHITE, hovering_color=GREY)
        #enter button only works if the user has inputted a name
        if userText != "":
            saveFileEnter = Button(pos=(640, 420), text_input="ENTER", font=get_font2(35), base_color=WHITE, hovering_color=GREY)
        else:
            saveFileEnter = Button(pos=(640, 420), text_input="ENTER", font=get_font2(35), base_color=GREY, hovering_color=GREY)
        #user text is placed onto pygame window
        textSurface = baseFont.render(userText,True,(255,255,255))
        SCREEN.blit(textSurface, (inputRect.x + 5, inputRect.y - 5))
        pygame.draw.rect(SCREEN,colour,inputRect,2)
        #rectangle changes with the length of the text
        inputRect.w = textSurface.get_width()+10
        
        for button in [saveFileBack, saveFileEnter]:
            button.changeColor(saveAs_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #pressing back returns the user to the logic interface in the state it was before
                if saveFileBack.checkForInput(saveAs_MOUSE_POS):
                    logicInterface(logicArray, fileName, False)
                if saveFileEnter.checkForInput(saveAs_MOUSE_POS):
                    #enter button only works if the user has inputted a name
                    if userText != "":
                        logicFile = open(userText, 'wb')
                        pickle.dump(logicArray, logicFile)
                        logicFile.close()
                        print("Save Successful")
                        #save successful prompt displayed
                        saveText = get_font2(35).render("Save Successful", True, GREEN)
                        saveTextRect = saveText.get_rect()
                        saveTextRect.center = (640,380)
                        SCREEN.blit(saveText, saveTextRect)
                        pygame.display.update()
                        #prompt is displayed for one second
                        time.sleep(1)
                        #returns user to logic document
                        logicInterface(logicArray, userText, False)
            if event.type == pygame.KEYDOWN:
                #pressing backspace removes a letter from the text
                if event.key == pygame.K_BACKSPACE:
                    userText = userText[:-1]
                #if the key being pressed is not alphanumeric nothing happens
                elif event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE or event.key == pygame.K_DELETE:
                    pass
                #pressing enter attempts a save
                elif event.key == pygame.K_RETURN:
                    if userText != "":
                        logicFile = open(userText, 'wb')
                        pickle.dump(logicArray, logicFile)
                        logicFile.close()
                        print("Save Successful")
                        saveText = get_font2(35).render("Save Successful", True, GREEN)
                        saveTextRect = saveText.get_rect()
                        saveTextRect.center = (640,380)
                        SCREEN.blit(saveText, saveTextRect)
                        pygame.display.update()
                        time.sleep(1)
                        logicInterface(logicArray, userText, False)
                #pressing any other key adds it to the text input
                else:
                    #max character limit 30
                    if len(userText) <= 30:
                        userText += event.unicode
        pygame.display.update()

#parameters used to determine the menu to return to, as well the contents of the logic interface, if the user is accessing the menu from there
def loadInterface(logicArray, fileName, menuBack):
    pygame.display.set_caption("Load")
    #font for user text
    baseFont = get_font3(32)
    userText = ""
    #text input is shown in a rectangle
    inputRect = pygame.Rect(390,315,200,40)
    colour = pygame.Color(WHITE)
    while True:
        load_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(BLACK)
        loadFile_TEXT = get_font2(45).render("Enter file name to load", True, WHITE)
        loadFile_RECT = loadFile_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(loadFile_TEXT, loadFile_RECT)
        loadFileBack = Button(pos=(100, 675), text_input="BACK", font=get_font2(35), base_color=WHITE, hovering_color=GREY)
        #enter button only works if the user has inputted a name
        if userText != "":
            loadFileEnter = Button(pos=(640, 420), text_input="ENTER", font=get_font2(35), base_color=WHITE, hovering_color=GREY)
        else:
            loadFileEnter = Button(pos=(640, 420), text_input="ENTER", font=get_font2(35), base_color=GREY, hovering_color=GREY)
        #user text is placed into pygame window
        textSurface = baseFont.render(userText,True,(255,255,255))
        SCREEN.blit(textSurface, (inputRect.x + 5, inputRect.y - 5))
        pygame.draw.rect(SCREEN,colour,inputRect,2)
        inputRect.w = textSurface.get_width()+10
        
        for button in [loadFileBack, loadFileEnter]:
            button.changeColor(load_MOUSE_POS)
            button.update(SCREEN)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if loadFileBack.checkForInput(load_MOUSE_POS):
                    #if the user accessed the load interface from the main menu they are returned to the main menu
                    if menuBack == True:
                        mainMenu()
                    #otherwise the user is returned to their logic circuit in the state it was previously
                    else:
                        logicInterface(logicArray,fileName, False)
                if loadFileEnter.checkForInput(load_MOUSE_POS):
                    print(logicArray)
                    #exception handling used to check if file exists
                    try:
                        logicFile = open(userText, 'rb')
                    except:
                        loadFailText = get_font2(35).render("File Not Found", True, RED)
                        loadFailTextRect = loadFailText.get_rect()
                        loadFailTextRect.center = (640,380)
                        SCREEN.blit(loadFailText, loadFailTextRect)
                        pygame.display.update()
                        time.sleep(1)
                    else:
                        logicArray = pickle.load(logicFile)
                        logicFile.close()
                        logicInterface(logicArray,userText, False)
            if event.type == pygame.KEYDOWN:
                #pressing backspace removes a letter from the text
                if event.key == pygame.K_BACKSPACE:
                    userText = userText[:-1]
                #if the key being pressed is not alphanumeric nothing happens
                elif event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE or event.key == pygame.K_DELETE:
                    pass
                #pressing enter attempts to load a file
                elif event.key == pygame.K_RETURN:
                    try:
                        logicFile = open(userText, 'rb')
                    except:
                        loadFailText = get_font2(35).render("File Not Found", True, RED)
                        loadFailTextRect = loadFailText.get_rect()
                        loadFailTextRect.center = (640,380)
                        SCREEN.blit(loadFailText, loadFailTextRect)
                        pygame.display.update()
                        time.sleep(1)
                    else:
                        logicArray = pickle.load(logicFile)
                        logicFile.close()
                        logicInterface(logicArray,userText, False)
                #pressing any other key adds it to text input
                else:
                    if len(userText) <= 30:
                        userText += event.unicode
                
        pygame.display.update()
        
def translate(truthTable, switchCount, lightCount, switchCombinations, logicArray, fileName):
    pygame.display.set_caption("Truth Table")
    #screen height increased to 850 from 720
    SCREEN = pygame.display.set_mode((1280, 850))
    #combined count determined
    combinedCount = switchCount + lightCount
    print(combinedCount)
    print((combinedCount*49))
    print(switchCombinations)
    while True:
        #grid pixel values change depending on number of switches and lights
        if switchCount == 1:
            SCREEN.fill(BLACK)
            #column lines drawn
            for i in range(0,(combinedCount*49)+1,49):
                pygame.draw.line(SCREEN,WHITE,(i+542,40),(i+542,combinedCount*49+40),2)
            #row lines drawn
            for i in range(0,(switchCombinations*49)+1,49):
                pygame.draw.line(SCREEN,WHITE,(542,i+40),(switchCombinations*49+542,i+40),2)
        elif switchCount == 2:
            SCREEN.fill(BLACK)
            if lightCount == 1:
                for i in range(0,(combinedCount*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(i+542,40),(i+542,combinedCount*49+89),2)
                for i in range(0,(switchCombinations*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(542,i+40),(switchCombinations*49+493,i+40),2)
            if lightCount == 2:
                for i in range(0,(combinedCount*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(i+542,40),(i+542,combinedCount*49+40),2)
                for i in range(0,(switchCombinations*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(542,i+40),(switchCombinations*49+542,i+40),2)
        elif switchCount == 3:
            SCREEN.fill(BLACK)
            if lightCount == 2:
                for i in range(0,(combinedCount*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(i+542,40),(i+542,combinedCount*49+40+147),2)
                for i in range(0,(switchCombinations*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(542,i+40),(switchCombinations*49+542-147,i+40),2)
            elif lightCount == 1:
                for i in range(0,(combinedCount*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(i+542,40),(i+542,combinedCount*49+40+147+49),2)
                for i in range(0,(switchCombinations*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(542,i+40),(switchCombinations*49+542-196,i+40),2)
        #max number of inputs accepted is 4
        elif switchCount == 4:
            SCREEN.fill(BLACK)
            if lightCount == 1:
                for i in range(0,(combinedCount*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(i+542,40),(i+542,combinedCount*49+578),2)
                for i in range(0,(switchCombinations*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(542,i+40),(switchCombinations*49+4,i+40),2)
            elif lightCount == 2:
                for i in range(0,(combinedCount*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(i+542,40),(i+542,combinedCount*49+529),2)
                for i in range(0,(switchCombinations*49)+1,49):
                    pygame.draw.line(SCREEN,WHITE,(542,i+40),(switchCombinations*49+53,i+40),2)
        else:
            SCREEN.fill(BLACK)
                
        #used to define position in logic array
        countHorizontal = 0
        countVertical = 0
        #used to determine where to place inputs and outputs text
        rectangleWidth = 0
        #input states are generated in grid
        for i in range(40,(switchCombinations*49)+40,49):
            rectangleWidth += 49
            for j in range(542,(switchCount*49)+542,49):
                #state being placed depends on horizontal and vertical position in truth table array
                truthTable_TEXT = get_font1(25).render(str(truthTable[0][countVertical][countHorizontal]), True, WHITE)
                #i and j values equal the pixel count at the top left corner of the grid square, 25 is added to each value to find the centre
                truthTable_RECT = truthTable_TEXT.get_rect(center=(j+25, i+25))
                SCREEN.blit(truthTable_TEXT, truthTable_RECT)
                #if the number of the position of the input value <= number of inputs 
                if countHorizontal < switchCount-1:
                    countHorizontal += 1
                #otherwise move onto next row
                else:
                    countHorizontal = 0
                    countVertical += 1
        
        #input header text is generated at a fixed position
        inputsText = get_font1(15).render("Inputs", True, WHITE)
        inputTextRect = pygame.Rect(542,20,rectangleWidth, 20)
        SCREEN.blit(inputsText, inputTextRect)
                    
        countHorizontal = 0
        countVertical = 0
        rectangleWidth = 0
        #output states are generated in grid
        for i in range(40,(switchCombinations*49)+40,49):
            for j in range((switchCount*49)+542,(lightCount*49)+(switchCount*49)+542,49):
                truthTable_TEXT = get_font1(25).render(str(truthTable[1][countVertical][countHorizontal]), True, GREY)
                truthTable_RECT = truthTable_TEXT.get_rect(center=(j+25, i+25))
                SCREEN.blit(truthTable_TEXT, truthTable_RECT)
                if countHorizontal < lightCount-1:
                    countHorizontal += 1
                else:
                    countHorizontal = 0
                    countVertical += 1
        
        #output header text is generated based on the amount of inputs compared to inputs and outputs
        outputText = get_font1(15).render("Outputs", True, WHITE)
        outputTextRect = pygame.Rect((switchCount*49)+542,20,rectangleWidth, 20)
        SCREEN.blit(outputText, outputTextRect)
        
        translate_MOUSE_POS = pygame.mouse.get_pos()
        
        translateBack = Button(pos=(100, 675), text_input="BACK", font=get_font2(35), base_color=WHITE, hovering_color=GREY)
        
        translateBack.changeColor(translate_MOUSE_POS)
        translateBack.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                print("X pos " + str(mouseX))
                print("Y pos " + str(mouseY))
                #back button returns user to original document
                if translateBack.checkForInput(translate_MOUSE_POS):
                    logicInterface(logicArray, fileName, False)

        pygame.display.update()
    

        
def logicInterface(logicArray, fileName, tutorialMode):
    #window naming
    if tutorialMode == True:
        pygame.display.set_caption("Tutorial")
    elif fileName == None:
        pygame.display.set_caption("New Document")
    else:
        pygame.display.set_caption(fileName)
        
    #global variables
    global count
    global lastCountChange
    global activeGate
    global undoStack
    global redoStack
    global finalTime
    global clockPulse
    
    #display set
    SCREEN = pygame.display.set_mode((1280, 720))
    
    #clock pulse synchronisation
    lastChange = time.time()
    clockPulse = False
    finalTime = time.time() + 1
    
    #tutorial mode selection
    if tutorialMode == True:
        tutorialPhase = 1
    if tutorialMode == False:
        tutorialPhase = None
    
    #auto save initial values
    autoSave = False
    autoSaveStartTime = time.time()

    
    while True:
        count += 1
        logicInterface_MOUSE_POS = pygame.mouse.get_pos()
        
        #save check
        if fileName != None and fileName != "halfAdder" and fileName != "fullAdder":
            try:
                logicFileTest = open(fileName, "rb")
            except:
                fileName = None
            else:
                logicFileTest.close()
                
        #auto save check
        if fileName == None:
            autoSave = False
        
        SCREEN.fill(WHITE)
        #logic menu draw
        #load gate image
        ORGate = pygame.image.load("ORGate.png")
        #creation of background rectangle needed for the OR gate to be displayed
        ORrect = ORGate.get_rect()
        ORrect.center = (50,120)
        #creation of the text description of the gate, colours change depending on events in the logic interface
        if activeGate == "ORGate":
            ORText = get_font3(15).render("OR Gate", True, BLUE)
        elif tutorialPhase == None  or tutorialPhase == 10:
            ORText = get_font3(15).render("OR Gate", True, BLACK)
        elif tutorialPhase != None:
            ORText = get_font3(15).render("OR Gate", True, GREY)
        #creation of the background rectangle needed for text description
        ORrectText = ORText.get_rect()
        ORrectText.center = (50,155)
        
        #all other logic elements follow the same format
        
        NOTGate = pygame.image.load("NOTGate.png")
        NOTrect = NOTGate.get_rect()
        NOTrect.center = (125,120)
        if activeGate == "NOTGate":
            NOTText = get_font3(15).render("NOT Gate", True, BLUE)
        elif tutorialPhase == None or tutorialPhase == 3:
            NOTText = get_font3(15).render("NOT Gate", True, BLACK)
        elif tutorialPhase != None:
            NOTText = get_font3(15).render("NOT Gate", True, GREY)
        NOTrectText = NOTText.get_rect()
        NOTrectText.center = (125,155)
        
        ANDGate = pygame.image.load("ANDGate.png")
        ANDrect = ANDGate.get_rect()
        ANDrect.center = (200,120)
        if activeGate == "ANDGate":
            ANDText = get_font3(15).render("AND Gate", True, BLUE)
        elif tutorialPhase == None or tutorialPhase == 8  or tutorialPhase == 10:
            ANDText = get_font3(15).render("AND Gate", True, BLACK)
        elif tutorialPhase != None:
            ANDText = get_font3(15).render("AND Gate", True, GREY)
        ANDrectText = ANDText.get_rect()
        ANDrectText.center = (200,155)
        
        NORGate = pygame.image.load("NORGate.png")
        NORrect = NORGate.get_rect()
        NORrect.center = (50,195)
        if activeGate == "NORGate":
            NORText = get_font3(15).render("NOR Gate", True, BLUE)
        elif tutorialPhase == None or tutorialPhase == 10:
            NORText = get_font3(15).render("NOR Gate", True, BLACK)
        elif tutorialPhase != None:
            NORText = get_font3(15).render("NOR Gate", True, GREY)
        NORrectText = NORText.get_rect()
        NORrectText.center = (50,230)
        
        NANDGate = pygame.image.load("NANDGate.png")
        NANDrect = NANDGate.get_rect()
        NANDrect.center = (125,195)
        if activeGate == "NANDGate":
            NANDText = get_font3(15).render("NAND Gate", True, BLUE)
        elif tutorialPhase == None or tutorialPhase == 10:
            NANDText = get_font3(15).render("NAND Gate", True, BLACK)
        elif tutorialPhase != None:
            NANDText = get_font3(15).render("NAND Gate", True, GREY)
        NANDrectText = NANDText.get_rect()
        NANDrectText.center = (125,230)
        
        XNORGate = pygame.image.load("XNORGate.png")
        XNORrect = ANDGate.get_rect()
        XNORrect.center = (200,195)
        if activeGate == "XNORGate":
            XNORText = get_font3(15).render("XNOR Gate", True, BLUE)
        elif tutorialPhase == None or tutorialPhase == 10:
            XNORText = get_font3(15).render("XNOR Gate", True, BLACK)
        elif tutorialPhase != None:
            XNORText = get_font3(15).render("XNOR Gate", True, GREY)
        XNORrectText = XNORText.get_rect()
        XNORrectText.center = (200,230)
        
        XORGate = pygame.image.load("XORGate.png")
        XORrect = XORGate.get_rect()
        XORrect.center = (50,270)
        if activeGate == "XORGate":
            XORText = get_font3(15).render("XOR Gate", True, BLUE)
        elif tutorialPhase == None or tutorialPhase == 10:
            XORText = get_font3(15).render("XOR Gate", True, BLACK)
        elif tutorialPhase != None:
            XORText = get_font3(15).render("XOR Gate", True, GREY)
        XORrectText = XORText.get_rect()
        XORrectText.center = (50,305)
        
        offSwitch = pygame.image.load("off_switch.jpg")
        switchRect = offSwitch.get_rect()
        switchRect.center = (45,365)
        if activeGate == "Switch_OFF":
            switchText = get_font3(15).render("Switch", True, BLUE)
        elif tutorialPhase == None or tutorialPhase == 1 or tutorialPhase == 6:
            switchText = get_font3(15).render("Switch", True, BLACK)
        elif tutorialPhase != None:
            switchText = get_font3(15).render("Switch", True, GREY)
        switchRectText = switchText.get_rect()
        switchRectText.center = (45,385)
        
        wireHorizontal = pygame.image.load("wire_horizontal.png")
        wireRect = wireHorizontal.get_rect()
        wireRect.center = (115,370)
        if activeGate == "wireHorizontal":
            wireText = get_font3(15).render("Wire", True, BLUE)
        elif tutorialPhase == None or tutorialPhase == 2 or tutorialPhase == 7:
            wireText = get_font3(15).render("Wire", True, BLACK)
        elif tutorialPhase != None:
            wireText = get_font3(15).render("Wire", True, GREY)
        wireRectText = wireText.get_rect()
        wireRectText.center = (115,405)
        
        clock = pygame.image.load("Clock_OFF.png")
        clockRect = clock.get_rect()
        clockRect.center = (190,370)
        if activeGate == "Clock":
            clockText = get_font3(15).render("Clock", True, BLUE)
        elif tutorialPhase != None:
            clockText = get_font3(15).render("Clock", True, GREY)
        else:
            clockText = get_font3(15).render("Clock", True, BLACK)
        clockTextRect = clockText.get_rect()
        clockTextRect.center = (190,405)    
        
        offLight = pygame.image.load("off_bulb.png")
        lightRect = offLight.get_rect()
        lightRect.center = (47,465)
        if activeGate == "Light_OFF":
            lightText = get_font3(15).render("Light Bulb", True, BLUE)
        elif tutorialPhase == None or tutorialPhase == 4 or tutorialPhase == 9:
            lightText = get_font3(15).render("Light Bulb", True, BLACK)
        elif tutorialPhase != None:
            lightText = get_font3(15).render("Light Bulb", True, GREY)
        lightRectText = lightText.get_rect()
        lightRectText.center = (47,500)
        
        DFlipFlop = pygame.image.load("DflipFlop.png")
        DFlipFlopRect = DFlipFlop.get_rect()
        DFlipFlopRect.center = (47,575)
        if activeGate == "DFlipFlop":
            DFlipFlopText = get_font3(15).render("Edge D Type", True, BLUE)
        elif tutorialPhase == None:
            DFlipFlopText = get_font3(15).render("Edge D Type", True, BLACK)
        else:
            DFlipFlopText = get_font3(15).render("Edge D Type", True, GREY)
        DFlipFlopTextRect = DFlipFlopText.get_rect()
        DFlipFlopTextRect.center = (47,610)
        
        #auto save switch and text display
        #if auto save is off, switch is off
        if autoSave == False:
            autoSaveSwitch = pygame.image.load("off_switch.jpg")
        #if auto save is on, switch is on
        else:
            autoSaveSwitch = pygame.image.load("on_switch.jpg")
        autoSaveSwitchRect = autoSaveSwitch.get_rect()
        autoSaveSwitchRect = (1050,30)
        #auto save unavailible
        if fileName == None or tutorialMode == True:
            autoSaveText = get_font3(15).render("Auto Save", True, GREY)
        #auto save off
        elif autoSave == False:
            autoSaveText = get_font3(15).render("Auto Save", True, BLACK)
        #auto save on
        elif autoSave == True:
            autoSaveText = get_font3(15).render("Auto Save", True, GREEN)
        autoSaveTextRect = autoSaveText.get_rect()
        autoSaveTextRect.center = (1150,42)
    
        #load wires, buttons, lights images
        
        toBeSquare = pygame.image.load("toBeSquare.png")
        
        wireIntersection = pygame.image.load("wire_intersection.jpg")
        wireIntersection_ON_BOTTOM = pygame.image.load("wire_intersection_ON_BOTTOM.jpg")
        wireIntersection_ON_TOP = pygame.image.load("wire_intersection_ON_TOP.jpg")
        wireIntersection_ON = pygame.image.load("wire_intersection_ON.jpg")
        
        wireHorizontal = pygame.image.load("wire_horizontal.png")
        wireHorizontal_ON = pygame.image.load("wire_horizontal_ON.png")
        
        wireBottomRight = pygame.image.load("wire_bottomRight.png")
        wireBottomRight_ON = pygame.image.load("wire_bottomRight_ON.png")
        
        wireBottomLeft = pygame.image.load("wire_bottomLeft.png")
        wireBottomLeft_ON = pygame.image.load("wire_bottomLeft_ON.png")
        
        wireTopRight = pygame.image.load("wire_topRight.png")
        wireTopRight_ON = pygame.image.load("wire_topRight_ON.png")
        
        wireTopLeft = pygame.image.load("wire_topLeft.png")
        wireTopLeft_ON = pygame.image.load("wire_topLeft_ON.png")
        
        wireVertical = pygame.image.load("wire_vertical.png")
        wireVertical_ON = pygame.image.load("wire_vertical_ON.png")
        
        wireSplitterDown = pygame.image.load("wire_splitter_down.png")
        wireSplitterDown_ON = pygame.image.load("wire_splitter_down_ON.png")
        
        wireSplitterUp = pygame.image.load("wire_splitter_up.png")
        wireSplitterUp_ON = pygame.image.load("wire_splitter_up_ON.png")
        
        wireSplitterRight = pygame.image.load("wire_splitter_right.png")
        wireSplitterRight_ON = pygame.image.load("wire_splitter_right_ON.png")
        
        wireSplitterLeft = pygame.image.load("wire_splitter_left.png")
        wireSplitterLeft_ON = pygame.image.load("wire_splitter_left_ON.png")
        
        wireCross = pygame.image.load("wire_cross.png")
        wireCross_ON_HORIZONTAL = pygame.image.load("wire_cross_ON_HORIZONTAL.png")
        wireCross_ON_VERTICAL = pygame.image.load("wire_cross_ON_VERTICAL.png")
        wireCross_ON = pygame.image.load("wire_cross_ON.png")
        
        onSwitch = pygame.image.load("on_switch.jpg")
        onLight = pygame.image.load("on_bulb.png")
        
        clock_OFF = pygame.image.load("Clock_OFF.png")
        clock_ON = pygame.image.load("Clock_ON.png")
        
        DFlipFlop = pygame.image.load("DFlipFlop.png")
        
        #draw grid
        for i in range(251,1280,49):
            pygame.draw.line(SCREEN,BLACK,(i,60),(i,720),2)
        for i in range(60,720,49):
            pygame.draw.line(SCREEN,BLACK,(60,i),(1280,i),2)
        pygame.draw.rect(SCREEN,BLUE, [0,0,1280,60])
        pygame.draw.rect(SCREEN,RED, [0,60,251,720])
        
        #drawing gates in array
        for i in range(0,len(logicArray)):
            for j in range(0,len(logicArray[i])):
                if logicArray[i][j] == None:
                    pass
                elif logicArray[i][j][0] == "ORGate":
                    #position in array used to determine which grid square to place in
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    #gate is drawn
                    DrawORrect = ORGate.get_rect()
                    DrawORrect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(ORGate, DrawORrect)
                elif logicArray[i][j][0] == "NOTGate":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawNOTrect = NOTGate.get_rect()
                    DrawNOTrect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(NOTGate, DrawNOTrect)
                elif logicArray[i][j][0] == "ANDGate":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawANDrect = ANDGate.get_rect()
                    DrawANDrect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(ANDGate, DrawANDrect)
                elif logicArray[i][j][0] == "NORGate":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawNORrect = NORGate.get_rect()
                    DrawNORrect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(NORGate, DrawNORrect)
                elif logicArray[i][j][0] == "NANDGate":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawNANDrect = NANDGate.get_rect()
                    DrawNANDrect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(NANDGate, DrawNANDrect)
                elif logicArray[i][j][0] == "XNORGate":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawXNORrect = XNORGate.get_rect()
                    DrawXNORrect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(XNORGate, DrawXNORrect)
                elif logicArray[i][j][0] == "XORGate":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawXORrect = XORGate.get_rect()
                    DrawXORrect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(XORGate, DrawXORrect)
                elif logicArray[i][j][0] == "Switch_OFF":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawOffSwitchRect = offSwitch.get_rect()
                    DrawOffSwitchRect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(offSwitch,DrawOffSwitchRect)
                elif logicArray[i][j][0] == "Switch_ON":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawOnSwitchRect = onSwitch.get_rect()
                    DrawOnSwitchRect.center = (XdrawPos, YdrawPos)
                    SCREEN.blit(onSwitch,DrawOnSwitchRect)
                elif logicArray[i][j][0] == "Light_OFF":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawOffLightRect = offLight.get_rect()
                    DrawOffLightRect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(offLight,DrawOffLightRect)
                elif logicArray[i][j][0] == "Light_ON":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawOnLightRect = onLight.get_rect()
                    DrawOnLightRect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(onLight,DrawOnLightRect)
                elif logicArray[i][j][0] == "wireIntersection":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireIntersectionRect = wireIntersection.get_rect()
                    DrawWireIntersectionRect.center = (XdrawPos,YdrawPos)
                    #depending on state of wire, different wire colours are used
                    if logicArray[i][j][1] == True and logicArray[i][j][2] == True:
                        SCREEN.blit(wireIntersection_ON,DrawWireIntersectionRect)
                    elif logicArray[i][j][1] == True:
                        SCREEN.blit(wireIntersection_ON_TOP,DrawWireIntersectionRect)
                    elif logicArray[i][j][2] == True:
                        SCREEN.blit(wireIntersection_ON_BOTTOM,DrawWireIntersectionRect)
                    else:
                        SCREEN.blit(wireIntersection,DrawWireIntersectionRect)
                elif logicArray[i][j][0] == "wireHorizontal":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireHorizontalRect = wireHorizontal.get_rect()
                    DrawWireHorizontalRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True:
                        SCREEN.blit(wireHorizontal_ON,DrawWireHorizontalRect)
                    else:
                        SCREEN.blit(wireHorizontal, DrawWireHorizontalRect)
                elif logicArray[i][j][0] == "wireVertical":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireVerticalRect = wireVertical.get_rect()
                    DrawWireVerticalRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True:
                        SCREEN.blit(wireVertical_ON,DrawWireVerticalRect)
                    else:
                        SCREEN.blit(wireVertical, DrawWireVerticalRect)
                elif logicArray[i][j][0] == "wireBottomRight":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireBottomRightRect = wireBottomRight.get_rect()
                    DrawWireBottomRightRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True:
                        SCREEN.blit(wireBottomRight_ON,DrawWireBottomRightRect)
                    else:
                        SCREEN.blit(wireBottomRight, DrawWireBottomRightRect)
                elif logicArray[i][j][0] == "wireBottomLeft":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireBottomLeftRect = wireBottomLeft.get_rect()
                    DrawWireBottomLeftRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True:
                        SCREEN.blit(wireBottomLeft_ON,DrawWireBottomLeftRect)
                    else:
                        SCREEN.blit(wireBottomLeft, DrawWireBottomLeftRect)
                elif logicArray[i][j][0] == "wireTopRight":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireTopRightRect = wireTopRight.get_rect()
                    DrawWireTopRightRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True:
                        SCREEN.blit(wireTopRight_ON,DrawWireTopRightRect)
                    else:
                        SCREEN.blit(wireTopRight, DrawWireTopRightRect)
                elif logicArray[i][j][0] == "wireTopLeft":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireTopLeftRect = wireBottomRight.get_rect()
                    DrawWireTopLeftRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True:
                        SCREEN.blit(wireTopLeft_ON,DrawWireTopLeftRect)
                    else:
                        SCREEN.blit(wireTopLeft, DrawWireTopLeftRect)
                elif logicArray[i][j][0] == "wireSplitterDown":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireSplitterDownRect = wireSplitterDown.get_rect()
                    DrawWireSplitterDownRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True:
                        SCREEN.blit(wireSplitterDown_ON,DrawWireSplitterDownRect)
                    else:
                        SCREEN.blit(wireSplitterDown, DrawWireSplitterDownRect)
                elif logicArray[i][j][0] == "wireSplitterUp":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireSplitterUpRect = wireSplitterUp.get_rect()
                    DrawWireSplitterUpRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True:
                        SCREEN.blit(wireSplitterUp_ON,DrawWireSplitterUpRect)
                    else:
                        SCREEN.blit(wireSplitterUp, DrawWireSplitterUpRect)
                elif logicArray[i][j][0] == "wireSplitterRight":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireSplitterRightRect = wireSplitterRight.get_rect()
                    DrawWireSplitterRightRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True:
                        SCREEN.blit(wireSplitterRight_ON,DrawWireSplitterRightRect)
                    else:
                        SCREEN.blit(wireSplitterRight, DrawWireSplitterRightRect)
                elif logicArray[i][j][0] == "wireSplitterLeft":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireSplitterLeftRect = wireSplitterLeft.get_rect()
                    DrawWireSplitterLeftRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True:
                        SCREEN.blit(wireSplitterLeft_ON,DrawWireSplitterLeftRect)
                    else:
                        SCREEN.blit(wireSplitterLeft, DrawWireSplitterLeftRect)
                elif logicArray[i][j][0] == "wireCross":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawWireCrossRect = wireSplitterUp.get_rect()
                    DrawWireCrossRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True and logicArray[i][j][2] == True:
                        SCREEN.blit(wireCross_ON,DrawWireCrossRect)
                    elif logicArray[i][j][1] == True:
                        SCREEN.blit(wireCross_ON_VERTICAL,DrawWireCrossRect)
                    elif logicArray[i][j][2] == True:
                        SCREEN.blit(wireCross_ON_HORIZONTAL,DrawWireCrossRect)
                    else:
                        SCREEN.blit(wireCross, DrawWireCrossRect)
                elif logicArray[i][j][0] == "Clock":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawClockRect = clock_OFF.get_rect()
                    DrawClockRect.center = (XdrawPos,YdrawPos)
                    if logicArray[i][j][1] == True: 
                        SCREEN.blit(clock_ON,DrawClockRect)
                    else:
                        SCREEN.blit(clock_OFF,DrawClockRect)
                elif logicArray[i][j][0] == "DFlipFlop":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    DrawDFlipFlopRect = DFlipFlop.get_rect()
                    DrawDFlipFlopRect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(DFlipFlop,DrawDFlipFlopRect)
                #used for tutorial mode
                elif logicArray[i][j][0] == "wireToBe" or logicArray[i][j][0] == "NOTGateToBe" or logicArray[i][j][0] == "lightToBe" or logicArray[i][j][0] == "switchToBe" or logicArray[i][j][0] == "gateToBe":
                    XdrawPos = (j+1)*49 + 227
                    YdrawPos = (i+1)*49 + 36
                    drawToBeSquareRect = toBeSquare.get_rect()
                    drawToBeSquareRect.center = (XdrawPos,YdrawPos)
                    SCREEN.blit(toBeSquare,drawToBeSquareRect)
                        
                    
        
        #button creation
        if tutorialPhase == None:
            logicInterfaceSave = Button(pos=(55,30), text_input="Save", font=get_font2(25), base_color=BLACK, hovering_color=GREY)
            logicInterfaceSaveAs = Button(pos=(145,30), text_input="Save As", font=get_font2(25), base_color=BLACK, hovering_color=GREY)
            logicInterfaceLoad = Button(pos=(235,30), text_input="Load", font=get_font2(25), base_color=BLACK, hovering_color=GREY)
            #undo button changes colour based on stack being empty
            if undoStack == []:
                logicInterfaceUndo = Button(pos=(315,30), text_input="Undo", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            else:
                logicInterfaceUndo = Button(pos=(315,30), text_input="Undo", font=get_font2(25), base_color=BLACK, hovering_color=GREY)
            #undo button changes colour based on stack being empty
            if redoStack == []:
                logicInterfaceRedo = Button(pos=(390,30), text_input="Redo", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            else:
                logicInterfaceRedo = Button(pos=(390,30), text_input="Redo", font=get_font2(25), base_color=BLACK, hovering_color=GREY)
            logicInterfaceTruthTable = Button(pos=(500,30), text_input="Truth Table", font=get_font2(25), base_color=BLACK, hovering_color=GREY)
            #delete button changes colour based on delete function being active
            if activeGate != "Delete":
                logicInterfaceDelete = Button(pos=(625,30), text_input="Delete", font=get_font2(25), base_color=BLACK, hovering_color=GREY)
            logicInterfaceClear = Button(pos=(715,30), text_input="Clear", font=get_font2(25), base_color=BLACK, hovering_color=GREY)
            logicInterfaceNew = Button(pos=(795,30), text_input="New", font=get_font2(25), base_color=BLACK, hovering_color=GREY)
            logicInterfaceMainMenu = Button(pos=(905,30), text_input="Main Menu", font=get_font2(25), base_color=BLACK, hovering_color=GREY)
        #all options are disabled in tutorial
        elif tutorialPhase == 1:
            logicInterfaceSave = Button(pos=(55,30), text_input="Save", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            logicInterfaceSaveAs = Button(pos=(145,30), text_input="Save As", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            logicInterfaceLoad = Button(pos=(235,30), text_input="Load", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            logicInterfaceUndo = Button(pos=(315,30), text_input="Undo", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            logicInterfaceRedo = Button(pos=(390,30), text_input="Redo", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            logicInterfaceTruthTable = Button(pos=(500,30), text_input="Truth Table", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            logicInterfaceDelete = Button(pos=(625,30), text_input="Delete", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            logicInterfaceClear = Button(pos=(715,30), text_input="Clear", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            logicInterfaceNew = Button(pos=(795,30), text_input="New", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            logicInterfaceMainMenu = Button(pos=(905,30), text_input="Main Menu", font=get_font2(25), base_color=GREY, hovering_color=GREY)
            logicInterfaceTutorialBack = Button(pos=(110,680), text_input="Back", font=get_font2(25), base_color=BLACK, hovering_color=GREY) 
        elif tutorialPhase == 4 or tutorialPhase == 10:
            logicInterfaceTutorialNext = Button(pos=(200,680), text_input="Next", font=get_font2(25), base_color=BLACK, hovering_color=GREY)
        
        #logic gate menu text creation
        logicGateText = get_font3(20).render("Logic Gates", True, BLACK)
        logicGateRectText = logicGateText.get_rect()
        logicGateRectText.center = (70,80)
        SCREEN.blit(logicGateText, logicGateRectText)
        
        inputText = get_font3(20).render("Inputs", True, BLACK)
        inputTextRect = inputText.get_rect()
        inputTextRect.center = (45,330)
        SCREEN.blit(inputText, inputTextRect)
        
        outputText = get_font3(20).render("Outputs", True, BLACK)
        outputTextRect = outputText.get_rect()
        outputTextRect.center = (50, 425)
        SCREEN.blit(outputText, outputTextRect)
        
        flipFlopText = get_font3(20).render("Flip Flops", True, BLACK)
        flipFlopTextRect = outputText.get_rect()
        flipFlopTextRect.center = (45, 530)
        SCREEN.blit(flipFlopText, flipFlopTextRect)
        
        #document name text
        if tutorialPhase != None:
            fileNameText = get_font3(15).render("Tutorial", True, BLACK)
        elif fileName == None:
            fileNameText = get_font3(15).render("New Document", True, BLACK)
        else:
            fileNameText = get_font3(15).render(fileName, True, BLACK)
        fileNameTextRect = fileNameText.get_rect()
        fileNameTextRect.center = (1100,10)
        SCREEN.blit(fileNameText, fileNameTextRect)
        
        #block transfer of images and text
        SCREEN.blit(ORGate, ORrect)
        SCREEN.blit(ORText, ORrectText)
        
        SCREEN.blit(NOTGate, NOTrect)
        SCREEN.blit(NOTText, NOTrectText)
        
        SCREEN.blit(ANDGate, ANDrect)
        SCREEN.blit(ANDText, ANDrectText)
        
        SCREEN.blit(NORGate, NORrect)
        SCREEN.blit(NORText, NORrectText)
        
        SCREEN.blit(NANDGate, NANDrect)
        SCREEN.blit(NANDText, NANDrectText)
        
        SCREEN.blit(XNORGate, XNORrect)
        SCREEN.blit(XNORText, XNORrectText)
        
        SCREEN.blit(XORGate, XORrect)
        SCREEN.blit(XORText, XORrectText)
        
        SCREEN.blit(offSwitch, switchRect)
        SCREEN.blit(switchText, switchRectText)
        
        SCREEN.blit(offLight, lightRect)
        SCREEN.blit(lightText, lightRectText)
        
        SCREEN.blit(wireHorizontal, wireRect)
        SCREEN.blit(wireText, wireRectText)
        
        SCREEN.blit(clock, clockRect)
        SCREEN.blit(clockText, clockTextRect)
        
        SCREEN.blit(DFlipFlop, DFlipFlopRect)
        SCREEN.blit(DFlipFlopText, DFlipFlopTextRect)
        
        SCREEN.blit(autoSaveSwitch, autoSaveSwitchRect)
        SCREEN.blit(autoSaveText, autoSaveTextRect)
        
        #main logic
        #on/off subroutines
        def turnOnVerticalUp(i,j):
            startPoint = i-1
            for k in range(startPoint,-1,-1):
                if logicArray[k][j] == [None]:
                    break
                elif logicArray[k][j][0] == "wireVertical":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Up"
                elif logicArray[k][j][0] == "wireTopLeft":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Right"
                    turnOnHorizontalRight(k,j)
                elif logicArray[k][j][0] == "wireTopRight":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Left"
                    turnOnHorizontalLeft(k,j)
                elif logicArray[k][j][0] == "wireIntersection":
                    logicArray[k][j][2] = True
                    break
                elif logicArray[k][j][0] == "wireCross":
                    logicArray[k][j][1] = True
                elif logicArray[k][j][0] == "wireSplitterLeft":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Up"
                    turnOnVerticalUp(k,j)
                    turnOnHorizontalLeft(k,j)
                elif logicArray[k][j][0] == "wireSplitterRight":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Up"
                    turnOnVerticalUp(k,j)
                    turnOnHorizontalRight(k,j)
                elif logicArray[k][j][0] == "wireSplitterDown":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Up"
                    turnOnHorizontalRight(i,k)
                    turnOnVerticalDown(i,k)
                    
        def turnOnVerticalDown(i,j):
            startPoint = i+1
            for k in range(startPoint,13):
                if logicArray[k][j] == [None]:
                    break
                elif logicArray[k][j][0] == "wireVertical":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Down"
                elif logicArray[k][j][0] == "wireBottomLeft":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Right"
                    turnOnHorizontalRight(k,j)
                elif logicArray[k][j][0] == "wireBottomRight":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Left"
                    turnOnHorizontalLeft(k,j)
                elif logicArray[k][j][0] == "wireIntersection":
                    logicArray[k][j][1] = True
                    break
                elif logicArray[k][j][0] == "wireCross":
                    logicArray[k][j][1] = True
                elif logicArray[k][j][0] == "wireSplitterLeft":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Down"
                    turnOnVerticalDown(k,j)
                    turnOnHorizontalLeft(k,j)
                elif logicArray[k][j][0] == "wireSplitterRight":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Down"
                    turnOnVerticalDown(k,j)
                    turnOnHorizontalRight(k,j)
                elif logicArray[k][j][1] == "wireSplitterUp":
                    logicArray[k][j][1] = True
                    logicArray[k][j][2] = "Down"
                    turnOnHorizontalRight(k,j)
                    turnOnHorizontalLeft(k,j)
                    
        def turnOffVerticalUp(i,j):
            startPoint = i-1
            for k in range(startPoint,-1,-1):
                if logicArray[k][j] == [None]:
                    break
                elif logicArray[k][j][0] == "wireVertical":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                elif logicArray[k][j][0] == "wireTopLeft":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                    turnOffHorizontalRight(k,j)
                elif logicArray[k][j][0] == "wireTopRight":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                    turnOffHorizontalLeft(k,j)
                elif logicArray[k][j][0] == "wireIntersection":
                    logicArray[k][j][2] = False
                    break
                elif logicArray[k][j][0] == "wireCross":
                    logicArray[k][j][1] = False
                elif logicArray[k][j][0] == "wireSplitterLeft":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                    turnOffVerticalUp(k,j)
                    turnOffHorizontalLeft(k,j)
                elif logicArray[k][j][0] == "wireSplitterRight":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                    turnOffVerticalUp(k,j)
                    turnOffHorizontalRight(k,j)
                elif logicArray[k][j][0] == "wireSplitterDown":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                    turnOffHorizontalRight(i,k)
                    turnOffVerticalDown(i,k)
                    
        def turnOffVerticalDown(i,j):
            startPoint = i+1
            for k in range(startPoint,13):
                if logicArray[k][j] == [None]:
                    break
                elif logicArray[k][j][0] == "wireVertical":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                elif logicArray[k][j][0] == "wireBottomLeft":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                    turnOffHorizontalRight(k,j)
                elif logicArray[k][j][0] == "wireBottomRight":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                    turnOffHorizontalLeft(k,j)
                elif logicArray[k][j][0] == "wireIntersection":
                    logicArray[k][j][1] = False
                    break
                elif logicArray[k][j][0] == "wireCross":
                    logicArray[k][j][1] = False
                elif logicArray[k][j][0] == "wireSplitterLeft":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                    turnOffVerticalUp(k,j)
                    turnOffHorizontalLeft(k,j)
                elif logicArray[k][j][0] == "wireSplitterRight":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                    turnOffVerticalUp(k,j)
                    turnOnHorizontalRight(k,j)
                elif logicArray[k][j][0] == "wireSplitterUp":
                    logicArray[k][j][1] = False
                    logicArray[k][j][2] = None
                    turnOffHorizontalRight(k,j)
                    turnOffHorizontalLeft(k,j)
        
        #i refers to vertical position, j refers to horizontal position
        def turnOnHorizontalRight(i,j):
            startPoint = j+1
            #entire row is searched
            for k in range(startPoint,21):
                #when blank square is found, subroutine ends
                if logicArray[i][k] == [None]:
                    break
                #state of wire is changed, direction of power flow is defined as "right"
                elif logicArray[i][k][0] == "wireHorizontal":
                    logicArray[i][k][1] = True
                    logicArray[i][k][2] = "Right"
                elif logicArray[i][k][0] == "wireBottomRight":
                    logicArray[i][k][1] = True
                    logicArray[i][k][2] = "Up"
                    #wire direction changes, so vertical up subroutine is called
                    turnOnVerticalUp(i,k)
                elif logicArray[i][k][0] == "wireTopRight":
                    logicArray[i][k][1] = True
                    logicArray[i][k][2] = "Down"
                    #wire direction changes so vertical down subroutine is called
                    turnOnVerticalDown(i,k)
                elif logicArray[i][k][0] == "wireSplitterDown":
                    logicArray[i][k][1] = True
                    logicArray[i][k][2] = "Right"
                    #power is splitm so both vertical down and horizontal right subroutines are called
                    turnOnVerticalDown(i,k)
                    turnOnHorizontalRight(i,k)
                elif logicArray[i][k][0] == "wireSplitterUp":
                    logicArray[i][k][1] = True
                    logicArray[i][k][2] = "Right"
                    #power is split, so both vertical up and horizontal right subroutines are called
                    turnOnVerticalUp(i,k)
                    turnOnHorizontalRight(i,k)
                elif logicArray[i][k][0] == "wireSplitterLeft":
                    logicArray[i][k][1] = True
                    logicArray[i][k][2] = "Right"
                    #power is split, so both vertical up and vertical down subroutines are called
                    turnOnVerticalDown(i,k)
                    turnOnVerticalUp(i,k)
                elif logicArray[i][k][0] == "wireCross":
                    #wire cross functions in the same way as a horizontal wire, but with a different index
                    logicArray[i][k][2] = True
                    
        def turnOnHorizontalLeft(i,j):
            startPoint = j-1
            for k in range(startPoint,-1,-1):
                if logicArray[i][k] == [None]:
                    break
                elif logicArray[i][k][0] == "wireHorizontal":
                    logicArray[i][k][1] = True
                    logicArray[i][k][2] = "Left"
                elif logicArray[i][k][0] == "wireBottomLeft":
                    logicArray[i][k][1] = True
                    turnOnVerticalUp(i,k)
                    logicArray[i][k][2] = "Up"
                elif logicArray[i][k][0] == "wireTopLeft":
                    logicArray[i][k][1] = True 
                    turnOnVerticalDown(i,k)
                    logicArray[i][k][2] = "Down"
                elif logicArray[i][k][0] == "wireSplitterDown":
                    logicArray[i][k][1] = True
                    logicArray[i][k][2] = "Left"
                    turnOnVerticalDown(i,k)
                    turnOnHorizontalLeft(i,k)
                elif logicArray[i][k][0] == "wireSplitterUp":
                    logicArray[i][k][1] = True
                    logicArray[i][k][2] = "Left"
                    turnOnVerticalUp(i,k)
                    turnOnHorizontalRight(i,k)
                elif logicArray[i][k][0] == "wireSplitterRight":
                    logicArray[i][k][1] = True
                    logicArray[i][k][2] = "Left"
                    turnOnVerticalDown(i,k)
                    turnOnVerticalUp(i,k)
                elif logicArray[i][k][0] == "wireCross":
                    logicArray[i][k][2] = True
                    
        #i refers to vertical position, j refers to horizontal position
        def turnOffHorizontalRight(i,j):
            startPoint = j+1
            #entire row is searched
            for k in range(startPoint,21):
                #when blank square is found, subroutine ends 
                if logicArray[i][k] == [None]:
                    break
                elif logicArray[i][k][0] == "wireHorizontal":
                    #state of wire is changed to off, direction of power flow is reset 
                    logicArray[i][k][2] = None
                    logicArray[i][k][1] = False
                elif logicArray[i][k][0] == "wireBottomRight":
                    logicArray[i][k][2] = None
                    logicArray[i][k][1] = False
                    #wire direction changes, so vertical subroutine is called
                    turnOffVerticalUp(i, k)
                elif logicArray[i][k][0] == "wireTopRight":
                    logicArray[i][k][2] = None
                    logicArray[i][k][1] = False
                    #wire direction changes, so vertical down subroutine is called
                    turnOffVerticalDown(i,k)
                elif logicArray[i][k][0] == "wireSplitterDown":
                    logicArray[i][k][2] = None
                    logicArray[i][k][1] = False
                    #power is split, both horizontal right and vertical down subroutines are called
                    turnOffVerticalDown(i,k)
                    turnOffHorizontalRight(i,k)
                elif logicArray[i][k][0] == "wireSplitterUp":
                    logicArray[i][k][2] = None
                    logicArray[i][k][1] = False
                    #power is split, both horizontal right and vertical up subroutines are called
                    turnOffVerticalUp(i,k)
                    turnOffHorizontalRight(i,k)
                elif logicArray[i][k][0] == "wireSplitterLeft":
                    logicArray[i][k][1] = False
                    logicArray[i][k][2] = None
                    #power is split, both vertical up and down subroutines are called
                    turnOffVerticalDown(i,k)
                    turnOffVerticalUp(i,k)
                elif logicArray[i][k][0] == "wireCross":
                    #wire cross functions in the same way as a horizontal wire but with a different index
                    logicArray[i][k][2] = False
                    
        def turnOffHorizontalLeft(i,j):
            startPoint = j-1
            for k in range(startPoint,-1,-1):
                if logicArray[i][k] == [None]:
                    break
                elif logicArray[i][k][0] == "wireHorizontal":
                    logicArray[i][k][1] = False
                    logicArray[i][k][2] = None
                elif logicArray[i][k][0] == "wireBottomLeft":
                    logicArray[i][k][1] = False
                    logicArray[i][k][2] = None
                    turnOffVerticalUp(i,k)
                elif logicArray[i][k][0] == "wireTopLeft":
                    logicArray[i][k][1] = False
                    logicArray[i][k][2] = None
                    turnOffVerticalDown(i,k)
                elif logicArray[i][k][0] == "wireSplitterDown":
                    logicArray[i][k][1] = False
                    logicArray[i][k][2] = None
                    turnOffVerticalDown(i,k)
                    turnOffHorizontalLeft(i,k)
                elif logicArray[i][k][0] == "wireSplitterUp":
                    logicArray[i][k][1] = False
                    logicArray[i][k][2] = None
                    turnOffVerticalUp(i,k)
                    turnOffHorizontalRight(i,k)
                elif logicArray[i][k][0] == "wireSplitterRight":
                    logicArray[i][k][1] = False
                    logicArray[i][k][2] = None
                    turnOnVerticalDown(i,k)
                    turnOnVerticalUp(i,k)
                elif logicArray[i][k][0] == "wireCross":
                    logicArray[i][k][2] = False
        
        #auto save logic
        if autoSave == True:
            # if time passed since last save is 30 seconds
            if time.time() - autoSaveStartTime >= 30:
                print("Auto Saving")
                #time reset
                autoSaveStartTime = time.time()
                if fileName is not None:
                    logicFile = open(fileName, "wb")
                    #file saved
                    pickle.dump(logicArray, logicFile)
                    logicFile.close()
        
        #main loop
        def mainLoop():
            #global variables
            global lastCountChange
            global count
            global finalTime
            global clockPulse
            global lastChange
            #clock pulses
            if time.time() > finalTime:
                if clockPulse == False:
                    clockPulse = True
                else:
                    clockPulse = False
                lastChange = finalTime
                finalTime = time.time() + 1
            for i in range(0,len(logicArray)):
                for j in range(0,len(logicArray[i])):
                    #algortihm passes over empty squares
                    if logicArray[i][j][0] == None:
                        pass
                    #turning a switch on causes corresponding elements in all directions to turn on
                    elif logicArray[i][j][0] == "Switch_ON":
                        turnOnHorizontalRight(i,j)
                        turnOnHorizontalLeft(i,j)
                        turnOnVerticalUp(i,j)
                        turnOnVerticalDown(i,j)
                    #turning a switch off causes corresponding elements in all directions to turn off
                    elif logicArray[i][j][0] == "Switch_OFF":
                        turnOffHorizontalRight(i,j)
                        turnOffHorizontalLeft(i,j)
                        turnOffVerticalUp(i,j)
                        turnOffVerticalDown(i,j)
                    elif logicArray[i][j][0] == "Clock":
                        #clock changes state based on pulse
                        if clockPulse == True:
                            logicArray[i][j][1] = True
                            turnOnHorizontalRight(i,j)
                            turnOnHorizontalLeft(i,j)
                            turnOnVerticalDown(i,j)
                            turnOnVerticalUp(i,j)
                        else:
                            logicArray[i][j][1] = False
                            turnOffHorizontalRight(i,j)
                            turnOffHorizontalLeft(i,j)
                            turnOffVerticalDown(i,j)
                            turnOffVerticalUp(i,j)
                    elif logicArray[i][j][0] == "NOTGate":
                        #NOT operation
                        if logicArray[i][j-1][0] == None:
                            pass
                        elif logicArray[i][j-1][1] == True:
                            logicArray[i][j] = ["NOTGate", False]
                            turnOffHorizontalRight(i,j)
                        else:
                            logicArray[i][j] = ["NOTGate", True]
                            turnOnHorizontalRight(i,j)
                    elif logicArray[i][j][0] == "ORGate":
                        #OR operation
                        if logicArray[i][j-1][0] == "wireIntersection" and logicArray[i][j-1][1] == True or logicArray[i][j-1][2] == True:
                            logicArray[i][j][1] = True
                            turnOnHorizontalRight(i,j)
                        else:
                            logicArray[i][j][1] = False
                            turnOffHorizontalRight(i,j)
                    elif logicArray[i][j][0] == "ANDGate":
                        #AND operation
                        if logicArray[i][j-1][0] == "wireIntersection" and logicArray[i][j-1][1] == True and logicArray[i][j-1][2] == True:
                            logicArray[i][j][1] = True
                            turnOnHorizontalRight(i,j)
                        else:
                            logicArray[i][j][1] = False
                            turnOffHorizontalRight(i,j)
                    elif logicArray[i][j][0] == "NORGate":
                        #NOR operation
                        if logicArray[i][j-1][0] == "wireIntersection" and logicArray[i][j-1][1] == True or logicArray[i][j-1][2] == True:
                            logicArray[i][j][1] = False
                            turnOffHorizontalRight(i,j)
                        else:
                            logicArray[i][j][1] = True
                            turnOnHorizontalRight(i,j)
                    elif logicArray[i][j][0] == "NANDGate":
                        #NAND operation
                        if logicArray[i][j-1][0] == "wireIntersection" and logicArray[i][j-1][1] == True and logicArray[i][j-1][2] == True:
                            logicArray[i][j][1] = False
                            turnOffHorizontalRight(i,j)
                        else:
                            logicArray[i][j][1] = True
                            turnOnHorizontalRight(i,j)
                    elif logicArray[i][j][0] == "XNORGate":
                        #XNOR operation
                        if logicArray[i][j-1][0] == "wireIntersection" and logicArray[i][j-1][1] == True and logicArray[i][j-1][2] == True:
                            logicArray[i][j][1] = True
                        elif logicArray[i][j-1][0] == "wireIntersection" and logicArray[i][j-1][1] == True or logicArray[i][j-1][2] == True:
                            logicArray[i][j][1] = False
                        else:
                            logicArray[i][j][1] = True
                        if logicArray[i][j][1] == True:
                            turnOnHorizontalRight(i,j)
                        else:
                            turnOffHorizontalRight(i,j)
                    elif logicArray[i][j][0] == "XORGate":
                        #XOR operation
                        if logicArray[i][j-1][0] == "wireIntersection" and logicArray[i][j-1][1] == True and logicArray[i][j-1][2] == True:
                            logicArray[i][j][1] = False
                        elif logicArray[i][j-1][0] == "wireIntersection" and logicArray[i][j-1][1] == True or logicArray[i][j-1][2] == True:
                            logicArray[i][j][1] = True
                        else:
                            logicArray[i][j][1] = False
                        if logicArray[i][j][1] == True:
                            turnOnHorizontalRight(i,j)
                        else:
                            turnOffHorizontalRight(i,j)
                    elif logicArray[i][j][0] == "DFlipFlop":
                        #state of D flip flop changes based on last switch state change and time since last clock pulse
                        if time.time() < lastChange + 0.5 and count == lastCountChange + 1:
                            if logicArray[i][j-1][1] == True:
                                if logicArray[i][j-1][2] == True:
                                    logicArray[i][j][1] = False
                                    turnOffHorizontalRight(i,j)
                                elif logicArray[i][j-1][2] == False:
                                    logicArray[i][j][1] = True
                                    turnOnHorizontalRight(i,j)
                        elif logicArray[i][j][1] == True:
                            turnOnHorizontalRight(i,j)
                        elif logicArray[i][j][1] == True:
                            turnOffHorizontalRight(i,j)
                    #light turns off if wire to the left is off
                    elif logicArray[i][j][0] == "Light_OFF":
                        if logicArray[i][j-1][0] == None:
                            logicArray[i][j] = ["Light_OFF", False]
                        elif logicArray[i][j-1][1] == True:
                            logicArray[i][j] = ["Light_ON", True]
                    #wire turns on if wire to the left is on
                    elif logicArray[i][j][0] == "Light_ON":
                        if logicArray[i][j-1][0] == None:
                            pass
                        elif logicArray[i][j-1][1] == False:
                            logicArray[i][j] = ["Light_OFF", False]
                    elif logicArray[i][j][0] == "wireHorizontal":
                        #change to wire splitter up
                        if (logicArray[i-1][j][0] == "wireHorizontal" or logicArray[i-1][j][0] == "wireVertical") and (logicArray[i][j-1][0] == "wireHorizontal" or logicArray[i][j-1][0] == "wireTopLeft") and (logicArray[i][j+1][0] == "wireHorizontal" or logicArray[i][j+1][0] == "wireBottomRight"):
                            logicArray[i][j][0] = "wireSplitterUp"
                        #change to bottom right
                        elif (logicArray[i-1][j][0] == "wireHorizontal" or logicArray[i-1][j][0] == "wireIntersection") and (logicArray[i][j-1][0] == "wireHorizontal" or logicArray[i][j-1][0] == "Switch_ON" or logicArray[i][j-1][0] == "Switch_OFF"):
                            logicArray[i][j][0] = "wireBottomRight"
                            if logicArray[i-1][j][0] == "wireHorizontal":
                                logicArray[i][j][0] = "wireVertical"
                        #change to top right
                        elif (logicArray[i+1][j][0] == "wireHorizontal" or logicArray[i+1][j][0] == "wireIntersection") and logicArray[i][j-1][0] == "wireHorizontal":
                            logicArray[i][j][0] = "wireTopRight"
                            if logicArray[i+1][j][0] == "wireHorizontal":
                                logicArray[i+1][j][0] = "wireVertical"
                        #change to vertical
                        elif logicArray[i+1][j][0] == "wireVertical" or logicArray[i+1][j][0] == "wireIntersection" or logicArray[i+1][j][0] == "wireBottomRight" or logicArray[i+1][j][0] == "wireSplitterUp" or logicArray[i+1][j][0] == "Switch_OFF" or logicArray[i+1][j][0] == "Switch_ON" or logicArray[i+1][j][0] == "Clock":
                            logicArray[i][j][0] = "wireVertical"
                        elif logicArray[i-1][j][0] == "wireVertical" or logicArray[i-1][j][0] == "wireIntersection" or logicArray[i-1][j][0] == "wireSplitterDown" or logicArray[i-1][j][0] == "wireSplitterLeft" or logicArray[i-1][j][0] == "wireSplitterRight" or logicArray[i-1][j][0] == "wireTopRight" or logicArray[i-1][j][0] == "Switch_OFF" or logicArray[i-1][j][0] == "Switch_ON" or logicArray[i-1][j][0] == "Clock":
                            logicArray[i][j][0] = "wireVertical"
                        elif logicArray[i+1][j][0] == "wireHorizontal":
                            logicArray[i+1][j][0] = "wireVertical"
                            logicArray[i][j][0] = "wireVertical"
                        elif logicArray[i-1][j][0] == "wireHorizontal":
                            logicArray[i-1][j][0] = "wireVertical"
                            logicArray[i][j][0] = "wireVertical"
                    elif logicArray[i][j][0] == "wireVertical":
                        #change to wire splitter left
                        if (logicArray[i-1][j][0] == "wireVertical" or logicArray[i-1][j][0] == "wireTopLeft") and (logicArray[i+1][j][0] == "wireVertical" or logicArray[i+1][j][0] == "wireBottomLeft") and logicArray[i][j-1][0] == "wireHorizontal":
                            logicArray[i][j][0] = "wireSplitterLeft"
                        #change to wire splitter right
                        elif (logicArray[i-1][j][0] == "wireVertical" or logicArray[i-1][j][0] == "wireTopRight") and (logicArray[i+1][j][0] == "wireVertical" or logicArray[i+1][j][0] == "wireBottomRight") and logicArray[i][j+1][0] == "wireHorizontal":
                            logicArray[i][j][0] = "wireSplitterRight"
                        #change to top left
                        elif logicArray[i][j-1][0] != "wireHorizontal" and (logicArray[i][j+1][0] == "wireHorizontal" or logicArray[i][j+1][0] == "wireBottomRight") and (logicArray[i+1][j][0] == "wireVertical" or logicArray[i+1][j][0] == "wireBottomRight"):
                            logicArray[i][j][0] = "wireTopLeft"
                        #change to top right
                        elif (logicArray[i+1][j][0] == "wireVertical" or logicArray[i+1][j][0] == "wireBottomLeft" or logicArray[i+1][j][0] == "wireIntersection") and (logicArray[i][j-1][0] == "wireHorizontal" or logicArray[i][j-1][0] == "wireBottomLeft" or logicArray[i][j-1][0] == "Switch_ON" or logicArray[i][j-1][0] == "Switch_OFF" or logicArray[i][j-1][0] == "Clock"):
                            logicArray[i][j][0] = "wireTopRight"
                        #change to bottom left
                        elif (logicArray[i-1][j][0] == "wireVertical" or logicArray[i-1][j][0] == "wireTopRight") and (logicArray[i][j+1][0] == "wireHorizontal" or logicArray[i][j+1][0] == "wireTopRight"):
                            logicArray[i][j][0] = "wireBottomLeft"
                        #change to bottom right
                        elif (logicArray[i-1][j][0] == "wireVertical" or logicArray[i-1][j][0] == "wireIntersection" or logicArray[i-1][j][0] == "wireTopLeft" or logicArray[i-1][j][0] == "wireSplitterDown") and (logicArray[i][j-1][0] == "wireHorizontal" or logicArray[i][j-1][0] == "wireTopLeft" or logicArray[i][j-1][0] == "Switch_ON" or logicArray[i][j-1][0] == "Switch_OFF" or logicArray[i][j-1][0] == "Clock"):
                            logicArray[i][j][0] = "wireBottomRight"
                    #top left change
                    elif logicArray[i][j][0] == "wireTopLeft":
                        if logicArray[i+1][j][0] == None and (logicArray[i][j+1][0] == "wireHorizontal" or logicArray[i][j+1][0] == "wireBottomRight"):
                            logicArray[i][j][0] = "wireHorizontal"
                        elif (logicArray[i+1][j][0] == "wireVertical" or logicArray[i+1][j][0] == "wireBottomRight") and logicArray[i][j+1][0] == None:
                            logicArray[i][j][0] = "wireVertical"
                        elif logicArray[i][j-1][0] == "wireHorizontal" and logicArray[i][j+1][0] == "wireHorizontal":
                            logicArray[i][j][0] = "wireSplitterDown"
                        elif logicArray[i-1][j][0] == "wireHorizontal":
                            logicArray[i][j][0] = "wireSplitterRight"
                            logicArray[i-1][j][0] = "wireVertical"
                    #top right change
                    elif logicArray[i][j][0] == "wireTopRight":
                        if (logicArray[i+1][j][0] == "wireVertical" or logicArray[i+1][j][0] == "wireVertical") and (logicArray[i][j-1][0] == "wireHorizontal" or logicArray[i][j-1][0] == "Switch_OFF" or logicArray[i][j-1][0] == "Switch_ON") and (logicArray[i][j+1][0] == "wireHorizontal" or logicArray[i][j+1][0] == "wireBottomRight"):
                            logicArray[i][j][0] = "wireSplitterDown"
                        elif logicArray[i+1][j][0] == None:
                            logicArray[i][j][0] = "wireHorizontal"
                        elif logicArray[i][j-1][0] == None:
                            logicArray[i][j][0] = "wireVertical"
                        elif logicArray[i-1][j][0] == "wireHorizontal":
                            logicArray[i][j][0] = "wireSplitterLeft"
                            logicArray[i-1][j][0] = "wireVertical"
                    #bottom left change
                    elif logicArray[i][j][0] == "wireBottomLeft":
                        if (logicArray[i-1][j][0] == "wireHorizontal" or logicArray[i-1][j][0] == "wireVertical") and (logicArray[i][j-1][0] == "wireHorizontal" or logicArray[i][j-1][0] == "Switch_OFF" or logicArray[i][j-1][0] == "Switch_ON") and (logicArray[i][j+1][0] == "wireHorizontal" or logicArray[i][j+1][0] == "wireTopRight"):
                            logicArray[i][j][0] = "wireSplitterUp"
                        if logicArray[i-1][j][0] == None:
                            logicArray[i][j][0] = "wireHorizontal"
                        elif logicArray[i][j+1][0] == None:
                            logicArray[i][j][0] = "wireVertical"
                        elif logicArray[i+1][j][0] == "wireHorizontal":
                            logicArray[i][j][0] = "wireSplitterRight"
                            logicArray[i+1][j][0] = "wireVertical"
                    #bottom right change
                    elif logicArray[i][j][0] == "wireBottomRight":
                        if (logicArray[i-1][j][0] == "wireHorizontal" or logicArray[i-1][j][0] == "wireVertical") and (logicArray[i][j-1][0] == "wireHorizontal" or logicArray[i][j-1][0] == "Switch_OFF" or logicArray[i][j-1][0] == "Switch_ON") and logicArray[i][j+1][0] == "wireHorizontal":
                            logicArray[i][j][0] = "wireSplitterUp"
                        elif logicArray[i-1][j][0] == None:
                            logicArray[i][j][0] = "wireHorizontal"
                        elif logicArray[i][j-1][0] == None:
                            logicArray[i][j][0] = "wireVertical"
                        elif logicArray[i+1][j][0] == "wireHorizontal":
                            logicArray[i][j][0] = "wireSplitterLeft"
                            logicArray[i+1][j][0] = "wireVertical"
                    elif logicArray[i][j][0] == "wireIntersection":
                        if logicArray[i][j+1][0] != "ANDGate" and logicArray[i][j+1][0] != "ORGate" and logicArray[i][j+1][0] != "NORGate" and logicArray[i][j+1][0] != "NANDGate" and logicArray[i][j+1][0] != "XNORGate" and logicArray[i][j+1][0] != "XORGate" and logicArray[i][j+1][0] != "DFlipFlop":
                            logicArray[i][j][0] = [None]
                    #wire splitter down change
                    elif logicArray[i][j][0] == "wireSplitterDown":
                        if (logicArray[i][j-1][0] == "wireHorizontal" and logicArray[i][j+1][0] == "wireHorizontal") and (logicArray[i+1][j][0] == "wireVertical" and logicArray[i-1][j][0] == "wireHorizontal"):
                            logicArray[i][j] = ["wireCross",False,False]
                            logicArray[i-1][j][0] = "wireVertical"
                        elif logicArray[i+1][j][0] == None:
                            logicArray[i][j][0] = "wireHorizontal"
                        elif logicArray[i][j-1][0] == None:
                            logicArray[i][j][0] = "wireTopLeft"
                        elif logicArray[i][j+1][0] == None:
                            logicArray[i][j][0] = "wireTopRight"
                    #wire splitter up change
                    elif logicArray[i][j][0] == "wireSplitterUp":
                        if (logicArray[i][j-1][0] == "wireHorizontal" and logicArray[i][j+1][0] == "wireHorizontal") and (logicArray[i+1][j][0] == "wireHorizontal" and logicArray[i-1][j][0] == "wireVertical"):
                            logicArray[i][j] = ["wireCross",False,False]
                            logicArray[i+1][j][0] = "wireVertical"
                        elif logicArray[i-1][j][0] == None:
                            logicArray[i][j][0] = "wireHorizontal"
                        elif logicArray[i][j-1][0] == None:
                            logicArray[i][j][0] = "wireBottomLeft"
                        elif logicArray[i][j+1][0] == None:
                            logicArray[i][j][0] = "wireBottomRight"
                    #wire splitter right change
                    elif logicArray[i][j][0] == "wireSplitterRight":
                        if logicArray[i-1][j][0] == None:
                            logicArray[i][j][0] = "wireTopLeft"
                        elif logicArray[i+1][j][0] == None:
                            logicArray[i][j][0] = "wireBottomLeft"
                        elif logicArray[i][j+1][0] == None:
                            logicArray[i][j][0] = "wireVertical"
                        elif logicArray[i][j-1][0] == "wireHorizontal":
                            logicArray[i][j] = ["wireCross",False,False]
                    #wire splitter left change
                    elif logicArray[i][j][0] == "wireSplitterLeft":
                        if logicArray[i-1][j][0] == None:
                            logicArray[i][j][0] = "wireTopRight"
                        elif logicArray[i+1][j][0] == None:
                            logicArray[i][j][0] = "wireBottomRight"
                        elif logicArray[i][j-1][0] == None:
                            logicArray[i][j][0] = "wireHorizontal"
                        elif logicArray[i][j+1][0] == "wireHorizontal":
                            logicArray[i][j] = ["wireCross",False,False]
                    
                    #wire cross change
                    elif logicArray[i][j][0] == "wireCross":
                        if logicArray[i-1][j][0] == None:
                            logicArray[i][j] = ["wireSplitterDown", False, None]
                        elif logicArray[i+1][j][0] == None:
                            logicArray[i][j] = ["wireSplitterUp", False, None]
                        elif logicArray[i][j+1][0] == None:
                            logicArray[i][j] = ["wireSplitterLeft", False, None]
                        elif logicArray[i][j-1][0] == None:
                            logicArray[i][j] = ["wireSplitterRight", False, None]
                
        mainLoop()  

        #reArrayLast consists of: [“add/remove”, “logicElement”, Ypositon, Xposition]
        def reInsert(reArrayLast, state):
            #logic element removal
            if reArrayLast[0] == "remove":
                #if logic element is a wire or NOT gate
                if reArrayLast[1] == "NOTGate" or reArrayLast[1] == "Switch_OFF" or reArrayLast[1] == "Light_OFF" or reArrayLast[1] == "wireHorizontal" or reArrayLast[1] == "wireVertical" or reArrayLast[1] == "wireTopLeft" or reArrayLast[1] == "wireTopRight" or reArrayLast[1] == "wireBottomRight" or reArrayLast[1] == "wireBottomLeft":
                    #turning off connected wires
                    if len(logicArray[reArrayLast[2]][reArrayLast[3]]) == 3:
                        print(logicArray[reArrayLast[2]][reArrayLast[3]][2])
                        if logicArray[reArrayLast[2]][reArrayLast[3]][2] == "Up":
                            turnOffVerticalUp(reArrayLast[2],reArrayLast[3])
                        elif logicArray[reArrayLast[2]][reArrayLast[3]][2] == "Down":
                            turnOffVerticalDown(reArrayLast[2],reArrayLast[3])
                        elif logicArray[reArrayLast[2]][reArrayLast[3]][2] == "Right":
                            turnOffHorizontalRight(reArrayLast[2],reArrayLast[3])
                        elif logicArray[reArrayLast[2]][reArrayLast[3]][2] == "Left":
                            turnOffHorizontalLeft(reArrayLast[2],reArrayLast[3])
                    elif reArrayLast[1] == "Clock":
                        pass
                    else:
                        turnOffHorizontalRight(reArrayLast[2],reArrayLast[3])
                    logicArray[reArrayLast[2]][reArrayLast[3]] = [None]
                #if logic element is a logic gate
                else:
                    turnOffHorizontalRight(reArrayLast[2],reArrayLast[3])
                    logicArray[reArrayLast[2]][reArrayLast[3]] = [None]
                    logicArray[reArrayLast[2]][reArrayLast[3]-1] = [None]
                if state == "undo":
                    #reArrayLast is popped from undo stack and pushed to redo stack with function reversed from add to remove
                    reArrayLast[0] = "add"
                    redoStack.append(reArrayLast)
                    del undoStack[len(undoStack)-1]
                elif state == "redo":
                    #reArrayLast is popped from redo stack and pushed to undo stack with function reversed from add to remove
                    reArrayLast[0] = "add"
                    undoStack.append(reArrayLast)
                    del redoStack[len(redoStack)-1]
            #logic element insertion
            elif reArrayLast[0] == "add":
                #NOT gate is reinserted
                if reArrayLast[1] == "NOTGate":
                    logicArray[reArrayLast[2]][reArrayLast[3]] = ["NOTGate", False, False]
                #switch or light is reinserted
                elif reArrayLast[1] == "Switch_OFF" or reArrayLast[1] == "Light_OFF":
                    logicArray[reArrayLast[2]][reArrayLast[3]] = [reArrayLast[1], False]
                #wire is reinserted
                elif reArrayLast[1] == "wireHorizontal" or reArrayLast[1] == "wireVertical" or reArrayLast[1] == "wireTopLeft" or reArrayLast[1] == "wireTopRight" or reArrayLast[1] == "wireBottomRight" or reArrayLast[1] == "wireBottomLeft":
                    logicArray[reArrayLast[2]][reArrayLast[3]] = ["wireHorizontal", False, None]
                #logic gate is reinserted
                else:
                    logicArray[reArrayLast[2]][reArrayLast[3]] = [reArrayLast[1], False]
                    if reArrayLast[1] == "Clock":
                        pass
                    else:
                        logicArray[reArrayLast[2]][reArrayLast[3]-1] = ["wireIntersection", False, False]
                if state == "redo":
                    #reArrayLast is popped from redo stack and pushed to undo stack with function reversed from add to remove
                    reArrayLast[0] = "remove"
                    undoStack.append(reArrayLast)
                    del redoStack[len(redoStack)-1]
                elif state == "undo":
                    #reArrayLast is popped from undo stack and pushed to redo stack with function reversed from add to remove
                    reArrayLast[0] = "remove"
                    redoStack.append(reArrayLast)
                    del undoStack[len(undoStack)-1]
                    
        #tutorial text
        if tutorialPhase == 1:
            #text and constants
            paragraphText = [
                "Welcome to the Tutorial",
                "First we are going to build a NOT Gate circuit",
                "Select the switch and place it in the glowing square"]
            yPos = 280
            lineSpacing = 20
            
            #width and height definitions
            textWidth = 400
            textHeight = len(paragraphText) * lineSpacing
            rectangleWidth = textWidth + 30
            rectangleHeight = textHeight + 20
            
            #drawing background rectangle
            rectangleSurface = pygame.Surface((rectangleWidth, rectangleHeight))
            rectangleSurface.fill(BLUE)
            rectangleRect = rectangleSurface.get_rect()
            rectangleRect.topleft = (830, 280)
            SCREEN.blit(rectangleSurface, rectangleRect)
            #drawing lines of text
            for line in paragraphText:
                textSurface = get_font3(15).render(line, True, BLACK)
                SCREEN.blit(textSurface, (835, yPos))
                yPos += lineSpacing
        elif tutorialPhase == 2:
            paragraphText = [
                "Well done!",
                "Now to place the wires that will be used to connect the circuit",
                "Select the wire and place it in the glowing squares"]
            yPos = 280
            lineSpacing = 20
            
            textWidth = 480
            textHeight = len(paragraphText) * lineSpacing
            rectangleWidth = textWidth + 30
            rectangleHeight = textHeight + 20
            
            rectangleSurface = pygame.Surface((rectangleWidth, rectangleHeight))
            rectangleSurface.fill(BLUE)
            rectangleRect = rectangleSurface.get_rect()
            rectangleRect.topleft = (760, 280)
            SCREEN.blit(rectangleSurface, rectangleRect)
            for line in paragraphText:
                textSurface = get_font3(15).render(line, True, BLACK)
                SCREEN.blit(textSurface, (765, yPos))
                yPos += lineSpacing
        elif tutorialPhase == 3:
            paragraphText = [
                "Now we need to add the logic gate to the circuit",
                "The gate we will be using is a NOT gate, which inverts the input",
                "Select the NOT gate and place it in the glowing square"]
            yPos = 280
            lineSpacing = 20
            
            textWidth = 490
            textHeight = len(paragraphText) * lineSpacing
            rectangleWidth = textWidth + 30
            rectangleHeight = textHeight + 20
            
            rectangleSurface = pygame.Surface((rectangleWidth, rectangleHeight))
            rectangleSurface.fill(BLUE)
            rectangleRect = rectangleSurface.get_rect()
            rectangleRect.topleft = (755, 280)
            SCREEN.blit(rectangleSurface, rectangleRect)
            for line in paragraphText:
                textSurface = get_font3(15).render(line, True, BLACK)
                SCREEN.blit(textSurface, (760, yPos))
                yPos += lineSpacing
        elif tutorialPhase == 4:
            paragraphText = [
                "We now need to put in the light bulb, completing the circuit",
                "Select the light bulb and place it in the glowing square"]
            yPos = 280
            lineSpacing = 20
            
            textWidth = 465
            textHeight = len(paragraphText) * lineSpacing
            rectangleWidth = textWidth + 30
            rectangleHeight = textHeight + 20
            
            rectangleSurface = pygame.Surface((rectangleWidth, rectangleHeight))
            rectangleSurface.fill(BLUE)
            rectangleRect = rectangleSurface.get_rect()
            rectangleRect.topleft = (775, 280)
            SCREEN.blit(rectangleSurface, rectangleRect)
            for line in paragraphText:
                textSurface = get_font3(15).render(line, True, BLACK)
                SCREEN.blit(textSurface, (780, yPos))
                yPos += lineSpacing
        elif tutorialPhase == 5:
            paragraphText = [
                "Now the circuit has been completed",
                "Feel free to test the circuit by turning it on and off",
                "Press the next button to continue"]
            yPos = 280
            lineSpacing = 20
            
            textWidth = 410
            textHeight = len(paragraphText) * lineSpacing
            rectangleWidth = textWidth + 30
            rectangleHeight = textHeight + 20
            
            rectangleSurface = pygame.Surface((rectangleWidth, rectangleHeight))
            rectangleSurface.fill(BLUE)
            rectangleRect = rectangleSurface.get_rect()
            rectangleRect.topleft = (800, 280)
            SCREEN.blit(rectangleSurface, rectangleRect)
            for line in paragraphText:
                textSurface = get_font3(15).render(line, True, BLACK)
                SCREEN.blit(textSurface, (805, yPos))
                yPos += lineSpacing
        elif tutorialPhase == 6:
            paragraphText = [
                "Now we are going to make an AND circuit",
                "We are going to need two switches for this circuit",
                "Select the switch and place it in the glowing squares"]
            yPos = 280
            lineSpacing = 20
            
            textWidth = 410
            textHeight = len(paragraphText) * lineSpacing
            rectangleWidth = textWidth + 30
            rectangleHeight = textHeight + 20
            
            rectangleSurface = pygame.Surface((rectangleWidth, rectangleHeight))
            rectangleSurface.fill(BLUE)
            rectangleRect = rectangleSurface.get_rect()
            rectangleRect.topleft = (830, 280)
            SCREEN.blit(rectangleSurface, rectangleRect)
            for line in paragraphText:
                textSurface = get_font3(15).render(line, True, BLACK)
                SCREEN.blit(textSurface, (835, yPos))
                yPos += lineSpacing
        elif tutorialPhase == 7:
            paragraphText = [
                "Now we need to place the wires needed for the circuit",
                "This will allow both of the switches to connect to the AND gate",
                "Select the wire and place it in the glowing squares"]
            yPos = 280
            lineSpacing = 20
            
            textWidth = 480
            textHeight = len(paragraphText) * lineSpacing
            rectangleWidth = textWidth + 30
            rectangleHeight = textHeight + 20
            
            rectangleSurface = pygame.Surface((rectangleWidth, rectangleHeight))
            rectangleSurface.fill(BLUE)
            rectangleRect = rectangleSurface.get_rect()
            rectangleRect.topleft = (750, 280)
            SCREEN.blit(rectangleSurface, rectangleRect)
            for line in paragraphText:
                textSurface = get_font3(15).render(line, True, BLACK)
                SCREEN.blit(textSurface, (755, yPos))
                yPos += lineSpacing
        elif tutorialPhase == 8:
            paragraphText = [
                "Now we need to place the logic gate needed for the circuit",
                "The gate we will be using an AND gate, which turns on when both inputs are on",
                "Select the AND gate and place it in the glowing square"]
            yPos = 280
            lineSpacing = 20
            
            textWidth = 595
            textHeight = len(paragraphText) * lineSpacing
            rectangleWidth = textWidth + 30
            rectangleHeight = textHeight + 20
            
            rectangleSurface = pygame.Surface((rectangleWidth, rectangleHeight))
            rectangleSurface.fill(BLUE)
            rectangleRect = rectangleSurface.get_rect()
            rectangleRect.topleft = (650, 280)
            SCREEN.blit(rectangleSurface, rectangleRect)
            for line in paragraphText:
                textSurface = get_font3(15).render(line, True, BLACK)
                SCREEN.blit(textSurface, (655, yPos))
                yPos += lineSpacing
        elif tutorialPhase == 9:
            paragraphText = [
                "We now need to put in the light bulb, completing the circuit",
                "Select the light bulb and place it in the glowing square"]
            yPos = 280
            lineSpacing = 20
            
            textWidth = 465
            textHeight = len(paragraphText) * lineSpacing
            rectangleWidth = textWidth + 30
            rectangleHeight = textHeight + 20
            
            rectangleSurface = pygame.Surface((rectangleWidth, rectangleHeight))
            rectangleSurface.fill(BLUE)
            rectangleRect = rectangleSurface.get_rect()
            rectangleRect.topleft = (775, 280)
            SCREEN.blit(rectangleSurface, rectangleRect)
            for line in paragraphText:
                textSurface = get_font3(15).render(line, True, BLACK)
                SCREEN.blit(textSurface, (780, yPos))
                yPos += lineSpacing
        elif tutorialPhase == 10:
            paragraphText = [
                "The AND gate circuit is now complete",
                "Feel free to test it again, you can also change the gate to one of your choosing",
                "Select the gate you want and place it in the same place as the AND Gate",
                "Press next to finish the tutorial"]
            yPos = 280
            lineSpacing = 20
            
            textWidth = 620
            textHeight = len(paragraphText) * lineSpacing
            rectangleWidth = textWidth + 30
            rectangleHeight = textHeight + 20
            
            rectangleSurface = pygame.Surface((rectangleWidth, rectangleHeight))
            rectangleSurface.fill(BLUE)
            rectangleRect = rectangleSurface.get_rect()
            rectangleRect.topleft = (620, 280)
            SCREEN.blit(rectangleSurface, rectangleRect)
            for line in paragraphText:
                textSurface = get_font3(15).render(line, True, BLACK)
                SCREEN.blit(textSurface, (625, yPos))
                yPos += lineSpacing
            
        
        #drawing buttons
        for button in [logicInterfaceSave, logicInterfaceSaveAs, logicInterfaceLoad, logicInterfaceUndo, logicInterfaceRedo, logicInterfaceTruthTable, logicInterfaceDelete, logicInterfaceClear, logicInterfaceNew, logicInterfaceMainMenu]:
            button.changeColor(logicInterface_MOUSE_POS)
            button.update(SCREEN)
        if tutorialPhase != None and tutorialPhase != 10:
            logicInterfaceTutorialBack.changeColor(logicInterface_MOUSE_POS)
            logicInterfaceTutorialBack.update(SCREEN)
        #input checker
        if tutorialPhase == None:
            #keyboard shortcuts
            keys = pygame.key.get_pressed()
            #undo
            if keys[pygame.K_LCTRL] and keys[pygame.K_z]:
                if undoStack == []:
                    pass
                else:
                    print(undoStack)
                    reInsert(undoStack[len(undoStack)-1], "undo")
                    print(undoStack)
                    print(redoStack)
            #redo
            elif keys[pygame.K_LCTRL] and keys[pygame.K_y]:
                if redoStack == []:
                    pass
                else:
                    print(redoStack)
                    reInsert(redoStack[len(redoStack)-1], "redo")
                    print(redoStack)
                    print(undoStack)
            #save
            elif keys[pygame.K_LCTRL] and keys[pygame.K_s]:
                if fileName == None:
                    saveAsInterface(logicArray, fileName)
                else:
                    logicFile = open(fileName, "wb")
                    pickle.dump(logicArray, logicFile)
                    logicFile.close()
                    logicSaveText = get_font2(25).render("Save Successful", True, GREEN)
                    logicSaveTextRect = logicSaveText.get_rect()
                    logicSaveTextRect.center = (120,670)
                    SCREEN.blit(logicSaveText, logicSaveTextRect)
                    pygame.display.update()
                    time.sleep(1)
                    print("Save Successful")
            #load
            elif keys[pygame.K_LCTRL] and keys[pygame.K_l]:
                loadInterface(logicArray, fileName,False)
                print(logicArray)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    print("X pos " + str(mouseX))
                    print("Y pos " + str(mouseY))
                    #button checker
                    #save as pressed
                    if logicInterfaceSaveAs.checkForInput(logicInterface_MOUSE_POS):
                        saveAsInterface(logicArray, fileName)
                    #delete pressed
                    if logicInterfaceDelete.checkForInput(logicInterface_MOUSE_POS):
                        #delete functionality acts as an active gate
                        if activeGate != "Delete":
                            activeGate = "Delete"
                            #button changes colour if pressed
                            logicInterfaceDelete = Button(pos=(625,30), text_input="Delete", font=get_font2(25), base_color="Yellow", hovering_color=GREY)
                            logicInterfaceDelete.changeColor(logicInterface_MOUSE_POS)
                            logicInterfaceDelete.update(SCREEN)
                            pygame.display.update()
                            print(activeGate)
                        else:
                            logicInterfaceDelete = Button(pos=(525,30),
                                    text_input="Delete", font=get_font2(25), base_color="Black", hovering_color=GREY)
                            activeGate = None
                    #undo button pressed
                    if logicInterfaceUndo.checkForInput(logicInterface_MOUSE_POS):
                        if undoStack == []:
                            pass
                        else:
                            print(undoStack)
                            reInsert(undoStack[len(undoStack)-1], "undo")
                            print(undoStack)
                            print(redoStack)
                    #redo button pressed
                    if logicInterfaceRedo.checkForInput(logicInterface_MOUSE_POS):
                        if redoStack == []:
                            pass
                        else:
                            print(redoStack)
                            reInsert(redoStack[len(redoStack)-1], "redo")
                            print(redoStack)
                            print(undoStack)
                    #truth table button pressed
                    if logicInterfaceTruthTable.checkForInput(logicInterface_MOUSE_POS):
                        activeGate = None
                        #finds the outputted information from a combination of inputs in the truth table
                        def checkOutput(combinationList,switchPosArray,lightPosArray):
                            output = []
                            print("combination list: " + str(combinationList))
                            #iterates through the combination of inputs
                            for i in range(0,len(combinationList)):
                                #switch is turned on, if combination specifies
                                if combinationList[i] == 1:
                                    turnOnHorizontalRight(switchPosArray[i][0],switchPosArray[i][1])
                                    logicArray[switchPosArray[i][0]][switchPosArray[i][1]] = ["Switch_ON",True]
                                    #main loop run to produce changes in logic array
                                    mainLoop()
                                #switch is turned off, if combination specifies
                                elif combinationList[i] == 0:
                                    turnOffHorizontalRight(switchPosArray[i][0],switchPosArray[i][1])
                                    logicArray[switchPosArray[i][0]][switchPosArray[i][1]] = ["Switch_OFF",False]
                                    #main loop run to produce changes in logic array
                                    mainLoop()
                            print("the length: " + str(len(lightPosArray)))
                            #checking if light bulbs turn on in correspondence, iterates through list of light positions
                            outputNumber = 0
                            while outputNumber < len(lightPosArray):
                                if logicArray[lightPosArray[outputNumber][0]][lightPosArray[outputNumber][1]][0] == "Light_ON":
                                    #output of light is appended to overall output
                                    output.append(1)
                                elif logicArray[lightPosArray[outputNumber][0]][lightPosArray[outputNumber][1]][0] == "Light_OFF":
                                    #output of light is appended to overall output
                                    output.append(0)
                                outputNumber += 1
                            print(output)
                            #overall output appended to truth table row
                            truthTable[1].append(output)
                        
                        #initial values and data structures set
                        switchCount = 0
                        lightCount = 0
                        switchPosArray = []
                        lightPosArray = []
                        truthTable = [[],[]]
                        print(switchCount)
                        print(lightCount)
                        #logic array is searched for switches and lights
                        for i in range(0,len(logicArray)):
                                for j in range(0,len(logicArray[i])):
                                    #switch found
                                    if logicArray[i][j][0] == "Switch_OFF" or logicArray[i][j][0] == "Switch_ON":
                                        switchCount += 1
                                        switchPosArray.append([i,j])
                                    #light found
                                    elif logicArray[i][j][0] == "Light_OFF" or logicArray[i][j][0] == "Light_ON":
                                        lightCount += 1
                                        lightPosArray.append([i,j])
                        
                        #amount of possible switch combinations is calcualted as 2^n
                        switchCombinations = 2**switchCount
                        #print values in shell
                        print("switchCount: " + str(switchCount))
                        print("switchPosArray: " + str(switchPosArray))
                        print("lightCount: " + str(lightCount))
                        print("lightPosArray: " + str(lightPosArray))
                        for i in range(0,switchCombinations):
                            rowList = []
                            #each switch combination is converted to binary
                            convertedNumber = binaryConvert(i)
                            if len(str(convertedNumber)) < switchCount:
                                difference = switchCount - len(str(convertedNumber))
                                #if binary number is less than the number of bits, zeros are appended to the combination
                                for i in range(0,difference):
                                    rowList.append(0)
                            #binary number is converted to list format
                            convertedNumberList = [int(x) for x in str(convertedNumber)]
                            #binary number is added to contents of rowList
                            rowList = rowList + convertedNumberList
                            #binary combination is appended to truth table
                            truthTable[0].append(rowList)
                        
                        #translation only runs if switches and lights are detected
                        if switchCount > 0 and switchCount < 5 and lightCount > 0:
                            for i in range(0,len(truthTable[0])):
                                checkOutput(truthTable[0][i],switchPosArray,lightPosArray)
                            
                            print(truthTable)

                            translate(truthTable,switchCount,lightCount, switchCombinations, logicArray, fileName)
                    
                    #save button pressed
                    if logicInterfaceSave.checkForInput(logicInterface_MOUSE_POS):
                        #file is a new document, pressing save directs the user to the save as menu
                        if fileName == None:
                            activeGate = None
                            saveAsInterface(logicArray, fileName)
                        #file is a previously saved document, pressing save overwrites file contents
                        else:
                            logicFile = open(fileName, "wb")
                            pickle.dump(logicArray, logicFile)
                            logicFile.close()
                            logicSaveText = get_font2(25).render("Save Successful", True, GREEN)
                            logicSaveTextRect = logicSaveText.get_rect()
                            logicSaveTextRect.center = (120,670)
                            SCREEN.blit(logicSaveText, logicSaveTextRect)
                            pygame.display.update()
                            time.sleep(1)
                            print("Save Successful")
                    #load button pressed
                    if logicInterfaceLoad.checkForInput(logicInterface_MOUSE_POS):
                        activeGate = None
                        loadInterface(logicArray, fileName,False)
                        print(logicArray)
                    #clear button pressed
                    if logicInterfaceClear.checkForInput(logicInterface_MOUSE_POS):
                        #stacks reset
                        undoStack = []
                        redoStack = []
                        #logic array reset
                        logicArray = []
                        for i in range(0,14):
                            logicArray.append([[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None]])
                    #new button pressed
                    if logicInterfaceNew.checkForInput(logicInterface_MOUSE_POS):
                        #stacks reset
                        undoStack = []
                        redoStack = []
                        #array reset
                        logicArray = []
                        #fileName reset
                        fileName = None
                        for i in range(0,14):
                            logicArray.append([[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None]])
                    #main menu button pressed
                    if logicInterfaceMainMenu.checkForInput(logicInterface_MOUSE_POS):
                        mainMenu()
                    if event.button == 1:
                        #logic menu input checker
                        if mouseX >= 25 and mouseX <= 75 and mouseY >= 100 and mouseY <= 140:
                            if activeGate == "ORGate":
                                #if the gate is already active, active gate is reset
                                activeGate = None
                            else:
                                #clicking the gate causes it to become active 
                                activeGate = "ORGate"
                        elif mouseX >= 99 and mouseX <= 125 and mouseY >= 100 and mouseY <= 140:
                            if activeGate == "NOTGate":
                                activeGate = None
                            else:
                                activeGate = "NOTGate"
                        elif mouseX >= 175 and mouseX <= 225 and mouseY >= 100 and mouseY <= 140:
                            if activeGate == "ANDGate":
                                activeGate = None
                            else:
                                activeGate = "ANDGate"
                        elif mouseX >= 25 and mouseX <= 75 and mouseY >= 175 and mouseY <= 215:
                            if activeGate == "NORGate":
                                activeGate = None
                            else:
                                activeGate = "NORGate"
                        elif mouseX >= 99 and mouseX <= 125 and mouseY >= 175 and mouseY <= 215:
                            if activeGate == "NANDGate":
                                activeGate = None
                            else:
                                activeGate = "NANDGate"
                        elif mouseX >= 175 and mouseX <= 225 and mouseY >= 175 and mouseY <= 215:
                            if activeGate == "XNORGate":
                                activeGate = None
                            else:
                                activeGate = "XNORGate"
                        elif mouseX >= 25 and mouseX <= 75 and mouseY >= 250 and mouseY <= 290:
                            if activeGate == "XORGate":
                                activeGate = None
                            else:
                                activeGate = "XORGate"
                        elif mouseX >= 20 and mouseX <= 69 and mouseY >= 355 and mouseY <= 375:
                            if activeGate == "Switch_OFF":
                                activeGate = None
                            else:
                                activeGate = "Switch_OFF"
                        elif mouseX >= 27 and mouseX <= 67 and mouseY >= 440 and mouseY <= 491:
                            if activeGate == "Light_OFF":
                                activeGate = None
                            else:
                                activeGate = "Light_OFF"
                        elif mouseX >= 90 and mouseX <= 140 and mouseY >= 345 and mouseY <= 395:
                            if activeGate == "wireHorizontal":
                                activeGate = None
                            else:
                                activeGate = "wireHorizontal"
                        elif mouseX >= 165 and mouseX <= 215 and mouseY >= 348 and mouseY <= 398:
                            if activeGate == "Clock":
                                activeGate = None
                            else:
                                activeGate = "Clock"
                        elif mouseX >= 25 and mouseX <= 75 and mouseY >= 550 and mouseY <= 605:
                            if activeGate == "DFlipFlop":
                                activeGate = None
                            else:
                                activeGate = "DFlipFlop"
                        elif mouseX >= 1050 and mouseX <= 1100 and mouseY >= 30 and mouseY <= 50:
                            #toggle on/off for auto save, only will turn on if file name is not none
                            if autoSave == False and fileName != None:
                                autoSave = True
                            else:
                                autoSave = False
                                
                        #placement checker
                        elif mouseX >= 251 and mouseX <= 1280 and mouseY >= 60 and mouseY <= 697:
                            #grid position is calculated
                            Xsquare = (mouseX-251)//49
                            Ysquare = (mouseY-60)//49
                            print(Xsquare)
                            print(Ysquare)
                            if activeGate != None:
                                redoStack = []
                            if activeGate == "ORGate":
                                #OR gate is added to grid
                                logicArray[Ysquare][Xsquare] = ["ORGate", False]
                                #wire intersection is added to grid
                                logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                #active gate is reset
                                activeGate = None
                                #action is added to undo stack
                                undoStack.append(["remove", "ORGate", Ysquare, Xsquare])
                                print(activeGate)
                            elif activeGate == "NOTGate":
                                #NOT gate is added to grid
                                logicArray[Ysquare][Xsquare] = ["NOTGate", False]
                                activeGate = None
                                undoStack.append(["remove", "NOTGate", Ysquare, Xsquare])
                                print(activeGate)
                            elif activeGate == "ANDGate":
                                #AND gate is added to grid
                                logicArray[Ysquare][Xsquare] = ["ANDGate", False]
                                logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                activeGate = None
                                undoStack.append(["remove", "ANDGate", Ysquare, Xsquare])
                                print(activeGate)
                            elif activeGate == "NORGate":
                                #NOR gate is added to grid
                                logicArray[Ysquare][Xsquare] = ["NORGate", False]
                                logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                activeGate = None
                                undoStack.append(["remove", "NORGate", Ysquare, Xsquare])
                                print(activeGate)
                            elif activeGate == "NANDGate":
                                #NAND gate is added to grid
                                logicArray[Ysquare][Xsquare] = ["NANDGate", False]
                                logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                activeGate = None
                                undoStack.append(["remove", "NANDGate", Ysquare, Xsquare])
                                print(activeGate)
                            elif activeGate == "XNORGate":
                                #XNOR gate is added to grid
                                logicArray[Ysquare][Xsquare] = ["XNORGate", False]
                                logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                activeGate = None
                                undoStack.append(["remove", "XNORGate", Ysquare, Xsquare])
                                print(activeGate)
                            elif activeGate == "XORGate":
                                #XOR gate is added to grid
                                logicArray[Ysquare][Xsquare] = ["XORGate", False]
                                logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                activeGate = None
                                undoStack.append(["remove", "XORGate", Ysquare, Xsquare])
                                print(activeGate)
                            elif activeGate == "Light_OFF":
                                #light is added to grid
                                logicArray[Ysquare][Xsquare] = ["Light_OFF", False]
                                activeGate = None
                                undoStack.append(["remove", "Light_OFF", Ysquare, Xsquare])
                                print(activeGate)
                            elif activeGate == "Switch_OFF":
                                #switch is added to grid
                                logicArray[Ysquare][Xsquare] = ["Switch_OFF", False]
                                activeGate = None
                                undoStack.append(["remove", "Switch_OFF", Ysquare, Xsquare])
                                print(activeGate)
                            elif activeGate == "wireHorizontal":
                                #horizontal wire is added to grid
                                logicArray[Ysquare][Xsquare] = ["wireHorizontal", False, None]
                                undoStack.append(["remove", "wireHorizontal", Ysquare, Xsquare])
                            elif activeGate == "Clock":
                                #clock is added to grid
                                logicArray[Ysquare][Xsquare] = ["Clock", False]
                                activeGate = None
                                undoStack.append(["remove", "Clock", Ysquare, Xsquare])
                            elif activeGate == "DFlipFlop":
                                #D type flip flop is added to grid
                                logicArray[Ysquare][Xsquare] = ["DFlipFlop",False]
                                logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                activeGate = None
                                undoStack.append(["remove", "DFlipFlop", Ysquare, Xsquare])
                            elif activeGate == "Delete":
                                undoStack.append(["add", logicArray[Ysquare][Xsquare][0], Ysquare, Xsquare])
                                print(undoStack)
                                if len(logicArray[Ysquare][Xsquare]) == 3:
                                    if logicArray[Ysquare][Xsquare][2] == "Up":
                                        turnOffVerticalUp(Ysquare,Xsquare)
                                    elif logicArray[Ysquare][Xsquare][2] == "Down":
                                        turnOffVerticalDown(Ysquare,Xsquare)
                                    elif logicArray[Ysquare][Xsquare][2] == "Right":
                                        if logicArray[Ysquare][Xsquare][0] == "wireSplitterDown":
                                            turnOffVerticalDown(Ysquare,Xsquare)
                                        turnOffHorizontalRight(Ysquare,Xsquare)
                                    elif logicArray[Ysquare][Xsquare][2] == "Left":
                                        if logicArray[Ysquare][Xsquare][0] == "wireSplitterDown":
                                            turnOffVerticalDown(Ysquare,Xsquare)
                                        turnOffHorizontalLeft(Ysquare,Xsquare)
                                if logicArray[Ysquare][Xsquare][0] == "wireIntersection":
                                    logicArray[Ysquare][Xsquare+1] = [None]
                                elif logicArray[Ysquare][Xsquare-1][0] == "wireIntersection":
                                    logicArray[Ysquare][Xsquare-1] = [None]
                                logicArray[Ysquare][Xsquare] = [None]
                            elif logicArray[Ysquare][Xsquare] == None:
                                break
                            elif logicArray[Ysquare][Xsquare][0] == "Switch_OFF":
                                logicArray[Ysquare][Xsquare] = ["Switch_ON", True]
                                lastCountChange = count
                            elif logicArray[Ysquare][Xsquare][0] == "Switch_ON":
                                logicArray[Ysquare][Xsquare] = ["Switch_OFF", False]
                                lastCountChange = count
                        print(logicArray)
                        print(activeGate)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        print(logicArray)
                        
        elif tutorialPhase != None:
            #functionality of stage 1 of the tutorial
            if tutorialPhase == 1:
                #loaction for the user to place a switch is set
                logicArray[6][1] = ["switchToBe"]
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #pixel position of click determined
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        print("X pos " + str(mouseX))
                        print("Y pos " + str(mouseY))
                        if event.button == 1:
                            #selection only allows for a switch to be selected
                            if mouseX >= 20 and mouseX <= 69 and mouseY >= 355 and mouseY <= 375:
                                if activeGate == "Switch_OFF":
                                    activeGate = None
                                else:
                                    activeGate = "Switch_OFF"
                                    print(activeGate)
                            elif mouseX >= 251 and mouseX <= 1280 and mouseY >= 60 and mouseY <= 697:
                                #x and y squares in grid are determined
                                Xsquare = (mouseX-251)//49
                                Ysquare = (mouseY-60)//49
                                print(Xsquare)
                                print(Ysquare)
                                if activeGate == "Switch_OFF":
                                    #user can only place in a specific square
                                    if logicArray[Ysquare][Xsquare][0] == "switchToBe":
                                        logicArray[Ysquare][Xsquare] = ["Switch_OFF", False]
                                        activeGate = None
                                        #procede to next phase
                                        tutorialPhase += 1
                            if logicInterfaceTutorialBack.checkForInput(logicInterface_MOUSE_POS):
                                #user returns to main menu if back button is pressed
                                mainMenu()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            print(logicArray)
                            
            elif tutorialPhase == 2:
                for i in range(2,7):
                    if i != 4:
                        #location for each wire piece is set
                        if logicArray[6][i][0] == None:
                            logicArray[6][i] = ["wireToBe"]
                #variable checking if all wires have been placed
                complete = True
                for i in range(2,7):
                    if i != 4:
                        if logicArray[6][i][0] == "wireToBe":
                            complete = False
                if complete == True:
                    tutorialPhase += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        print("X pos " + str(mouseX))
                        print("Y pos " + str(mouseY))
                        if event.button == 1:
                            if mouseX >= 90 and mouseX <= 140 and mouseY >= 345 and mouseY <= 395:
                                if activeGate == "wireHorizontal":
                                    activeGate = None
                                else:
                                    activeGate = "wireHorizontal"
                            elif mouseX >= 251 and mouseX <= 1280 and mouseY >= 60 and mouseY <= 697:
                                Xsquare = (mouseX-251)//49
                                Ysquare = (mouseY-60)//49
                                print(Xsquare)
                                print(Ysquare)
                                if activeGate == "wireHorizontal":
                                    if logicArray[Ysquare][Xsquare][0] == "wireToBe":
                                        logicArray[Ysquare][Xsquare] = ["wireHorizontal", False, None]
                            if logicInterfaceTutorialBack.checkForInput(logicInterface_MOUSE_POS):
                                mainMenu()
                                    
            elif tutorialPhase == 3:
                #activeGate is reset
                if activeGate == "wireHorizontal":
                    activeGate = None
                #location for NOT gate is set
                if logicArray[6][4][0] == None:
                    logicArray[6][4][0] = "NOTGateToBe"
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        print("X pos " + str(mouseX))
                        print("Y pos " + str(mouseY))
                        if event.button == 1:
                            #selection only allows for NOT gates to selected
                            if mouseX >= 99 and mouseX <= 125 and mouseY >= 100 and mouseY <= 140:
                                if activeGate == "NOTGate":
                                    activeGate = None
                                else:
                                    activeGate = "NOTGate"
                            elif mouseX >= 251 and mouseX <= 1280 and mouseY >= 60 and mouseY <= 697:
                                Xsquare = (mouseX-251)//49
                                Ysquare = (mouseY-60)//49
                                print(Xsquare)
                                print(Ysquare)
                                if activeGate == "NOTGate":
                                    if logicArray[Ysquare][Xsquare][0] == "NOTGateToBe":
                                        logicArray[Ysquare][Xsquare] = ["NOTGate", False]
                                        activeGate = None
                                        tutorialPhase += 1
                            if logicInterfaceTutorialBack.checkForInput(logicInterface_MOUSE_POS):
                                mainMenu()
                                
                                
            elif tutorialPhase == 4:
                #location for user to place a light is set
                if logicArray[6][7][0] == None:
                    logicArray[6][7][0] = "lightToBe"
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        print("X pos " + str(mouseX))
                        print("Y pos " + str(mouseY))
                        if event.button == 1:
                            #selection only allows lights to be selected
                            if mouseX >= 27 and mouseX <= 67 and mouseY >= 440 and mouseY <= 491:
                                if activeGate == "Light_OFF":
                                    activeGate = None
                                else:
                                    activeGate = "Light_OFF"
                            elif mouseX >= 251 and mouseX <= 1280 and mouseY >= 60 and mouseY <= 697:
                                Xsquare = (mouseX-251)//49
                                Ysquare = (mouseY-60)//49
                                print(Xsquare)
                                print(Ysquare)
                                if activeGate == "Light_OFF":
                                    if logicArray[Ysquare][Xsquare][0] == "lightToBe":
                                        logicArray[Ysquare][Xsquare] = ["Light_OFF", False]
                                        activeGate = None
                                        tutorialPhase += 1
                            if logicInterfaceTutorialBack.checkForInput(logicInterface_MOUSE_POS):
                                mainMenu()
                                
            elif tutorialPhase == 5:
                #next button becomes visible to user
                logicInterfaceTutorialNext.changeColor(logicInterface_MOUSE_POS)
                logicInterfaceTutorialNext.update(SCREEN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        print("X pos " + str(mouseX))
                        print("Y pos " + str(mouseY))
                        if event.button == 1:
                            if mouseX >= 251 and mouseX <= 1280 and mouseY >= 60 and mouseY <= 697:
                                Xsquare = (mouseX-251)//49
                                Ysquare = (mouseY-60)//49
                                print(Xsquare)
                                print(Ysquare)
                                #user can turn the switch on and off 
                                if logicArray[Ysquare][Xsquare][0] == "Switch_OFF":
                                    logicArray[Ysquare][Xsquare] = ["Switch_ON", True]
                                elif logicArray[Ysquare][Xsquare][0] == "Switch_ON":
                                    logicArray[Ysquare][Xsquare] = ["Switch_OFF", False]
                            if logicInterfaceTutorialBack.checkForInput(logicInterface_MOUSE_POS):
                                mainMenu()
                            if logicInterfaceTutorialNext.checkForInput(logicInterface_MOUSE_POS):
                                #pressing next procedes to AND circuit building
                                tutorialPhase += 1
                                
            elif tutorialPhase == 6:
                #logic array reset
                if logicArray[6][1][0] == "Switch_OFF" or logicArray[6][1][0] == "Switch_ON":
                    logicArray = []
                    for i in range(0,14):
                        logicArray.append([[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None]])
                    #locations for switches to be placed are set
                    logicArray[5][1][0] = "switchToBe"
                    logicArray[7][1][0] = "switchToBe"
                if logicArray[5][1][0] == "Switch_OFF" and logicArray[7][1][0] == "Switch_OFF":
                    tutorialPhase += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        print("X pos " + str(mouseX))
                        print("Y pos " + str(mouseY))
                        if event.button == 1:
                            #oselection only allows for a switch to be placed
                            if mouseX >= 20 and mouseX <= 69 and mouseY >= 355 and mouseY <= 375:
                                if activeGate == "Switch_OFF":
                                    activeGate = None
                                else:
                                    activeGate = "Switch_OFF"
                                    print(activeGate)
                            elif mouseX >= 251 and mouseX <= 1280 and mouseY >= 60 and mouseY <= 697:
                                Xsquare = (mouseX-251)//49
                                Ysquare = (mouseY-60)//49
                                print(Xsquare)
                                print(Ysquare)
                                if activeGate == "Switch_OFF":
                                    if logicArray[Ysquare][Xsquare][0] == "switchToBe":
                                        logicArray[Ysquare][Xsquare] = ["Switch_OFF", False]
                                        activeGate = None
                            if logicInterfaceTutorialBack.checkForInput(logicInterface_MOUSE_POS):
                                mainMenu()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            print(logicArray)
                            
            elif tutorialPhase == 7:
                if logicArray[5][2][0] == None:
                    #locations for wires to be placed are set
                    for i in range(2,4):
                        logicArray[5][i][0] = "wireToBe"
                        logicArray[7][i][0] = "wireToBe"
                if logicArray[5][2][0] == "wireHorizontal" and logicArray[7][2][0] == "wireHorizontal" and logicArray[5][3][0] == "wireHorizontal" and logicArray[7][3][0] == "wireHorizontal":
                    activeGate = None
                    tutorialPhase += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        print("X pos " + str(mouseX))
                        print("Y pos " + str(mouseY))
                        if event.button == 1:
                            #selection only allows for a wire to be placed
                            if mouseX >= 90 and mouseX <= 140 and mouseY >= 345 and mouseY <= 395:
                                if activeGate == "wireHorizontal":
                                    activeGate = None
                                else:
                                    activeGate = "wireHorizontal"
                            elif mouseX >= 251 and mouseX <= 1280 and mouseY >= 60 and mouseY <= 697:
                                Xsquare = (mouseX-251)//49
                                Ysquare = (mouseY-60)//49
                                print(Xsquare)
                                print(Ysquare)
                                if activeGate == "wireHorizontal":
                                    if logicArray[Ysquare][Xsquare][0] == "wireToBe":
                                        logicArray[Ysquare][Xsquare] = ["wireHorizontal", False, None]
                            if logicInterfaceTutorialBack.checkForInput(logicInterface_MOUSE_POS):
                                mainMenu()               
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            print(logicArray)
            elif tutorialPhase == 8:
                #location for AND gate is set
                 if logicArray[6][4][0] == None:
                     logicArray[6][4][0] = "gateToBe"
                 for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        print("X pos " + str(mouseX))
                        print("Y pos " + str(mouseY))
                        if event.button == 1:
                            if mouseX >= 175 and mouseX <= 225 and mouseY >= 100 and mouseY <= 140:
                                if activeGate == "ANDGate":
                                    activeGate = None
                                else:
                                    activeGate = "ANDGate"
                            elif mouseX >= 251 and mouseX <= 1280 and mouseY >= 60 and mouseY <= 697:
                                Xsquare = (mouseX-251)//49
                                Ysquare = (mouseY-60)//49
                                print(Xsquare)
                                print(Ysquare)
                                if activeGate == "ANDGate":
                                    if logicArray[Ysquare][Xsquare][0] == "gateToBe":
                                        logicArray[Ysquare][Xsquare] = ["ANDGate", False]
                                        logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                        activeGate = None
                                        tutorialPhase += 1
                                        print(activeGate)
                            if logicInterfaceTutorialBack.checkForInput(logicInterface_MOUSE_POS):
                                mainMenu()               
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            print(logicArray)
            elif tutorialPhase == 9:
                #location for light is set
                if logicArray[6][5][0] == None:
                    logicArray[6][5][0] = "lightToBe"
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        print("X pos " + str(mouseX))
                        print("Y pos " + str(mouseY))
                        if event.button == 1:
                            if mouseX >= 27 and mouseX <= 67 and mouseY >= 440 and mouseY <= 491:
                                if activeGate == "Light_OFF":
                                    activeGate = None
                                else:
                                    activeGate = "Light_OFF"
                            elif mouseX >= 251 and mouseX <= 1280 and mouseY >= 60 and mouseY <= 697:
                                Xsquare = (mouseX-251)//49
                                Ysquare = (mouseY-60)//49
                                print(Xsquare)
                                print(Ysquare)
                                if activeGate == "Light_OFF":
                                    if logicArray[Ysquare][Xsquare][0] == "lightToBe":
                                        logicArray[Ysquare][Xsquare] = ["Light_OFF", False]
                                        activeGate = None
                                        tutorialPhase += 1
                            if logicInterfaceTutorialBack.checkForInput(logicInterface_MOUSE_POS):
                                mainMenu()
            elif tutorialPhase == 10:
                #next button appears visible to user
                logicInterfaceTutorialNext.changeColor(logicInterface_MOUSE_POS)
                logicInterfaceTutorialNext.update(SCREEN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        print("X pos " + str(mouseX))
                        print("Y pos " + str(mouseY))
                        if event.button == 1:
                            #any logic gate can be placed in place of the AND gate
                            if mouseX >= 25 and mouseX <= 75 and mouseY >= 100 and mouseY <= 140:
                                if activeGate == "ORGate":
                                    activeGate = None
                                else:
                                    activeGate = "ORGate"
                            elif mouseX >= 175 and mouseX <= 225 and mouseY >= 100 and mouseY <= 140:
                                if activeGate == "ANDGate":
                                    activeGate = None
                                else:
                                    activeGate = "ANDGate"
                            elif mouseX >= 25 and mouseX <= 75 and mouseY >= 175 and mouseY <= 215:
                                if activeGate == "NORGate":
                                    activeGate = None
                                else:
                                    activeGate = "NORGate"
                            elif mouseX >= 99 and mouseX <= 125 and mouseY >= 175 and mouseY <= 215:
                                if activeGate == "NANDGate":
                                    activeGate = None
                                else:
                                    activeGate = "NANDGate"
                            elif mouseX >= 175 and mouseX <= 225 and mouseY >= 175 and mouseY <= 215:
                                if activeGate == "XNORGate":
                                    activeGate = None
                                else:
                                    activeGate = "XNORGate"
                            elif mouseX >= 25 and mouseX <= 75 and mouseY >= 250 and mouseY <= 290:
                                if activeGate == "XORGate":
                                    activeGate = None
                                else:
                                    activeGate = "XORGate"
                            elif mouseX >= 251 and mouseX <= 1280 and mouseY >= 60 and mouseY <= 697:
                                Xsquare = (mouseX-251)//49
                                Ysquare = (mouseY-60)//49
                                print(Xsquare)
                                print(Ysquare)
                                if logicArray[Ysquare][Xsquare][0] == "ORGate" or logicArray[Ysquare][Xsquare][0] == "ANDGate" or logicArray[Ysquare][Xsquare][0] == "NORGate" or logicArray[Ysquare][Xsquare][0] == "NANDGate" or logicArray[Ysquare][Xsquare][0] == "XNORGate" or logicArray[Ysquare][Xsquare][0] == "XORGate":
                                    if activeGate == "ORGate":
                                        logicArray[Ysquare][Xsquare] = ["ORGate", False]
                                        logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                        activeGate = None
                                        print(activeGate)
                                    elif activeGate == "ANDGate":
                                        logicArray[Ysquare][Xsquare] = ["ANDGate", False]
                                        logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                        activeGate = None
                                        undoStack.append(["remove", "ANDGate", Ysquare, Xsquare])
                                        print(activeGate)
                                    elif activeGate == "NORGate":
                                        logicArray[Ysquare][Xsquare] = ["NORGate", False]
                                        logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                        activeGate = None
                                        print(activeGate)
                                    elif activeGate == "NANDGate":
                                        logicArray[Ysquare][Xsquare] = ["NANDGate", False]
                                        logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                        activeGate = None
                                        print(activeGate)
                                    elif activeGate == "XNORGate":
                                        logicArray[Ysquare][Xsquare] = ["XNORGate", False]
                                        logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                        activeGate = None
                                        print(activeGate)
                                    elif activeGate == "XORGate":
                                        logicArray[Ysquare][Xsquare] = ["XORGate", False]
                                        logicArray[Ysquare][Xsquare-1] = ["wireIntersection", False, False]
                                        activeGate = None
                                        print(activeGate)
                                if logicArray[Ysquare][Xsquare][0] == "Switch_OFF":
                                    logicArray[Ysquare][Xsquare] = ["Switch_ON", True]
                                elif logicArray[Ysquare][Xsquare][0] == "Switch_ON":
                                    logicArray[Ysquare][Xsquare] = ["Switch_OFF", False]
                            if logicInterfaceTutorialNext.checkForInput(logicInterface_MOUSE_POS):
                                #tutorial ends
                                mainMenu()
                    
        pygame.display.update()

def adders():
    pygame.display.set_caption("Adders")
    while True:
        adders_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill(BLACK)
        
        
        #adder text created
        adders_TEXT = get_font1(45).render("Please select an adder to load", True, WHITE)
        adders_RECT = adders_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(adders_TEXT, adders_RECT)
        
        #buttons created
        addersBack = Button(pos=(640,440),text_input="Back", font=get_font2(30), base_color=WHITE, hovering_color=GREEN)
        addersHalfAdder = Button(pos=(550, 360), text_input="Half Adder", font=get_font2(30), base_color=WHITE, hovering_color=GREEN)
        addersFullAdder = Button(pos=(730,360), text_input="Full Adder", font = get_font2(30), base_color=WHITE, hovering_color=GREEN)
        
        #buttons draw in in interface
        for button in [addersBack, addersHalfAdder, addersFullAdder]:
            button.changeColor(adders_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #back button pressed
                if addersBack.checkForInput(adders_MOUSE_POS):
                    mainMenu()
                #half adder button pressed
                if addersHalfAdder.checkForInput(adders_MOUSE_POS):
                    #file is loaded from adders folder
                    currentDirectory = os.path.dirname(os.path.abspath(__file__))
                    folderPath = os.path.join(currentDirectory, "adders")
                    filePath = os.path.join(folderPath, "halfAdder")
                    logicFile = open(filePath,"rb")
                    logicArray = pickle.load(logicFile)
                    #logic interface opens
                    logicInterface(logicArray,"halfAdder", False)
                #full addder button pressed
                if addersFullAdder.checkForInput(adders_MOUSE_POS):
                    #file is loaded from adders folder
                    currentDirectory = os.path.dirname(os.path.abspath(__file__))
                    folderPath = os.path.join(currentDirectory, "adders")
                    filePath = os.path.join(folderPath, "fullAdder")
                    logicFile = open(filePath,"rb")
                    logicArray = pickle.load(logicFile)
                    #logic interface opens
                    logicInterface(logicArray,"fullAdder", False)
                    
        pygame.display.update()
        
def mainMenu():
    pygame.display.set_caption("Main Menu")
    #logic array reset
    logicArray = []
    for i in range(0,14):
        logicArray.append([[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None],[None], [None], [None]])
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        menuText = get_font1(100).render("Logic Gate Simulator", True, "#b68f40")
        menuRect = menuText.get_rect(center=(640, 100))

        #menu buttons created
        newFileButton = Button(pos=(640, 200), 
                            text_input="New File", font=get_font1(75), base_color="#d7fcd4", hovering_color=WHITE)
        loadFileButton = Button(pos=(640, 300), 
                            text_input="Load File", font=get_font1(75), base_color="#d7fcd4", hovering_color=WHITE)
        tutorialButton = Button(pos=(640, 400), 
                            text_input="Tutorial", font=get_font1(75), base_color="#d7fcd4", hovering_color=WHITE)
        adderButton = Button(pos=(640, 500), 
                            text_input="Adders", font=get_font1(75), base_color="#d7fcd4", hovering_color=WHITE)
        quitButton = Button(pos=(640, 600), 
                            text_input="Quit", font=get_font1(75), base_color="#d7fcd4", hovering_color=WHITE)

        SCREEN.blit(menuText, menuRect)

        for button in [newFileButton, loadFileButton, tutorialButton, adderButton, quitButton]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #new file button pressed
                if newFileButton.checkForInput(MENU_MOUSE_POS):
                    logicInterface(logicArray, None,False)
                #load file button pressed
                if loadFileButton.checkForInput(MENU_MOUSE_POS):
                    loadInterface(logicArray,None,True)
                #adder button pressed
                if adderButton.checkForInput(MENU_MOUSE_POS):
                    adders()
                #tutorial button pressed
                if tutorialButton.checkForInput(MENU_MOUSE_POS):
                    logicInterface(logicArray, None, True)
                #quit button pressed
                if quitButton.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

#main menu opens
mainMenu()