# SummarizeSlackGPT

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  

## **Install**

Clone the repo and execute the following command:

```
make build-prod
```

But if you want to do it manual you can use:

```
python -m venv env
source env/bin/activate
python -m pip install -r requirements/base.txt
```

Then fill the .env file with your api_keys


# **Description**

## Commands

- Summary
- Topics
- Feelings
- Report
- Help

In each command (except help) you can add the following extra arguments:
-Date:string : To filter the messages after that date
-User mentions:string|list :  To filter the messages for user.

## Examples

- @SummarizeGPT summary 11/06/2023 -> Summarize the messages from that date to now.
- @SummarizeGPT summary 11/06/2023 @PepeFrog -> Summarize the filtered pepefrog messages from that date to now.

![Example](https://i.imgur.com/fTuu7Mk.png)
