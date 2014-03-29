import sys
import string
import re
from optparse import OptionParser, HelpFormatter, IndentedHelpFormatter

__author__ = 'Soh Ishiguro'
__program__ = 'pretty_bio_strings'
__license__ = 'MIT'


class PrettyBioStrings(object):
    def __init__(self):
        self.NUC_CODE =  {
            'A': '\033[35m',
            'T': '\033[32m',
            'G': '\033[36m',
            'C': '\033[34m',
            'RESET': "\033[0m",
        }
        self.P_R_CODE = {}
        self.HYDROPHOBIC_CODE = {}
        self.POLAR_CODE = {}
        
    def run(self):
        self.opt = self.__cmd_args()
        if self.opt.fasta:
            fa = self._fasta_to_dict(self.opt.fasta)
            for entory in fa:
                sys.stdout.write('>' + entory + '\n')
                self.seq_to_color(fa[entory])
        elif self.opt.seq:
            self.seq_to_color(self.opt.seq)

    def seq_to_color(self, seq):
        char = list(seq)
        for _ in char:
            if _ == 'A':
                sys.stdout.write(self.NUC_CODE['A'] + 'A' + self.NUC_CODE['RESET'])
            elif _ == 'T':
                sys.stdout.write(self.NUC_CODE['T'] + 'T' + self.NUC_CODE['RESET'])
            elif _ == 'G':
                sys.stdout.write(self.NUC_CODE['G'] + 'G' + self.NUC_CODE['RESET'])
            elif _ == 'C':
                sys.stdout.write(self.NUC_CODE['C'] + 'C' + self.NUC_CODE['RESET'])
        sys.stdout.write("\n")

    def _fasta_to_dict(self, fasta):
        recs = dict()
        with open(fasta, 'r') as f:
            for line in f:
                if line.startswith(">"):
                    fasta_p = re.compile(r'^>(.+)$')
                    ma = fasta_p.match(line)
                    if ma:
                        header = ma.group(1)
                    else:
                        raise SystemExit("[{0}] is not Fasta format file".format(fasta))
                seq = line.strip("\n")
                recs.update({header: seq})
        if len(recs) <= 0:
            raise SystemExit("No sequence entory is found in {0}".format(fasta))
            
        return recs

    def __cmd_args(self):
        desc = 'Pretty printer for nucleotide sequence in your console'
        usage = 'Usage: %prog [options]'
        fmt = IndentedHelpFormatter(indent_increment=2, max_help_position=60,
                                    width=120, short_first=1)
        parser = OptionParser(usage=usage, formatter=fmt, version='0.0.1',  description=desc)
        parser.add_option('-f', '--fasta', dest='fasta', action='store', metavar='', type='string',
                          help='Fasta file')
        parser.add_option('-s','--seq', dest='seq', action='store', metavar='', type='string',
                          help="Raw sequence charactor")
        parser.add_option('-m', '--mode', dest='mode', action='store', metavar='', type='string',
                          help='Pretty print mode.')
        (opt, args) = parser.parse_args()
        return opt
    
            
if __name__ == '__main__':
    pp_bio = PrettyBioStrings()
    pp_bio.run()
    
