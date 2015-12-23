import sys
import re

class Links:

    def __init__(self, fname):
        self.read(fname)

    def read(self, fname):
        f = open(fname, 'r')
        lines = f.readlines()
        f.close()

        i = 0
        self.links = {}
        self.revlinks = {}
        for l in lines:
            c = l.strip().split('|')
            self.links[i] = Link(c[0], c[1], c[2])
            self.revlinks[c[0]] = i
            i += 1

    def writeMakefile(self, mfname):
        mf = open(mfname, 'w')
        for i in self.links.keys():
            l = self.links[i]
            # push to Evernote
            mf.write(str.format("push{0} :\n\t", i))
            mf.write(str.format("geeknote find --search \"{0}\" --notebooks \"{1}\"\n\t", l.note, l.notebook))
            mf.write(str.format("geeknote edit 1 --content \"{0}\"\n", l.filepath))
            # pull from Evernote
            mf.write(str.format("pull{0} :\n\t", i))
            mf.write(str.format("geeknote find --search \"{0}\" --notebooks \"{1}\"\n\t", l.note, l.notebook))
            mf.write(str.format("geeknote show 1 > edump.tmp\n\t"))
            mf.write(str.format("python processEDump.py > {0}\n\t", l.filepath))
            mf.write(str.format("rm edump.tmp\n"))

    def getLinkNum(self, fpath):
        return self.revlinks[fpath]

    def listIn(self, dirpath):
        matches = []
        for link in self.links.values():
            match = re.match(dirpath, link.filepath)
            if match:
                matches.append((match, link))
        return matches

class Link:
    filepath=None
    notebook=None
    note=None

    def __init__(self, fp, nb, n):
        self.filepath = fp
        self.notebook = nb
        self.note = n

if __name__ == '__main__':
    ## TODO: better option and argument handling
    l = Links("links")
    if sys.argv[1] == "updatemf":
        l.writeMakefile("makefile")
    elif sys.argv[1] == "getnum":
        print l.getLinkNum(sys.argv[2])
    elif sys.argv[1] == "listin":
        matches = l.listIn(sys.argv[2])
        for (match, link) in matches:
            if len(sys.argv) > 3 and sys.argv[3] == 'fponly':
                print link.filepath[match.end()+1:]
            else:
                print str.format("\n{0}\n\tTitle: {1}\n\tNotebook: {2}",
                    link.filepath[match.end()+1:],
                    link.note,
                    link.notebook)
