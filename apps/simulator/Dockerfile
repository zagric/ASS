FROM golang:1.25-alpine

WORKDIR /app

RUN go install github.com/go-delve/delve/cmd/dlv@latest
RUN go install github.com/air-verse/air@latest

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o main ./cmd/simulator

# EXPOSE 50205

ENTRYPOINT ["air"]