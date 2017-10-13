FROM tensorflow/syntaxnet
#If they ever update this image things will likely break

RUN apt-get install -y netcat

#y_tho.gif
ENV PYTHONPATH="${PYTHONPATH}:/opt/tensorflow/syntaxnet/bazel-bin/dragnn/tools/oss_notebook_launcher.runfiles/__main__:/opt/tensorflow/syntaxnet/bazel-bin/dragnn/tools/oss_notebook_launcher.runfiles/org_tensorflow"

RUN mkdir /src
ADD . /src
RUN pip install -r /src/requirements.txt

CMD ["/src/wait-for", "rabbitmq:5672", "-t", "30", "--", "python", "/src/app.py"]
