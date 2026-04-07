#!/usr/bin/env bash

if ! command -v openssl &> /dev/null; then
    echo "openssl not installed. installing..."
    DISTRO = "$(source /etc/os-release && echo $PRETTY_NAME)"
    if ["$DISTRO" = "Arch Linux"]; then
        sudo pacman -Syy openssl    
    fi
fi
set -e

echo "Creating .env file..."

if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env created. Enter Telegram token for your bot."
    read -p "" TELEGRAM_TOKEN
    DJANGO_KEY="$(openssl rand -base64 48)"
    POSTGRES_PASSWORD="$(openssl rand -hex 16)"
    sed -i "1s|changeme|$TELEGRAM_TOKEN|g" .env 
    sed -i "2s|changeme|$DJANGO_KEY|g" .env
    sed -i "3s|changeme|$POSTGRES_PASSWORD|g" .env
else
    echo ".env already exists"
fi

mkdir -p syzygy

cd syzygy

if [ echo $(ls ./syzygy) = "" ]; then
    echo "Downloading Syzygy 3-4-5 tablebases..."
    wget -e robots=off -r -np -nH --cut-dirs=2 -R "index.html*" http://tablebase.sesse.net/syzygy/3-4-5/
fi

cd ..

sudo docker compose up --build
