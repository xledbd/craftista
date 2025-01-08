FROM maven:3.9-amazoncorretto-23-alpine AS build
WORKDIR /app
COPY . .
RUN --mount=type=cache,target=/root/.m2 \
    mvn clean package -DskipTests

FROM amazoncorretto:23-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar ./app.jar
ENTRYPOINT ["java"]
CMD ["-jar", "app.jar"]
EXPOSE 8080