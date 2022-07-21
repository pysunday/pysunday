FROM python:2.7.18

ENV LANG C.UTF-8
ENV SUNDAY_PATH=/root/sunday
ADD ./ $SUNDAY_PATH

WORKDIR $SUNDAY_PATH

RUN mkdir ~/.pip
RUN cp $SUNDAY_PATH/static/pip.conf ~/.pip
RUN python $SUNDAY_PATH/setup.py install

ENV PATH="/root/.sunday/bin:${PATH}"

# CMD ["/bin/bash"]