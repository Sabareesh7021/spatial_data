# Spatial Data Management Platform

This is a **FastAPI + GraphQL + MongoDB** project for managing spatial data, including points and polygons. It provides APIs to store, update, and retrieve spatial data using GraphQL.

---

## 🚀 Features

- **Points**: Store and manage point data with latitude and longitude.
- **Polygons**: Store and manage polygon data with a list of coordinates.
- **GraphQL API**: Perform queries and mutations using GraphQL.
- **MongoDB**: Store spatial data in a MongoDB database.
- **Dockerized**: Easy setup and deployment using Docker.

---

## 📌 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Git**: [Install Git](https://git-scm.com/downloads)

---

## 🛠 Setup

### 1️⃣ Clone the Repository

Clone the project repository to your local machine:

```bash
git clone <repository-url>
cd spatial-data-platform
```

### 2️⃣ Set Up Environment Variables

Copy the `.env.example` file to `.env` and update the environment variables as needed:

```bash
cp .env.example .env
```

Edit the `.env` file to configure your MongoDB connection and other settings.

### 3️⃣ Build the Docker Image

Build the Docker image for the application:

```bash
docker build -t spatial_data:0.1 .
```

This will create a Docker image named `spatial_data` with the tag `0.1`.

### 4️⃣ Deploy the Stack

Deploy the Docker stack using Docker Compose:

```bash
docker stack deploy -c docker-compose.yml stack_name
```

This will start the following services:

- **FastAPI + GraphQL API** (running on port **8000**)
- **MongoDB** (running on port **27017**)

---

## ▶️ Running the Application

### 🎯 Access the GraphQL Playground

Once the stack is running, you can access the **GraphQL Playground** at:

🔗 [http://localhost:8000/graphql](http://localhost:8000/graphql)

The GraphQL Playground is an interactive IDE where you can test your queries and mutations.

---

## 📊 GraphQL API

### 📌 Queries

#### Get a Point by ID
```graphql
query {
  getPoint(id: "<point_id>") {
    id
    name
    description
    location {
      latitude
      longitude
      latitudeDelta
      longitudeDelta
    }
    categories
  }
}
```

#### Get Points in a Region
```graphql
query {
  getPointsInRegion(latitude: 12.97, longitude: 77.59, latitudeDelta: 0.01, longitudeDelta: 0.01, categories: ["Park", "Restaurant"]) {
    id
    name
    location {
      latitude
      longitude
    }
  }
}
```

#### Get a Polygon by ID
```graphql
query {
  getPolygon(id: "<polygon_id>") {
    id
    geometry {
      type
      coordinates
    }
    category
  }
}
```

#### Get Polygons in a Region
```graphql
query {
  getPolygonsInRegion(minLat: 12.96, minLon: 77.58, maxLat: 12.98, maxLon: 77.60) {
    id
    geometry {
      type
      coordinates
    }
  }
}
```

### 📌 Mutations

#### Create a Point
```graphql
mutation {
  createPoint(point: {
    name: "My Point"
    description: "This is a test point"
    location: { latitude: 12.97, longitude: 77.59, latitudeDelta: 0.01, longitudeDelta: 0.01 }
    categories: ["Park"]
  }) {
    id
    name
    description
  }
}
```

#### Update a Point
```graphql
mutation {
  updatePoint(id: "<point_id>", point: {
    name: "Updated Point"
    description: "Updated description"
    location: { latitude: 12.97, longitude: 77.59, latitudeDelta: 0.02, longitudeDelta: 0.02 }
    categories: ["Museum"]
  }) {
    id
    name
    description
  }
}
```

#### Create a Polygon
```graphql
mutation {
  createPolygon(polygon: {
    coordinates: [[
      { latitude: 12.96, longitude: 77.58 },
      { latitude: 12.98, longitude: 77.58 },
      { latitude: 12.98, longitude: 77.60 },
      { latitude: 12.96, longitude: 77.60 },
      { latitude: 12.96, longitude: 77.58 }
    ]]
    fillColor: "#FF0000"
    strokeColor: "#000000"
    strokeWidth: 2
    tappable: true
    zIndex: 1
    category: "Restricted Zone"
  }) {
    id
    category
  }
}
```

#### Update a Polygon
```graphql
mutation {
  updatePolygon(id: "<polygon_id>", polygon: {
    coordinates: [[
      { latitude: 12.96, longitude: 77.58 },
      { latitude: 12.98, longitude: 77.58 },
      { latitude: 12.98, longitude: 77.60 },
      { latitude: 12.96, longitude: 77.60 },
      { latitude: 12.96, longitude: 77.58 }
    ]]
    fillColor: "#00FF00"
    strokeColor: "#FFFFFF"
    strokeWidth: 1
    tappable: false
    zIndex: 2
    category: "Public Park"
  }) {
    id
    category
  }
}
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Contributing

We welcome contributions! Feel free to open an issue or submit a pull request.

---

## 📞 Support

For any issues, please contact sabareesh9961@gmail.com.

