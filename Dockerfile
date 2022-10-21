FROM public.ecr.aws/lambda/python:3.9 as build

RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/106.0.5249.61/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1036826%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/

FROM public.ecr.aws/lambda/python:3.9 as run

RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y

COPY app.py ${LAMBDA_TASK_ROOT}
COPY scraper ${LAMBDA_TASK_ROOT}

ENV POETRY_HOME=/opt/poetry
RUN python3 -m venv $POETRY_HOME

RUN $POETRY_HOME/bin/pip install poetry==1.2.0

RUN $POETRY_HOME/bin/poetry --version

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | pip3 install -r /dev/stdin --target "${LAMBDA_TASK_ROOT}"

COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt

CMD ["app.handler"]

