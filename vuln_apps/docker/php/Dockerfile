FROM php:8.1-fpm

RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
RUN echo "extension=mongodb.so" >> "$PHP_INI_DIR/php.ini"

RUN apt-get update \
    && apt-get install -y libcurl4-openssl-dev pkg-config libssl-dev \
    && apt-get install -y git zip unzip \
    && pecl install mongodb \
    && php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" \
    && php composer-setup.php --install-dir=/usr/local/bin --filename=composer \
    && rm composer-setup.php \
    && composer require mongodb/mongodb