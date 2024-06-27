class Treasure():
    def __init__(self, value:int, level:str) -> None:
        self.value = value
        self.level = level
    #end def:constructor
    def getValue(self) -> int:
        return self.value
    #end def:function
    def getLevel(self) -> str:
        return self.level
    #end def:function
    def setValue(self, value):
        self.value = value
    #end def:procedure
    def setLevel(self, level):
        self.level = level
    #end def:procedure
#end class

myTreasure = Treasure(0, "None")
if myTreasure.getValue() == 0:
    myTreasure.setValue(input("Your treasure has no value. Enter one: "))
if myTreasure.getLevel() == "None":
    myTreasure.setLevel(input("There is no level. Enter one: "))

print("Treasure:", myTreasure.getValue(), myTreasure.getLevel())
