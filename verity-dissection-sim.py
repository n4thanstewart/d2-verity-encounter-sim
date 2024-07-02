import random
import time
import threading
import sys

shapes = {"C": "circle", "S": "square", "T": "triangle"}

def combineShapes(shape_pair):
    shapes = tuple(sorted([shape_pair[0].lower(), shape_pair[1].lower()]))
    shape_combinations = {
        ("square", "triangle"): "Prism",
        ("circle", "triangle"): "Cone",
        ("circle", "square"): "Cylinder",
        ("circle", "circle"): "Sphere",
        ("square", "square"): "Cube",
        ("triangle", "triangle"): "Pyramid"
    }
    return shape_combinations.get(shapes, "Unknown combination")

def generateInnerCallout():
    shapes = ["C", "T", "S"]
    while True:
        callout = "".join(random.sample(shapes, 3))
        if len(set(callout)) == 3:
            return callout

def setupOuterStatues():
    shapes = ["circle", "triangle", "square"]
    all_shapes = shapes * 2
    random.shuffle(all_shapes)
    leftStatue = all_shapes[:2]
    middleStatue = all_shapes[2:4]
    rightStatue = all_shapes[4:]
    return leftStatue, middleStatue, rightStatue

def setupEncounter(challengeRating):
    callout = generateInnerCallout()
    print(f"\nInside callout: {callout}\n")
    if challengeRating=='':
        leftStatue, middleStatue, rightStatue = setupOuterStatues()
    elif challengeRating=="1":
        def containsOneDouble(statue):
            return "Sphere" == combineShapes(statue) or "Cube" == combineShapes(statue) or "Pyramid" == combineShapes(statue)
        leftStatue, middleStatue, rightStatue = setupOuterStatues()
        while not containsOneDouble(leftStatue) and not containsOneDouble(middleStatue) and not containsOneDouble(rightStatue):
            leftStatue, middleStatue, rightStatue = setupOuterStatues()
            break
    elif challengeRating=="2":
        shapes = ["circle", "triangle", "square"]
        random.shuffle(shapes)
        leftStatue = [shapes[0],shapes[0]]
        middleStatue = [shapes[1],shapes[1]]
        rightStatue = [shapes[2],shapes[2]]
    leftCombination = combineShapes(leftStatue)
    middleCombination = combineShapes(middleStatue)
    rightCombination = combineShapes(rightStatue)
    print(f"Left Statue: {leftCombination}")
    print(f"Middle Statue: {middleCombination}")
    print(f"Right Statue: {rightCombination}\n")
    return callout, leftStatue, middleStatue, rightStatue

def checkWinCondition(callout, leftStatue, middleStatue, rightStatue):
    def statueTarget(innerShape, outerShapes):
        if outerShapes[0] != shapes.get(innerShape) and outerShapes[1] != shapes.get(innerShape):
            return True
        return False
    if statueTarget(callout[0], leftStatue) and statueTarget(callout[1], middleStatue) and statueTarget(callout[2], rightStatue):
        return True
    return False

def swapShapes(command, leftStatue, middleStatue, rightStatue):
    statues = {"L": leftStatue, "M": middleStatue, "R": rightStatue}
    commands = command.split()
    
    if len(commands) < 5:
        print(f"Not enough arguments")
        return leftStatue, middleStatue, rightStatue
    
    shape1, dest1, shape2, dest2 = commands[0].upper(), commands[2].upper(), commands[3].upper(), commands[5].upper()

    def shapePresent(shape, statue):
        if shapes.get(shape) in statue:
            return True
        return False
    
    if not shapePresent(shape1, statues[dest1]):
        print(f"No {shape1} available in {dest1}")
        return leftStatue, middleStatue, rightStatue
        
    if not shapePresent(shape2, statues[dest2]):
        print(f"No {shape2} available in {dest2}")
        return leftStatue, middleStatue, rightStatue
    
    shapeDissected=statues[dest1].pop(statues[dest1].index(shapes.get(shape1)))
    shapeReplaced=statues[dest2].pop(statues[dest2].index(shapes.get(shape2)))
    statues[dest1].append(shapeReplaced)
    statues[dest2].append(shapeDissected)
    
    return leftStatue, middleStatue, rightStatue

def startTimer(duration):
    time.sleep(duration)
    print("\nTime's up")
    return True

def main():
    challengeRating=input("Challenge rating: ")
    callout, leftStatue, middleStatue, rightStatue = setupEncounter(challengeRating)
    while checkWinCondition(callout, leftStatue, middleStatue, rightStatue):
        callout, leftStatue, middleStatue, rightStatue = setupEncounter(challengeRating)

    timer_thread = threading.Thread(target=startTimer, args=(90,))
    timer_thread.daemon = True
    timer_thread.start()
    
    while timer_thread.is_alive():
        command = input("Enter command (e.g., 'C to L S to R'): ")
        if not timer_thread.is_alive():
            break
        leftStatue, middleStatue, rightStatue = swapShapes(command, leftStatue, middleStatue, rightStatue)
        leftCombination = combineShapes(leftStatue)
        middleCombination = combineShapes(middleStatue)
        rightCombination = combineShapes(rightStatue)

        print(f"\nLeft Statue: {leftCombination}")
        print(f"Middle Statue: {middleCombination}")
        print(f"Right Statue: {rightCombination}\n")
        
        if checkWinCondition(callout, leftStatue, middleStatue, rightStatue):
            print("Dissection completed")
            break
    
    if not timer_thread.is_alive():
        print("Time's up")
    sys.exit(0)

if __name__ == "__main__":
    main()
