<p align="center">
  <img src="./assets/imgs/tiny-drive-logo.svg" />
</p>

# Welcome to **Tiny Drive**

Tiny Drive in a personal project to create google's drive concept \
Provides a online plataform for saving files and folders, you can access them on every device

You can access and test the project on [Tiny Drive](https://tiny-drive.vercel.app/login)

# How to download

First you will need to clone the project into your machine or virtual environment

```bash
git clone https://github.com/RobertSDM/be-tiny-drive.git
```

Once the download completed, go into the directory

```bash
cd be-tiny-drive
```

Create the virtual environment for the project

```bash
python -m venv venv
```

Install the project dependencies in the requirements file

```bash
pip install -r requirements.txt
```

This project has some environment varibles, they are: \
`DATABASE_URL` = The frontend base url (in your case must be "http://localhost:5173") \
`PORT` = The backend base url \
`ORIGINS` = Origins to be allowed on CORS \
`SECRET_KEY` = Secret

# Execution

Initialize the backend project using the makerfile command: \

```bash
# if you're not using the venv or if already activated the venv
make run
# if you want to run and enter the venv
make env-run
```

# API

## <a id="file"></a>File `/file`

1. [Folder](#folder)
2. [Content](#content)
3. [Auth](#auth)

`POST`

#### /save

| HTTP | Description                              |
| ---- | ---------------------------------------- |
| 200  | If success return the created file       |
| 422  | If the file already exists in the folder |
| 500  | If error while saving the file           |

`GET`

#### /download/{id}/{owner_id}

| HTTP | Description      |
| ---- | ---------------- |
| 200  | Return the bytes |

`PUT`

#### /update/name/{id}/{owner_id}

| HTTP | Description                              |
| ---- | ---------------------------------------- |
| 200  | If success on update the name            |
| 422  | If the name already exists in the folder |
| 500  | If error while update name               |

`DELETE`

#### /delete/{id}/{owner_id}

| HTTP | Description                |
| ---- | -------------------------- |
| 200  | If success on delete file  |
| 500  | If error while delete file |

## <a id="folder"></a>Folder `/folder`

### Pricipais rotas

1. [File](#file)
2. [Content](#content)
3. [Auth](#auth)

`POST`

#### /save

| HTTP | Description                                |
| ---- | ------------------------------------------ |
| 200  | If success return the created folder       |
| 422  | If the folder already exists in the folder |
| 500  | If error while saving the folder           |

`GET`

#### /donwload/zip/{id}/{owner_id}

| HTTP | Description             |
| ---- | ----------------------- |
| 200  | Return the zip as bytes |

`PUT`

#### /update/name/{id}/{owner_id}

| HTTP | Description                              |
| ---- | ---------------------------------------- |
| 200  | If success on update the name            |
| 422  | If the name already exists in the folder |
| 500  | If error while update name               |

`DELETE`

#### /delete/{id}/{owner_id}

| HTTP | Description                  |
| ---- | ---------------------------- |
| 200  | If success on delete folder  |
| 500  | If error while delete folder |

## <a id="content"></a>Content `/content`

### Pricipais rotas

1. [File](#file)
2. [Folder](#folder)
3. [Auth](#auth)

`GET`

#### /all/{owner_id}

| HTTP | Description                                      |
| ---- | ------------------------------------------------ |
| 200  | Return all the files and folders with pagination |
| 204  | If no content was found                          |

#### /by/folder/{owner_id}

| HTTP | Description                                      |
| ---- | ------------------------------------------------ |
| 200  | Return all the files and folders with pagination |
| 204  | If no content was found                          |

#### /search/{owner_id}

| HTTP | Description                            |
| ---- | -------------------------------------- |
| 200  | Return all the files and folders found |
| 204  | If no content was found                |

## <a id="auth"></a>Auth `/auth`

### Pricipais rotas

1. [File](#file)
2. [Folder](#folder)
3. [Content](#content)

`POST`

#### /login

| HTTP | Description                        |
| ---- | ---------------------------------- |
| 200  | Return the user and the jwt        |
| 400  | If email or password are incorrect |

#### /register

| HTTP | Description                      |
| ---- | -------------------------------- |
| 200  | If success on create user        |
| 400  | If the email already exists      |
| 500  | If error while creating the user |

## Technologies

### Frameworks

-   Vite.js (frontend)
-   Fastapi (backend)

### Libraries

-   React.js (frontend)
-   Typescript (frontend)
-   Tailwind (frontend)
-   Axios (frontend)
-   Bcrypt (backend)
-   SQLAlchemy (backend)
-   Logger (backend)
-   Uvicorn (backend)

### Database

-   PostgreSQL (Hosted on Neon)

### Host Services

-   Vercel (frontend)
-   Azure (backend)
