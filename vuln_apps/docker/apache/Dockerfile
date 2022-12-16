FROM httpd:2.4.51

COPY apache.conf /usr/local/apache2/conf/apache.conf

RUN echo "Include /usr/local/apache2/conf/apache.conf" \
    >> /usr/local/apache2/conf/httpd.conf