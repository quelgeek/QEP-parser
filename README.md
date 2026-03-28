# QEP-parser
**QEP-parser** is an ANTLR-based tool for parsing "concise" Ingres query plans
such as this:
```
QUERY PLAN 3,1, no timeout, of main query | {K Join(customernr) Heap Pages 2 Tups 9 D569 C1425 {Proj-rest Heap Pages 3 Tups 91 D553 C901 {orders (o) Hashed(NU) Pages 567 Tups 90100}}{customers (c) Hashed(customernr) Pages 844 Tups 10000}};
```

## Getting Started
I like Python for rapid development and testing of ideas. The
instructions below assume you will use Python so start by taking
whatever steps you usually take to set up an isolated Python development
environment. I use [conda](https://www.anaconda.com/). You be you. Any 
version of Python from 3.8 onwards should be usable for this project.

(Python is not mandatory. Many other target languages are supported by ANTLR)

## Installing ANTLR



> [!TIP]
> To learn about using ANTLR see [The ANTLR Mega Tutorial](https://tomassetti.me/antlr-mega-tutorial).

You will need to install [ANTLR](https://www.antlr.org). 
ANTLR reads a grammar definintion and generates a lexer and parser
for it, coded in a target language such as Python, Java, C++, etc. 

If you have created a Python environment for this project,
activate it before installing ANTLR.

See [Getting Started with ANTLR v4](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)
for instructions on installing it.
I strongly endorse the suggestion there for "getting started the easy way", 
but it does require Python. 

You also need to install the ANTLR4 Python3 run-time, which is not 
mentioned in the above referenced *Getting Started* guide:
```
pip install antlr4-python3-runtime
```

> [!NOTE]
> If the *antlr4* command fails with a **FileNotFoundError** because
> it could not get the latest version number, a workaround is to:
> ```
> export ANTLR4_TOOLS_ANTLR_VERSION=4.13.2
> ```
> then try again.


## Getting Started with QEP-parser
Activate your environment if you haven't already, 
then clone the project from GitHub:
```
git clone https://github.com/quelgeek/QEP-parser
cd QEP-parser
```

The ANTLR grammar files have a **.g4** suffix.

Generate a lexer, parser, visitor, and
listener from the **QueryPlan.g4** grammar specification:
```
antlr4 -Dlanguage=Python3 QueryPlan.g4 -visitor
```

If there are no errors you will now have the following additional files:
* **QueryPlan.interp**
* **QueryPlanLexer.interp**
* **QueryPlanLexer.py**
* **QueryPlanLexer.tokens**
* **QueryPlanListener.py**
* **QueryPlanParser.py**
* **QueryPlan.tokens**
* **QueryPlanVisitor.py**

The new **.py** files can be used to develop Python-based tools to
interpret and report concise Ingres query execution plans.
