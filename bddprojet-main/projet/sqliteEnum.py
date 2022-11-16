import enum

class SqliteTypes(enum.Enum):
    NULL    =   "null"       #The value is a NULL value.
    INTEGER =   "integer"    #The value is a signed integer, stored in 0, 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value.
    REAL    =   "real"       #The value is a floating point value, stored as an 8-byte IEEE floating point number.
    TEXT    =   "text"       #The value is a text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE).
    BLOBL   =   "blobl"      #The value is a blob of data, stored exactly as it was input.