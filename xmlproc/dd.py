import split, sys, outputters
from listsets import listminus, listunion
from xml.parsers.xmlproc import xmlproc

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

TEMP_FILE = "temp.xml"

def dd(c_pass, c_fail, test, splitter = None):
    """Return a triple (DELTA, C_PASS', C_FAIL') such that
       - C_PASS subseteq C_PASS' subset C_FAIL' subseteq C_FAIL holds
       - DELTA = C_FAIL' - C_PASS' is a minimal difference
         between C_PASS' and C_FAIL' that is relevant with respect to TEST."""

    if splitter is None:
        splitter = split.split

    n = 2

    while 1:
        assert test(c_pass) == PASS or UNRESOLVED
        assert test(c_fail) == FAIL
        assert n >= 2

        delta = listminus(c_fail, c_pass) #c_fail-c_pass

        if n > len(delta):
            # No further minimizing
            return (delta, c_pass, c_fail)

        deltas = splitter(delta, n)
        assert len(deltas) == n

        offset = 0
        j = 0
        while j < n:
            i = (j + offset) % n
            next_c_pass = listunion(c_pass, deltas[i])
            next_c_fail = listminus(c_fail, deltas[i])

            if test(next_c_fail) == FAIL and n == 2:
                c_fail = next_c_fail
                n = 2; offset = 0; break
            elif test(next_c_fail) == PASS or UNRESOLVED:
                c_pass = next_c_fail
                n = 2; offset = 0; break
            elif test(next_c_pass) == FAIL:
                c_fail = next_c_pass
                n = 2; offset = 0; break
            elif test(next_c_fail) == FAIL:
                c_fail = next_c_fail
                n = max(n - 1, 2); offset = i; break
            elif test(next_c_pass) == PASS or UNRESOLVED:
                c_pass = next_c_pass
                n = max(n - 1, 2); offset = i; break
            else:
                j = j + 1

        if j >= n:
            if n >= len(delta):
                return (delta, c_pass, c_fail)
            else:
                n = min(len(delta), n * 2)

if __name__ == "__main__":
    tests = {}
    c_fail = []
    warnings = 1
    entstack = 0
    rawxml = 0

    if len(sys.argv) < 2:
        print 'Please input file'
        sys.exit()

    fname = sys.argv[1]
    file = open(fname, 'r')
    data = file.read()
    file.close()

    app = xmlproc.Application()
    p = xmlproc.XMLProcessor()
    p.set_application(app)
    err = outputters.MyErrorHandler(p, p, warnings, entstack, rawxml)
    p.set_error_handler(err)
    p.set_data_after_wf_error(0)

    def string_to_list(s):
        c = []
        for i in range(len(s)):
            c.append((i, s[i]))
        return c

    def mytest(c):
        global tests
        global c_fail

        s = ""
        for (index, char) in c:
            s += char

        if s in tests.keys():
            return tests[s]

        map = {}
        for (index, char) in c:
            map[index] = char

        x = ""
        for i in range(len(c_fail)):
            if map.has_key(i):
                x += map[i]
            else:
                x += "."
        
        f = open(TEMP_FILE, 'w')
        f.write(s)
        f.close()

        try:
            p.parse_resource(TEMP_FILE)
            if err.errors == 0:
                print PASS
                tests[s] = PASS
                return PASS
            else:
                print UNRESOLVED
                tests[s] = UNRESOLVED
                return UNRESOLVED
                #print PASS
                #tests[s] = PASS
                #return PASS
        except UnboundLocalError:
            print FAIL
            tests[s] = FAIL
            return FAIL

    c_pass = []
    c_fail = string_to_list(data)
    (delta, c_pass, c_fail) = dd(c_pass, c_fail, mytest)
    print "==========delta=========="
    print delta 
    print "==========c_pass=========="
    print c_pass
    print "==========c_fail=========="
    print c_fail
