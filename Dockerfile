FROM python:3.10-alpine

# upgrade pip
RUN pip install --upgrade pip

# permissions and nonroot user for tightened security
RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
WORKDIR /home/app
USER nonroot

# copy all the files to the container
COPY --chown=nonroot:nonroot /requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY --chown=nonroot:nonroot /src /home/app/

RUN export FLASK_APP=app.py

# define the port number the container should expose
EXPOSE 5000

HEALTHCHECK --interval=3s --timeout=3s --start-period=3s --retries=3 \
    CMD ["wget", "--no-verbose", "--tries=1", "--spider", "http://127.0.0.1:5000/health"]

CMD ["python", "wsgi.py"]
