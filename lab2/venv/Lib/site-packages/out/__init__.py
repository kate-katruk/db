import sys


class Cursor():

    def SetPos(col, row, flush=True):
        sys.stdout.write(u"\u001b[{0};{1}H".format(int(row), int(col)))
        if flush: sys.stdout.flush()

    def Left(n, flush=True):
        sys.stdout.write(u"\u001b[{0}D".format(str(n)))
        if flush: sys.stdout.flush()

    def Right(n, flush=True):
        sys.stdout.write(u"\u001b[{0}C".format(str(n)))
        if flush: sys.stdout.flush()

    def Up(n, flush=True):
        sys.stdout.write(u"\u001b[{0}A".format(str(n)))
        if flush: sys.stdout.flush()

    def Down(n, flush=True):
        sys.stdout.write(u"\u001b[{0}B".format(str(n)))
        if flush: sys.stdout.flush()


class Screen():

    def Clear(flush=True):
        sys.stdout.write(u"\u001b[2J")  # Clear screen
        if flush: sys.stdout.flush()

    def Flush():
        sys.stdout.flush()

    def Decorate(fg=None, bg=None, dec=None, flush=True):
        if (fg is None) and (bg is None) and (dec is None):
            sys.stdout.write(u"\u001b[0m")

        if fg is not None:
            sys.stdout.write(u"\u001b[38;5;{0}m".format(str(fg)))
        if bg is not None:
            sys.stdout.write(u"\u001b[48;5;{0}m".format(str(fg)))
        if dec is not None:
            if type(dec) == list:
                for thing in dec:
                    if (thing == "reversed"): sys.stdout.write(u"\u001b[7m")
                    elif (thing == "underline"): sys.stdout.write(u"\u001b[4m")
                    elif (thing == "bold"): sys.stdout.write(u"\u001b[1m")
                    else:
                        raise ValueError('"{}" Not rekognized as a decoration'.format(thing))

            elif type(dec) == str:
                if (dec == "reversed"): sys.stdout.write(u"\u001b[7m")
                elif (dec == "underline"): sys.stdout.write(u"\u001b[4m")
                elif (dec == "bold"): sys.stdout.write(u"\u001b[1m")
            else:
                raise ValueError('"{}" Not rekognized as a decoration'.format(dec))

        if flush: sys.stdout.flush()

    def Write(outStr, flush=True):
        sys.stdout.write(str(outStr))
        if flush: sys.stdout.flush()
