## COMPX301-20A   Assignment 2:  Pattern Searching

This assignment is intended to give you experience building a regular expression (regexp) FSM compiler and corresponding pattern matcher. Students are to work in pairs to complete this assignment (n.b. I encourage new partnerships, but I do not insist on it). Your implementation is expected to be written in Java, and compile and run on a Linux machine such as those in the R Block labs. Deviation from this specification requires prior approval from the lecturer or tutor.

**Due:  Thursday, 7 May 2020, 11:30pm**

**Overview:**     Implement a regexp pattern searcher using the FSM, deque and compiler techniques outlined in lectures. Your solution must consist of two programs: one called REcompile.java and the other called REsearch.java. The first of these must accept a regexp pattern as a command-line argument (enclosed within double-quotes—see "**Note**" below), and produce as standard output a description of the corresponding FSM, such that each line of output includes four things: the state-number, the character to be matched (I recommend as an int value so you can always read it) or branch-state indicator (however you like), and two numbers indicating the two possible next states. The second program must accept, as standard input, the output of the first program, then it must execute a search for matching patterns within the text of a file whose name is given as a command-line argument. Each line of the text file that contains a match is output to standard out just once, regardless of the number of times the pattern might be satisfied in that line. (Note, we are just interested in searching text files.)

**Regexp specification:**     For this assignment, a wellformed regexp is specified as follows:

1.  any symbol that does not have a special meaning (as given below) is a literal that matches itself
2.  . is a _wildcard_ symbol that matches any literal
3.  adjacent regexps are concatenated to form a single regexp
4.  \* indicates closure (zero or more occurrences) on the preceding regexp
5.  ? indicates that the preceding regexp can occur zero or one time
6.  | is an infix alternation operator such that if _r_ and _e_ are regexps, then _r|e_ is a regexp that matches one of either _r_ or _e_
7.  ( and ) may enclose a regexp to raise its precedence in the usual manner; such that if _e_ is a regexp, then _(e)_ is a regexp and is equivalent to _e_. _e_ cannot be empty.
8.  \ is an escape character that matches nothing but indicates the symbol immediately following the backslash loses any special meaning and is to be interpretted as a literal symbol
9.  operator precedence is as follows (from high to low):
    *   escaped characters (i.e. symbols preceded by \)
    *   parentheses (i.e. the most deeply nested regexps have the highest precedence)
    *   repetition/option operators (i.e. * and ?)
    *   concatenation
    *   alternation (i.e. |)

You must implement your own parser/compiler, and your own FSM (simulating two-state and branching machines) similar to how it was shown to you in lectures, and you must implement your own dequeue to support the search.

Note that you should make sure you have a good grammar before you start programming, so take time to write out the phrase structure rules that convince you that your program will accept all and only the regular expressions you deem legal. Anything not explicitly covered by this specification may be handled any way you want. For example, you can decide if a** is a legal expression or not. And it is okay to preprocess the expression before trying to compile it, if such preprocessing simplifies what you are trying to do. For example, you could decide to replace any ** with just * if you want ** to be legal.

Observe also that REsearch can be developed in parallel to REcompile simply by working out the states of a valid FSM by hand and testing with that.

**Note:**     Operating system shells typically parse command-line arguments as regular expressions, and some of the special characters defined for this assignment are also special characters for the command-line interpreter of various operating systems. This can make it hard to pass your regexp into the argument vector of your program. You can get around most problems by simply enclosing your regexp command-line argument within double-quote characters, which is what you should do for this assignment. To get a double-quote character into your regexp, you have to escape it by putting a backslash in front of it, and then the backslash is removed by the time the string gets into your program's command-line argument vector. There is only one other situation where Linux shells remove a backslash character from a quoted string, and that is when it precedes another backslash. For this assignment, it is the string that gets into your program that is the regexp—which may entail some extra backslashes in the argument. (N.b. Windows command prompt shell has a different syntax for parsing regexps than does Linux, so if you develop on a windows box, make sure you make the necessary adjustments for it to run under linux.)

**Submission:**       Place only copies of your well-documented, well-formatted source code and any README text file in an otherwise empty folder/directory whose name is your student ID number and the student ID number of your partner separated with an underscore, then compress it and submit through Moodle as per usual. I recommend including your grammar as a set of phrase structure rules in the README file or in the header of your compiler to assist in marking. See your tutor for details.  

  <font size="-1">Tony C Smith, Apr 2020</font>
