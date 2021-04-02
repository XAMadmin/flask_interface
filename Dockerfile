FROM python:3-slim
​
ADD ./  /code
​
WORKDIR /code
​
RUN apt-get update
RUN apt-get install -y nginx supervisor
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip3 config set install.trusted-host pypi.tuna.tsinghua.edu.cn
RUN pip3 install -r requirements.txt
​
# 时区设置
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo 'Asia/Shanghai' >/etc/timezone
​
# 端口
EXPOSE 3340

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx_flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx_flask.conf /etc/nginx/sites-enabled/nginx_flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# CMD ["python3", "/code/app.py"]  py文件启动方式
​CMD ["/bin/bash"]
# gunicorn 启动
ENTRYPOINT ["gunicorn", "--config", "gunicorn.conf.py", "manage:app"]