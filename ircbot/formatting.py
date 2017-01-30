class Format:
    # Codes from https://github.com/myano/jenni/wiki/IRC-String-Formatting
    BOLD = "\x02"
    COLOR = "\x03"
    ITALIC = "\x1D"
    UNDERLINE = "\x1F"
    SWAP = "\x16"
    RESET = "\x0F"

    WHITE = COLOR + "00"
    BLACK = COLOR + "01"
    BLUE = COLOR + "02"
    GREEN = COLOR + "03"
    RED = COLOR + "04"
    BROWN = COLOR + "05"
    PURPLE = COLOR + "06"
    ORANGE = COLOR + "07"
    YELLOW = COLOR + "08"
    LIME = COLOR + "09"
    TEAL = COLOR + "10"
    AQUA = COLOR + "11"
    ROYAL = COLOR + "12"
    PINK = COLOR + "13"
    GREY = COLOR + "14"
    SILVER = COLOR + "15"

    TEST_STRING = "none %swhite %sblack %sblue %sgreen %sred %sbrown %spurple %sorange %syellow %slime %steal " \
                  "%saqua %sroyal %spink %sgrey %ssilver%s" % (
                      WHITE, BLACK, BLUE, GREEN, RED, BROWN, PURPLE, ORANGE, YELLOW, LIME, TEAL, AQUA, ROYAL, PINK,
                      GREY, SILVER, RESET
                  )
