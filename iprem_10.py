#!/usr/bin/env python

from random import randrange
import argparse
import re


class iprem_Tool():
    """ replace IP addresses with random values. """

    def __init__(self, arg_logfile):
        self.logfile = arg_logfile
        self.replacements = {}



    def _replace_ip(self, match):
        ip = match.group(0)
        # don't replace localhost ip
        if ip == '127.0.0.1':
            return ip

        if ip in self.replacements:
            return self.replacements[ip]
        else:
            n1 = randrange(0, 255)
            n2 = randrange(0, 255)
            n3 = randrange(0, 255)
            n4 = randrange(0, 255)
            return self.replacements.setdefault(ip, '%i.%i.%i.%i' % (n1, n2, n3, n4))


    
    def run(self):
        """ Print out useful information about the log file. """
        new_File = ""
        for logevent in open(self.logfile, 'r'):
            line = logevent

            # replace IP addresses
            line = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', self._replace_ip, line)
            new_Line = line.strip()
            #print new_Line
            
            
            new_File = new_File + new_Line + '\n'
        f = open(self.logfile, 'w')
        f.write(new_File)
        f.close()



if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.description = 'Anonymizes log files by replacing IP addresses.'
    argparser.add_argument('logfile', type=str)
    args = argparser.parse_args()

    tool = iprem_Tool(arg_logfile=args.logfile)
    tool.run()