# python-aws-foundation

Python script using Boto3 to check your conformity against [CIS Amazon Web Services Foundations](https://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf) benchmark.

This is currently a **Work in Progress**

# Features

For the moment, we're just displaying the results of the test.

TODO :
- [] Cover every tests in the CIS Benchmark
- [] Find a way to check for a specific section or task only
- [] Manage errors (boto configuration, )

# Installation

This script uses [Boto3](https://github.com/boto/boto3#boto-3---the-aws-sdk-for-python).
You can either use the [Quick Start](https://github.com/boto/boto3#quick-start) described there, or install the `awscli` package.

Using `awscli` :
```
$ sudo apt-get install awscli
$ aws configure
```
It will prompt an interactive shell, asking you couples of informations regarding your AWS Account.


# Usage

This is a basic python script, so simply type the following :
```
python python-aws-foundation.py
```

# Contribute

You can contribute in several ways :
  - report issues : [issue tracker](https://github.com/SpoonBoy/python-aws-foundation/issues)
  - make Pull requests to add new tests

# Support

If you are having issues, please let me know.
I didn't set up an irc channel or anything, so for the moment we'll use with issues

# License
