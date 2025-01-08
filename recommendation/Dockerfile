FROM golang:1.23 AS build
WORKDIR /build
COPY . .
ENV GOCACHE=/root/.cache/go-build
ENV GOMODCACHE=/go/pkg/mod/
RUN --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=cache,target=/go/pkg/mod/ \
    CGO_ENABLED=0 GOOS=linux go build -o app

FROM scratch
WORKDIR /app
COPY --from=build /build/app /build/config.json ./
COPY --from=build /build/static ./static
COPY --from=build /build/templates ./templates
ENTRYPOINT ["./app"]
EXPOSE 8080