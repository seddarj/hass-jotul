"""Constants for the Jotul integration."""

DOMAIN = "jotul"
STATUS_CODES = {
    0 : "OFF",
    1 : "OFF TIMER",
    2 : "TESTFIRE",
    3 : "HEATUP",
    4 : "FUELIGN",
    5 : "IGNTEST",
    6 : "BURNING",
    9 : "COOLFLUID",
    10 : "FIRESTOP",
    11 : "CLEANFIRE",
    12 : "COOL",
    241 : "CHIMNEY ALARM",
    243 : "GRATE ERROR",
    244 : "NTC2 ALARM",
    245 : "NTC3 ALARM",
    247 : "DOOR ALARM",
    248 : "PRESS ALARM",
    249 : "NTC1 ALARM",
    250 : "TC1 ALARM",
    252 : "GAS ALARM",
    253 : "NOPELLET ALARM"
}
