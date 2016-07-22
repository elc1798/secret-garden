import sys, traceback
import getpass

import db_session as dbs

class Gridifier:
    def __init__(self, array_repr):
        self.array_repr = array_repr

    def get_column_widths(self):
        if self.array_repr == []:
            return [ 0 ]
        widths = [ 0 ] * len(self.array_repr[0])
        for i in range(len(widths)):
            for row in self.array_repr:
                if i < len(row) and len(row[i]) > widths[i]:
                    widths[i] = len(row[i])
        return widths

    def get_grid(self):
        widths = self.get_column_widths()

        def pad(s, length):
            return s + " " * (length - len(s))

        gaps = [ "-" * (n + 2) for n in widths ]
        separator = "+" + "+".join(gaps) + "+\n"
        rows = []
        for i in range(len(self.array_repr)):
            padded = [ pad(self.array_repr[i][j], widths[j]) for j in range(len(self.array_repr[i])) ]
            while len(padded) < len(widths):
                padded.append(" " * widths[len(padded)])
            row = "| %s " * len(widths) + "|\n"
            rows.append(row % tuple(padded))

        grid = separator + separator.join(rows) + separator
        return grid

def ex3cut0r(func, *args, **kwargs):
    return func(*args, **kwargs)

def beautify(s):
    l = []
    if s == None:
        return ""
    elif type(s) in [ str, int, float ]:
        l = [ [s] ]
    elif type(s) in [ tuple, list ]:
        s = list(s)
        l = []
        for i in range(0, len(s), 4):
            if len(s[0]) == 1:
                l.append( [ str(t[0]) for t in s[i : i + 4] ] )
            else:
                if type(s[i]) in [ tuple, list ]:
                    for t in s[i : i + 4]:
                        l.append( [ str(item) for item in t ] )
                elif type(s[i]) in [ str, unicode ]:
                    l.append( [ str(item) for item in s[i : i + 4] ])
                else:
                    l.append( [ 'wtf this borkened' ] )
    else:
        return "Output type unrecognized\n"
    return Gridifier(l).get_grid()

class S3kr3t:
    """
    The class is called 'Secret' for a reason. No comments.
    """
    def __init__(self, dekrypshun):
        self.session = dbs.Session(dekrypshun)
        self.commands = {
            "spill" : self.spill,
            "clear" : self.clear,
            "help" : self.show_commands,
            "insert" : self.session.insert_into_table,
            "remove" : self.session.remove_from_table,
            "get" : self.session.get_password_by_key,
            "show" : self.session.get_keys,
            "showall" : self.session.get_all,
            "exit" : sys.exit,
            "quit" : sys.exit
        }

    def show_commands(self):
        print "Commands:"
        for key in self.commands.keys():
            print "\t%s" % (key,)

    def spill(self):
        print repr(self.session.enkryptor.key)

    def clear(self):
        sys.stdout.write("\033\143")

    def do_the_thing_with_the_thing_please(self, the_thing):
        #spongebobreferences

        if the_thing in [ "exit", "quit" ]:
            return

        output = "Command failed"
        try:
            l = the_thing.split(" ")
            output = ex3cut0r(self.commands[l[0]], *tuple(l[1:]))
            sys.stdout.write(beautify(output))
        except KeyboardInterrupt, EOFError:
            return
        except:
            print "Traceback:", traceback.print_exc()
            print output

def main():
    print "Welcome to the Sekr3t Gard3n."
    fate = str(getpass.getpass("What is your secret? ")).encode('utf-8')
    secret_session = S3kr3t(fate)
    command = ""
    while command not in ["exit", "quit"]:
        try:
            command = str(raw_input("<(^_^)> "))
            secret_session.do_the_thing_with_the_thing_please(command)
        except KeyboardInterrupt, EOFError:
            print

if __name__ == "__main__":
    main()

