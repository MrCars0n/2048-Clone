# Colors
ColorEmptySq = (204, 192, 179)
Color2 = (238, 228, 218)
Color4 = (237, 224, 200)
Color8 = (242, 177, 121)
Color16 = (245, 149, 99)
Color32 = (231, 130, 102)
Color64 = (245, 124, 95)
Color128 = (237, 206, 113)
Color256 = (237, 204, 97)
Color512 = (236, 200, 80)
Color1024 = (237, 197, 63)
Color2048 = (238, 194, 45)
ColorAbove2048 = (61, 58, 51)


# Determine color by number
def determineColor(number):
    if number == 0:
        return ColorEmptySq
    elif number == 2:
        return Color2
    elif number == 4:
        return Color4
    elif number == 8:
        return Color8
    elif number == 16:
        return Color16
    elif number == 32:
        return Color32
    elif number == 64:
        return Color64
    elif number == 128:
        return Color128
    elif number == 256:
        return Color256
    elif number == 512:
        return Color512
    elif number == 1024:
        return Color1024
    elif number == 2048:
        return Color2048
    else:
        return ColorAbove2048


class Square:
    def __init__(self, number=0, width=0, color=0):
        self.number = number
        self.width = width

        # Determine color based on number if not specified in constructor
        if color == 0:
            self.color = determineColor(number)
        else:
            self.color = color
        self.hasCombined = False

    def setWidth(self, width):
        self.width = width

    def setNumber(self, number):
        self.number = number

    def getWidth(self):
        return self.width

    def getNumber(self):
        return self.number

    def getHasCombined(self):
        return self.hasCombined

    def setHasCombined(self, boolean):
        self.hasCombined = boolean

    def getColor(self):
        self.color = determineColor(self.number)
        return self.color
