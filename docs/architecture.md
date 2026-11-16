# LakshyaX deployment architecture

The public site is served by Django and Gunicorn on a Lubuntu host. Docker Swarm runs the app and the Cloudflare Tunnel connector as separate services. SQLite lives on a persistent Docker volume.

## How a request reaches the app

```mermaid
flowchart LR
    Visitor["Visitor browser"]
    Edge["Cloudflare edge"]
    subgraph Host["Lubuntu host running Docker Swarm"]
        Connector["cloudflared connector"]
        App["Gunicorn and Django"]
        Data[("SQLite on a persistent Docker volume")]
        Connector -->|"HTTP on private Docker network"| App
        App <-->|"Read and write"| Data
    end
    Visitor <-->|"HTTPS at lakshyax.focuskey.xyz"| Edge
    Connector <-->|"Traffic over the outbound tunnel"| Edge
```

The browser connects to Cloudflare over HTTPS. The connector initiates the tunnel from inside the host and receives matching requests over that connection. It forwards each request to Django over the private Docker network. The public address belongs to the site, and the Swarm stack publishes zero ports on the host.

## Connection setup and request flow

```mermaid
sequenceDiagram
    participant Visitor as Visitor browser
    participant Edge as Cloudflare edge
    participant Connector as cloudflared
    participant App as Django
    participant Data as SQLite volume
    Connector->>Edge: Establish outbound tunnel
    Visitor->>Edge: Open LakshyaX over HTTPS
    Edge->>Connector: Forward request over established tunnel
    Connector->>App: Forward on private Docker network
    App->>Data: Read or write when the request needs data
    Data-->>App: Return result
    App-->>Connector: Return response
    Connector-->>Edge: Return through tunnel
    Edge-->>Visitor: Return HTTPS response
```

The connector, app, and storage depend on one host. If that machine or its internet connection goes offline, the app becomes unavailable. The data volume persists across container replacements on that host.

[Cloudflare Tunnel fundamentals](https://developers.cloudflare.com/tunnel/concepts/) · [Back to LakshyaX](../README.md)
