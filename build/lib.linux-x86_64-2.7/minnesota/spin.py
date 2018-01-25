import itertools, sys
spinner = itertools.cycle(['-', '/', '|', '\\'])
while True:
    sys.stdout.write(spinner.next())  # write the next character
    sys.stdout.flush()                # flush stdout buffer (actual character display)
    sys.stdout.write('\b')            # erase the last written char