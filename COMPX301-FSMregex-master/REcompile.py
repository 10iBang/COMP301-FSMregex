# COMPX301-20A Lee So 1364878

# The context-free grammar used by the compiler is the following:
#   E -> T
#   E -> T E
#   T -> F
#   T -> F *
#   T -> F ?
#   T -> F | T
#   F -> v
#   F -> \ s
#   F -> .
#   F -> (E)
#
#   where E = expression, T = term, F = factor,
#   v = literal (which is not a reserved symbol with a function),
#   s = any symbol
#
# ===============================================================

import sys
import logging
import string

# set up logger handler to output to stdout for debugging purposes ==========
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)

# ====================================================
class FSM:
    c = ""  # the expected character
    next1 = 0  # next FSM, possibility 1
    next2 = 0  # next FSM, possibility 2

    def __init__(self, c: str, n1: int, n2: int):
        self.c = c
        self.next1 = n1
        self.next2 = n2

    def __str__(self):
        return self.c + " " + str(self.next1) + " " + str(self.next2)


class REcompiler:

    reservedChars = ".()*?|\\"  # symbols that have special meaning in the regex
    branchingStateChar = "BR"  # placeholder "null" character for branching-only state
    p = "notyetdefined"  # input regular expression (encased in quotes) through stdin
    j = 0  # iterator for parsing p
    state = 1  # the number of the state being built
    statemachines = []  # the array of state machines

    def __init__(self):
        pass

    def expression(self) -> int:
        """Evaluates a regex expression, returning the starting state
        of the expression finite state machine
        """

        # the starting state number of the expression
        startState = self.term()

        # once we're done with the term, check if we reached the end
        if self.j >= len(self.p):
            logging.info("end reached")
            return startState

        # check if what follows is something an expression could conceivably start with
        if (
            (self.p[self.j] == "(")
            or (self.isVocab(self.p[self.j]))
            or (self.p[self.j] == "\\")
        ):
            self.expression()

        # or did we just leave a parenthesized expression?
        elif self.p[self.j] == ")":
            return startState

        else:
            logging.error(
                "malformed input regex. P = " + self.p + ", J = " + str(self.j)
            )
            exit()

        return startState

    def term(self) -> int:
        """Evaluates a regex term, returning the starting state
        of the term finite state machine
        """

        startState = self.factor()  # get factor start state in r

        # just get outta there without further checks if we've read the entire input pattern
        if self.j >= len(self.p):
            return startState
        else:
            if self.p[self.j] == "*":
                logging.info("term: closure. P = " + self.p + ", J = " + str(self.j))

                # consume the symbol
                self.j += 1

                # build the closure machine;
                # a branching machine with terminal 1 being the
                # start state of the factor, and terminal 2 being
                # whatever comes next
                self.statemachines[self.state] = FSM(
                    self.branchingStateChar, startState, self.state + 1
                )
                self.state += 1
                return startState + 1  # return the beginning of the state we just built

            elif self.p[self.j] == "?":
                logging.info("term: option. P = " + self.p + ", J = " + str(self.j))

                # consume the symbol
                self.j += 1

                # an option is very similar to alernation.
                # we use a branching machine, with the machine's 1st terminal
                # being the state machine of whatever literal preceded the '?',
                # and that state machine's terminal pointing to the branching
                # machine's 2nd terminal
                terminal1 = startState
                branchingState = self.state
                self.state += 1

                self.statemachines[branchingState] = FSM(
                    self.branchingStateChar, terminal1, self.state
                )

                # whatever terminal 2 of the state /before/ the first factor
                # was, redirect it to this new branching state.
                # if it was non-branching, redirect both terminals
                if self.statemachines[startState - 1] is not None:
                    if (
                        self.statemachines[startState - 1].next1
                        == self.statemachines[startState - 1].next2
                    ):
                        self.statemachines[startState - 1].next1 = branchingState
                    self.statemachines[startState - 1].next2 = branchingState

                self.statemachines[terminal1] = FSM(
                    self.statemachines[terminal1].c, self.state, self.state
                )
                return branchingState  # return the beginning of the state we just built

            elif self.p[self.j] == "|":
                logging.info(
                    "term: alternation. P = " + self.p + ", J = " + str(self.j)
                )

                # consume the symbol
                self.j += 1

                # at this point, we've built the FSM for the first
                # factor in the alternation sequence, and we need to
                # build the 2nd one and have both connect to a single
                # final out state. we need a branching machine.
                terminal1 = startState
                branchingState = self.state
                self.state += 1

                # get the starting state of the 2nd term
                terminal2 = self.term()

                self.statemachines[branchingState] = FSM(
                    self.branchingStateChar, terminal1, terminal2
                )

                # whatever terminal 2 of the state /before/ the first factor
                # was, redirect it to this new branching state.
                # if it was non-branching, redirect both terminals
                if self.statemachines[startState - 1] is not None:
                    if (
                        self.statemachines[startState - 1].next1
                        == self.statemachines[startState - 1].next2
                    ):
                        self.statemachines[startState - 1].next1 = branchingState
                    self.statemachines[startState - 1].next2 = branchingState

                self.statemachines[terminal1] = FSM(
                    self.statemachines[terminal1].c, self.state, self.state
                )

                return branchingState  # return the beginning of the state we just built
            return startState

    def factor(self) -> int:
        """Evaluates a regex factor, returning the starting state
        of the factor finite state machine
        """

        # check if we just escaped something i.e. \s
        if self.p[self.j - 1] == "\\":
            logging.info(
                "factor: escaped character found: "
                + self.p[self.j]
                + ". P = "
                + self.p
                + ", J = "
                + str(self.j)
            )

            # build the non-branching state machine
            self.statemachines[self.state] = FSM(self.p[self.j], self.j + 1, self.j + 1)
            self.state += 1
            self.j += 1
            # return the beginning of the state we just built
            return self.state - 1

        # check for v
        if self.isVocab(self.p[self.j]):
            logging.info(
                "factor: vocab found: "
                + self.p[self.j]
                + ". P = "
                + self.p
                + ", J = "
                + str(self.j)
            )

            # build the non-branching state machine
            self.statemachines[self.state] = FSM(
                self.p[self.j], self.state + 1, self.state + 1
            )
            self.j += 1
            self.state += 1
            # return the beginning of the state we just built
            return self.state - 1

        # check for . (wildcard)
        if self.p[self.j] == ".":
            logging.info(
                "factor: vocab found: "
                + self.p[self.j]
                + ". P = "
                + self.p
                + ", J = "
                + str(self.j)
            )

            # build the non-branching state machine
            self.statemachines[self.state] = FSM(
                self.p[self.j], self.state + 1, self.state + 1
            )
            self.j += 1
            self.state += 1
            # return the beginning of the state we just built
            return self.state - 1

        # check for \
        if self.p[self.j] == "\\":
            logging.info(
                "factor: escape char found: "
                + self.p[self.j]
                + ". P = "
                + self.p
                + ", J = "
                + str(self.j)
            )

            # don't build a state machine -- we do that on the next j
            self.j += 1
            return self.state

        # check for (E)
        if self.p[self.j] == "(":
            logging.info(
                "factor: parenthesized expression start. P = "
                + self.p
                + ", J = "
                + str(self.j)
            )

            # consume the input
            self.j += 1
            # get the start state of the parenthesized expression
            startState = self.expression()
            # malformed if there are no closing parentheses
            try:
                if self.p[self.j] != ")":
                    logging.error("malformed input regex")
                    exit()
                else:
                    logging.info("leaving parenthesized expression")
                    self.j += 1
                    return startState

            except Exception:
                logging.error("malformed input regex")
                exit()

    def isVocab(self, c):
        """Checks if a character is == "v" defined in the CFG
        """

        if (c in string.printable) and (c not in self.reservedChars):
            return True
        return False

    def compile(self, input: str):
        """Parses and compiles finite state machines
        from an input regular expression, outputting to stdout
        """

        self.p = input
        logging.info("input regular expression: " + self.p)

        # the length of the FSM array is the length of
        # the input pattern, minus all parentheses
        temp = str.replace(self.p, "(", "")
        statemachineArraySize = len(str.replace(temp, ")", ""))
        self.statemachines = [None] * (statemachineArraySize + 1)

        # start evaluation, and get the initial state number of the entire regex
        initial = self.expression()
        # once we're done with that, create the initial FSM
        # self.statemachines[0] = FSM(self.branchingStateChar, initial, initial)
        self.statemachines[0] = FSM(self.branchingStateChar, initial, initial)

        # tack on a dummy FSM at the end redirecting to initial FSM
        self.statemachines.append(FSM(self.branchingStateChar, 0, 0))

        # print out all the FSMs we compiled to stdout
        for machine in self.statemachines:
            print(machine)


def main():
    REcompiler().compile(input())


main()

