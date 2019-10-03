FROM lambci/lambda:build-python3.6

ENV AWS_DEFAULT_REGION ap-northeast-1
ENV APP_DIR /app
ENV TASK_DIR /var/tmp
ENV FILE_NAME deploy_package.zip

WORKDIR ${APP_DIR}

CMD touch ${FILE_NAME} && \
  rm ${FILE_NAME} && \
  cp * ${TASK_DIR} && \
  cd ${TASK_DIR} && \
  pip install -r requirements.txt -t ${TASK_DIR} && \  
  zip -r9 ${FILE_NAME} * && \
  cp ${FILE_NAME} ${APP_DIR}