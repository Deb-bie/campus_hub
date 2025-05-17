# ---- Stage 1: Build the app ----
FROM gradle:8.5.0-jdk21 AS builder
WORKDIR /app
COPY . .
RUN ./gradlew clean build -x test --no-daemon

# ---- Stage 2: Create the runtime image ----
FROM openjdk:21-jdk
WORKDIR /app

# Copy the built jar from the builder stage
COPY --from=builder /app/build/libs/*.jar app.jar
EXPOSE 8081
ENTRYPOINT ["java", "-Dspring.profiles.active=docker", "-jar", "app.jar"]