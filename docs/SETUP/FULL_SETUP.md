# Setup Instructions

## Overview

If you plan to contribute to both front and back end development for Clean & Green Philly, follow the installation and setup instructions below.

## Installation

### Docker

Docker is a platform that allows you to containerize and run applications in isolated environments, making it easier to manage dependencies and ensure consistent deployments. Download the [latest version of Docker Desktop for your operating system](https://www.docker.com/products/docker-desktop/).

### PostgreSQL

PostgreSQL is an open-source relational database management system. We use it to store and our data. Make sure you have the latest version of PostgreSQL installed on your computer. You can download it [here](https://www.postgresql.org/download/). As part of that setup, you will also need to install PostGIS; this should be done through the setup wizard, [as detailed here](https://postgis.net/workshops/postgis-intro/installation.html).

### NVM (Windows Only)

If you are running Windows, you will need to [install NVM for Windows](https://github.com/coreybutler/nvm-windows/blob/master/README.md). Under 'Assets', [nvm-setup.exe](https://github.com/coreybutler/nvm-windows/releases) is straightforward. Node.js and nvm ship with Linux and macOS and therefore do not need to be installed for people using those OS.

## Setup

### Fork the Repository

1. Navigate to [our GitHub repository](https://github.com/CodeForPhilly/vacant-lots-proj).
2. Create a fork of the repository by clicking the "Fork" button in the top right corner of the page. This will create a copy of the repository in your own GitHub account.
3. Clone your fork of the repository to your local machine using `git clone`.

Note: make sure to keep your fork up to date with the original repository by following the instructions [here](https://docs.github.com/en/get-started/quickstart/fork-a-repo#keep-your-fork-synced).

### Create a New Database

#### Windows

1. Using powershell, navigate to the directory where PostgreSQL is installed. You can do this with a command like cd `"C:\Program Files\PostgreSQL\13\bin"` (replace 13 with your PostgreSQL version). Run `./psql -U postgres`. Enter your computer password.
2. Run `CREATE DATABASE vacantlotdb;` to create a new database named `vacantlotdb`.
3. Run `\c vacantlotdb` to connect to the database.
4. Run `CREATE EXTENSION postgis;`.
5. Run `\q` to exist PostgreSQL.

### Linux

1. Ensure that PostgreSQL is installed and running on your Mac.
2. In your terminal, run `createdb vacantlotdb`. This command directly creates a new database named `vacantlotdb`.
3. Run `psql -U postgres -d vacantlotdb`. Enter the password when prompted. This command opens the PostgreSQL command line interface and connects you to the `vacantlotdb` database.
4. Run `CREATE EXTENSION postgis;`
5. Run `\q` to exit the PostgreSQL command line interface.

### macOS

1. Ensure that PostgreSQL is installed and running on your Mac.
2. In your terminal, run `createdb vacantlotdb`. This command directly creates a new database named `vacantlotdb`.
3. Run `psql -d vacantlotdb`. Note that you might need to start postgres on mac: `brew services start postgresql` before running psql If prompted, enter the password for your PostgreSQL user. This will open the PostgreSQL command line interface and connect you to the `vacantlotdb` database. You will know it’s succeeded when you see `vacantlotdb=#`
4. Run `CREATE EXTENSION postgis;`
5. To exit the PostgreSQL interface, type `\q` and press Enter.

Note for all OS: Optionally, in `/config/config`, set `FORCE_RELOAD` = `False` to read "cached" data in postgres instead of downloading new data.

### Set Environment Variables

#### Windows

Open the command prompt as an admin. Run `setx VACANT_LOTS_DB "postgresql://postgres:password@localhost/vacantlotdb"`. Make sure to replace “password” with your user password (not your postgres password). You should get a message saying something like “Success! Specified value was saved.”

#### Linux

In the terminal, open your shell's profile file, like `~/.bashrc` or `~/.bash_profile`, using a text editor. You should be able to do this by running something like `nano ~/.bashrc`. Add the following lines at the end of the file:
`export VACANT_LOTS_DB="postgresql://postgres:password@localhost/vacantlotdb"`
Replace `password` with your PostgreSQL user password. Save and close the file. Apply the changes by running `source ~/.bashrc`.

#### macOS

In the terminal, open your shell's profile file, such as `~/.zshrc` (for Zsh, which is the default shell on recent versions of macOS) or `~/.bash_profile` (for Bash), using a text editor like Nano or Vim. For instance, `nano ~/.zshrc`. Add the following lines at the end of the file
`export VACANT_LOTS_DB="postgresql://postgres:password@localhost/vacantlotdb"`
Make sure to replace `password` with your actual PostgreSQL password. Save and close the file. To apply these changes, run `source ~/.zshrc` (or the appropriate file for your shell).

Note for all OS: you can choose to write to local, remote, both, or neither in the settings in `config.py`

### Docker Build

All of the data scripting is in python and lives in the `data` folder. Everything below should be run in that folder.

For all three OS, you'll first have to go into the `data` subdirectory and open the `docker-compose.yml` file. Change the filepath under `volumes` to the location of your repository. (Currently it is hardcoded to Brandon's filepath.)
For example, if your repository is located at `user/Documents/vacant-lots-proj`, you would change the filepath to `user/Documents/vacant-lots-proj/data`. Save and close the file. Alternatively, you can run the image in Docker following the steps below. If needed, it will build (this will take a few minutes). It should only need to build if it's your first time running or if major configuation changes are made. Changes to the python script should not trigger a re-build.

#### Windows

1. Make sure Docker is running by opening the Docker Desktop app.
2. Open the command prompt. Navigate to the location of the `vacant-lots-proj` repository. Run `cd data` and then `docker-compose run vacant-lots-proj`.
3. When the script is done running, you’ll get a notification. When you’re done, to shut up off the Docker container (which uses memory), run `docker-compose down`.

#### Linux

1. In the terminal, navigate to your repository location using `cd path/to/repository`. Then run `cd data` to move into the `data` directory.
2. Run `sudo docker-compose run vacant-lots-proj`. Enter your password if requested. If you run into an error message related to "KEY_ID" or something like similar, you may have to do the following:

- Hard-code your VACANT_LOTS_DB variable in `docker-compose.yml`.
- Also in `docker-compose.yml`, add `extra_hosts: -"host.docker.internal:host-gateway"`
- In your `postgresql.conf` file, set `listen_addresses = '*'` in
- In your `pg_hba.conf` file, add the following new lines: `host all all 10.0.0.0/24 md5` and `host all postgres 172.18.0.2/32 trust`. You may have to modify these based on your own IP address.
- Finally, after restarting postgres, navigate back to the `data` subdirectory in the project and run `docker-compose --verbose up -d`. This should run successfuly; message

3. When you're finished, and you want to shut down the Docker container, run `docker-compose down`.

#### macOS

In the terminal, use the `cd` command to navigate to your repository location, and then into the `data` directory. Run `docker-compose run vacant-lots-proj`. This command starts Docker Compose and sets up your environment as defined in your `docker-compose.yml` file. When you're finished and want to shut down the Docker containers, run `docker-compose down`.

### Nextjs App

Finally, it's time to run the Nextjs app. Navigate to the root directory of the repository. Install dependencies by running `npm i`. Then, run the development server with `npm run dev`. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result. Congrats! You're all set up.

### MapTiler

You'll need to set up a free [MapTiler](https://www.maptiler.com/) and get an API key. Once you have this, set it as en environment variable called `NEXT_PUBLIC_MAPTILER_KEY`.

#### Formatting

For js/ts, install [Prettier](https://prettier.io/) and enable it for your [editor](https://prettier.io/docs/en/editors.html). For VSCode, enable [Format on Save](https://www.robinwieruch.de/how-to-use-prettier-vscode/) for best experience.

Format all python files by running:

```
docker-compose run formatter
```

#### Google Cloud

The map data is converted to the [pmtiles](https://docs.protomaps.com/pmtiles/) format and served from Google Cloud. For access to production credentials, contact the project lead. If you'd like to test the tile build locally, create your own credentials using their free trial.
