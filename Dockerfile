#base image
FROM python:3.9

#set timezone to Eastern
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#set up working directory
WORKDIR /code

#install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

#copy over code
COPY vault_cleaner/ ./vault_cleaner

#command to run
COPY run.py .
CMD [ "python", "./run.py" ]
