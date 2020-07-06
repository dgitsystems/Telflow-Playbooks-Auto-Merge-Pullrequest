FROM python:3-alpine

MAINTAINER DGIT Systems <devops@dgitsystems.com>

LABEL "com.github.actions.name"="Auto-merge my pull requests"
LABEL "com.github.actions.description"="Merge and clean-up the pull request after the checks pass"
LABEL "com.github.actions.icon"="activity"
LABEL "com.github.actions.color"="green"

COPY requirements.txt /requirements.txt
RUN	pip3 install -r /requirements.txt

COPY approve_and_merge_for_user.py /approve_and_merge_for_user.py

ENTRYPOINT ["python3", "/approve_and_merge_for_user.py"]
