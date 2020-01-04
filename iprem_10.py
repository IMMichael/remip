#!/usr/bin/env python

from random import randrange
import argparse
import re
import os

class iprem_Tool():
    """ replace IP addresses with random values. """

    def __init__(self, arg_logfile, arg_verbose):
        self.logfile = arg_logfile
        self.verbose = arg_verbose
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


    def file_handle(self,filename,new_File=""):
        for logevent in open(filename, 'r'):
                line = logevent

                # replace IP addresses
                line = re.sub(
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', self._replace_ip, line)
                new_Line = line.strip()
                new_File = new_File + new_Line + '\n'
                
        if self.verbose:
            print filename + ':' + '\n' + new_File
            pass
        f = open(filename, 'w')
        f.write(new_File)
        f.close()
        return filename
        

    
    def run(self):
        """ Print out useful information about the log file. """
        check_path = self.logfile
        if os.path.isfile(check_path):
            filename = check_path
            self.file_handle(filename)
        else:
            check_path = os.path.abspath(check_path)
            os.chdir(check_path)
            for filename in os.listdir(check_path):
                    filename = os.path.abspath(filename)
                    self.file_handle(filename)



if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description = 'Anonymizes log files by replacing IP addresses.')
    argparser.add_argument('arg', type=str, help='File or Directory only.')
    argparser.add_argument('--verbose','-v', action='store_true', default=False, help='Provides further verbosity to stdout.')
    v_args = argparser.parse_args()

    tool = iprem_Tool(arg_logfile=v_args.arg,arg_verbose=v_args.verbose)
    tool.run()
