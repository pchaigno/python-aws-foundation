# python-aws-foundation

Python script using Boto3 to check your conformity against [CIS Amazon Web Services Foundations](https://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf) benchmark.

#### This is currently a **Work in Progress**

# Features

For the moment, we're just displaying the results of the test.

TODO :
- [ ] Cover every tests in the CIS Benchmark
- [x] Find a way to check for a specific section only, or several at once.
- [ ] Find a way to check for a specific task only
- [x] Manage errors (boto configuration, missing reports ... )

# Installation

This script uses [Boto3](https://github.com/boto/boto3#boto-3---the-aws-sdk-for-python).
You can either use the [Quick Start](https://github.com/boto/boto3#quick-start) described there, or install the `awscli` package.

Using `aws configure`, it will prompt an interactive shell, asking you couples of informations regarding your AWS Account :
```
$ sudo apt-get install awscli
$ aws configure
AWS Access Key ID [********************]: ALongString
AWS Secret Access Key [********************]: AnOtherVeryLongString
Default region name [eu-central-1]: eu-central-1  # your region id
Default output format [json]: json                # text is an other possible value
```


# Usage

This is a basic python script, so simply type the following :
```
python python-aws-foundation.py {{Section number(s) to test}}
```
with `{{Section numbers to test}}` being a section number in the Benchmark PDF.

So if you want to check `Identify and Access Management`, which is section number 1 in the PDF, you will have to type the following command :
```
python python-aws-foundation.py 1
```

#### Note :
As mentionned before, it is still a WIP, therefore all sections are not yet available.

# Contribute

You can contribute in several ways :
  - report issues : [issue tracker](https://github.com/SpoonBoy/python-aws-foundation/issues)
  - make Pull Requests to add new tests. We will provide a CONTRIBUTING.md in a near future.

# Support

If you are having issues, please let me know.
I didn't set up an irc channel or anything, so for the moment we'll use the github issues.

# License
MIT License (MIT)
