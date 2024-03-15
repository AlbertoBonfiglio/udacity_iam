# Backend - IAM API

The following provides detailed documentation of the backend API endpoints including the URL, request parameters, and the response body.

## Table Of Content <!-- omit from toc -->
- [Backend - IAM API](#backend---iam-api)
  - [Endpoints](#endpoints)
    - [`GET '/api/v1.0/drinks'`](#get-apiv10drinks)
    - [`GET '/api/v1.0/drinks-details'`](#get-apiv10drinks-details)
    - [`POST '/api/v1.0/drinks'`](#post-apiv10drinks)
    - [`PATCH '/api/v1.0/drinks'`](#patch-apiv10drinks)
    - [`DELETE '/api/v1.0/drinks'`](#delete-apiv10drinks)

## Endpoints

### `GET '/api/v1.0/drinks'`

- Fetches an array of category objects in which the ids are the categories ids and the type is the corresponding string of the category
- Request Arguments: None
- Usage example: `http://127.0.0.1:5000/api/v1.0/drinks` 
- Returns: An object with a key, `data`, that contains an array of objects with  `id: key, type: string` attributes, and a `success` boolean key.

```json
{
    "drinks": [
        {   "id": 1, "type": "Science" },
        {   "id": 2, "type": "Art" },
        {   "id": 3, "type": "Geography" },
        {   "id": 4, "type": "History" },
        {   "id": 5, "type": "Entertainment" },
        {   "id": 6, "type": "Sports" }
    ],
    "success": true
}
```
---

### `GET '/api/v1.0/drinks-details'`

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
