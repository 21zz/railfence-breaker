import sys
import railfence as rf
import enchant
import traceback
from pathos import multiprocessing
import time
from pathos.multiprocessing import cpu_count
import re
import argparse
import colorama

# initialize colored line library
colorama.init(autoreset=True)


"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ARG PARSER @@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
parser = argparse.ArgumentParser(
    description="Multithreaded Bruteforce tool for railfence cipher"
)

# ciphertext arg
parser.add_argument(
    "ct",
    metavar="ciphertext",
    type=str,
    help="railfence ciphertext"
)
# multithreaded
parser.add_argument(
    "-m", "--multithread",
    action="store_true",
    dest="mt",
    help="enable multithreading"
)
# number of processes
parser.add_argument(
    "-p", "--processes",
    type=int,
    dest="P",
    help="number of processes to use. if multithreading is enabled, the \
          default is 2. the maximum is the number of CPU threads you have"
)
# tolerance float
parser.add_argument(
    "-t", "--tolerance",
    type=float,
    dest="T",
    default=0.2
)
# verbose/debug
parser.add_argument(
    "-v", "--verbose",
    dest="dbg",
    action="store_true"
)


args = parser.parse_args()

"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DICTIONARY @@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
lang = "en_US"
d = enchant.Dict(lang)


"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ALGORITHM @@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""


def solve_railfence(ct, debug=False, multithreaded=False, processes=2, tolerance=0.2):  # railfence
    rails = list(range(2, len(ct) + 1))
    offset = list(range(0, len(rails) * 2 - 2))
    if debug:
        print(colorama.Fore.BLUE + "rails:\t\t" + str(rails))
        print(colorama.Fore.CYAN + "offset:\t\t" + str(offset))
        if multithreaded:
            print(colorama.Fore.GREEN + "multithreaded:\t" + str(multithreaded))
            print(colorama.Fore.GREEN + "processes:\t" + str(args.P))
        else:
            print(colorama.Fore.RED + "multithreaded:\t" + str(multithreaded))

        print(colorama.Fore.RED + "tolerance:\t" + str(tolerance))
    full_solve = []
    potential_solutions = []
    # --------------------------- start of basic defs---------------------------

    # using an offset o
    def solve_rails(o):
        to_out = []
        if debug:
            print("offset: " + str(o))
        for r in rails:  # for rail in rails (variable above)
            # return the decrypted fence
            decrypted = rf.decryptFence(ct, r, offset=o)
            to_out.append(decrypted)
        return(to_out)

    # filter out solution
    # returns None if solution is not correct enough
    # returns the solution if it's fine
    def filter_solution(solution):
        is_word_count = 0
        not_word_count = 0
        for w in solution.split():
            # regex to filter special chars
            w = re.sub('[^A-Za-z0-9]+', '', w)
            if len(w) == 0 or w == None or w == "":
                return
            if(d.check(w)):
                is_word_count += 1
            else:
                not_word_count += 1
        if(is_word_count > not_word_count):
            if(float(not_word_count) / float(is_word_count) < tolerance):
                if solution not in potential_solutions:
                    if debug:
                        print(colorama.Fore.GREEN +
                              colorama.Style.BRIGHT + "found potential solution")
                    return(solution)
    # --------------------------- end of basic defs ---------------------------
    if processes > cpu_count():
        processes = cpu_count()
    pool = multiprocessing.Pool(processes=processes)

    # --------------------------- start offset ---------------------------
    if multithreaded:  # run threaded
        for t in pool.map(solve_rails, offset):
            full_solve += t
    else:  # run on single thread, so use the above but iteratively
        for o in offset:
            full_solve += solve_rails(o)
    if debug:
        print("\nappended all possible values\n")
    if debug:
        expected = len(rails) * len(offset)
        actual = len(full_solve)
        print(colorama.Style.BRIGHT + "expected length, (rails * offset):\t" +
              str(expected))
        if actual == expected:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN +
                  "length of full_solve:\t\t\t" + str(actual))
        else:
            print(colorama.Style.BRIGHT + colorama.Fore.RED +
                  "length of full_solve: " + str(actual))

    # --------------------------- end offset ---------------------------

    # --------------------------- start solution filtering ---------------------------

    # after full_solve[] is acquired
    if debug:
        print(colorama.Style.DIM + str(full_solve))
    if multithreaded:
        # send list of fully calculated things to thread pool. comes back as a list of filtered things
        solut_list = pool.map(filter_solution, full_solve)
        # for solution in the list of possible solutions
        for solut in solut_list:
            if solut != None:
                potential_solutions.append(solut)
    else:  # run on single thread, so use the above but iteratively
        for solution in full_solve:
            solut = filter_solution(solution)
            if solut != None:
                potential_solutions.append(solut)
    if debug:
        print(colorama.Style.DIM + str(potential_solutions))
    if potential_solutions != []:
        return potential_solutions
    # --------------------------- end solution filtering ---------------------------

    # if nothing is returned above, return this string.
    # this means it went through all options and found nothing in
    # the english language using the given tolerance
    return("Exhausted. No matching solutions.")


"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@ MAIN FUNCTION CALL @@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
# use the args given by user to put into this function.
railfence_result = solve_railfence(
    # argument provided in command line
    args.ct,
    # multithreading on (True) or off (False)
    multithreaded=args.mt,
    # if multithreaded, this is how many
    # processes it will use.
    # cannot use more than you have cpu threads,
    # will make sure of this.
    processes=args.P,
    # debug prints on (True) or off (False)
    # this is known as verbose in argparser
    debug=args.dbg,
    # percentage of non-words allowed.
    # 20% (0.2) is default
    tolerance=args.T
)

"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@ PARSE FUNCTION OUTPUT @@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
# if length if the output's first index is 1, it's likely a string. so just output that string
if len(railfence_result[0]) == 1:
    print(colorama.Fore.RED + railfence_result)
# if the length of first index is not 1, then it's obviously something!
else:
    # remove duplicates
    newresult = []
    for r in railfence_result:
        if r not in newresult:
            newresult.append(r)
    # for each non-dupe, print with different color
    colors = [colorama.Fore.BLUE,
              colorama.Fore.RED,
              colorama.Fore.GREEN,
              colorama.Fore.YELLOW]
    for i in range(0, len(newresult)):
        print(colors[i % 3] + newresult[i])
