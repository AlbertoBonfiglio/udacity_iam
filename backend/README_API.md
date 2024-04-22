# Backend - IAM API

The following provides detailed documentation of the backend API endpoints including the URL, request parameters, and the response body.

## Table Of Content <!-- omit from toc -->
- [Backend - IAM API](#backend---iam-api)
  - [Models](#models)
  - [Endpoints](#endpoints)
    - [`GET '/api/v1.0/drinks'`](#get-apiv10drinks)
    - [`GET '/api/v1.0/drinks-details'`](#get-apiv10drinks-details)
    - [`POST '/api/v1.0/drinks'`](#post-apiv10drinks)
    - [`PATCH '/api/v1.0/drinks'`](#patch-apiv10drinks)
    - [`DELETE '/api/v1.0/drinks'`](#delete-apiv10drinks)

## Models

There is one model in the app, the Drink model which has `id: key, title: string  recipe: json[]` attributes. The recipes are json objexts in the format of `name: string, color: string, parts: integer`  

## Endpoints

### `GET '/api/v1.0/drinks'`

- Fetches an array of drink objects in short format 
- Request Arguments: None
- Permissions: public
- Usage example: `http://127.0.0.1:5000/api/v1.0/drinks` 
- Returns: An object with a key, `drinks`, that contains an array of objects with  `id: key, recipe: json[]` attributes. The recipes are json objexts in the format of `name: string, ingredient: string, parts: integer`

```json
{
 "drinks": [
    {
        "id": 1,
        "recipe": [
            {
                "color": "Misty Rose",
                "parts": 1
            },
            {
                "color": "White Smoke",
                "parts": 4
            }
        ],
        "title": "subject sure find"
    },
    {
        "id": 2,
        "recipe": [
            {
                "color": "Seashell",
                "parts": 5
            },
            {
                "color": "Dark Red",
                "parts": 2
            }
        ],
        "title": "kid about cultural"
    },
    ...
}
```
---

### `GET '/api/v1.0/drinks-details'`

- Fetches an array of category objects in long format
- Request Arguments: None
- Permissions: requires the `get:drinks-detail` role from the Auth token
- Usage example: `http://127.0.0.1:5000/api/v1.0/drinks-details` 

```json
{
    "drinks": [
        {   "id": 1, "type": "Science" },
    ],
    "success": true
}
```
---

### `POST '/api/v1.0/drinks'`

- Fetches an array of category objects in which the ids are the categories ids and the type is the corresponding string of the category
- Request Arguments: None
- Usage example: `http://127.0.0.1:5000/api/v1.0/drinks` 
- Returns: An object with a key, `data`, that contains an array of objects with  `id: key, type: string` attributes, and a `success` boolean key.

```json
{
    "drinks": [
        {   "id": 1, "type": "Science" },
    ],
    "success": true
}
```
---

### `PATCH '/api/v1.0/drinks'`

- Fetches an array of category objects in which the ids are the categories ids and the type is the corresponding string of the category
- Request Arguments: None
- Usage example: `http://127.0.0.1:5000/api/v1.0/drinks-details` 
- Returns: An object with a key, `data`, that contains an array of objects with  `id: key, type: string` attributes, and a `success` boolean key.

```json
{
    "drinks": [
        {   "id": 1, "type": "Science" },
    ],
    "success": true
}
```
---


### `DELETE '/api/v1.0/drinks'`

- Fetches an array of category objects in which the ids are the categories ids and the type is the corresponding string of the category
- Request Arguments: None
- Usage example: `http://127.0.0.1:5000/api/v1.0/drinks-details` 
- Returns: An object with a key, `data`, that contains an array of objects with  `id: key, type: string` attributes, and a `success` boolean key.

```json
{
    "drinks": [
        {   "id": 1, "type": "Science" },
    ],
    "success": true
}
```
---
