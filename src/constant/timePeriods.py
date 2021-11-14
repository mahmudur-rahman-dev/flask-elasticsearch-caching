import enum
# Using enum class create enumerations

# class periodDefinition:
#   def __init__(self, timePeriod):
#     self.timePeriod = timePeriod
#     # self.end = end
#     # return self
#   def getTimeDefinitionClass(self):
#     return (self.start, self.end)

class TimePeriods(enum.Enum):
    # LATE_NIGHT = periodDefinition("12 AM - 4 AM")
    # EARLY_MORNING = periodDefinition("4 AM - 8 AM")
    # MORNING = periodDefinition("8 AM - 12 PM")
    # NOON = periodDefinition("12 PM - 4 PM")
    # EVENING = periodDefinition("4 PM - 8 PM")
    # NIGHT = periodDefinition("8 PM - 12 AM")

    LATE_NIGHT = "12 AM - 4 AM"
    EARLY_MORNING = "4 AM - 8 AM"
    MORNING = "8 AM - 12 PM"
    NOON = "12 PM - 4 PM"
    EVENING = "4 PM - 8 PM"
    NIGHT = "8 PM - 12 AM"
    # LATE_NIGHT = ("12 AM", "4 AM"),
    # EARLY_MORNING = ("4 AM", "8 AM"),
    # MORNING = ("8 AM", "12 PM"),
    # NOON = ("12 PM", "4 PM"),
    # EVENING = ("4 PM", "8 PM"),
    # NIGHT = ("8 PM", "12 AM")


    # def getTimeDefinition(self):
    #   print("value: ",self.value)
    #   print("enum def: ",self.value[0])
    #   return self.value[0].getTimeDefinitionClass(self.value[0])


