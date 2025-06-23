package io.campushub.auth_service.kafka;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.Map;

@Service
public class LogProducer {
    @Autowired
    private KafkaTemplate<String, LogItem> kafkaTemplate;

    public void emitAuthUserSignUpLog(String userId, String email) {
        LogItem logItem = buildLog(
                "INFO",
                "New user signed up",
                Map.of(
                        "userId", userId,
                        "email", email)
        );

        kafkaTemplate.send("auth_user_signup", logItem);
    }

    public void emitAuthUserSignInLog(String userId, String email) {
        LogItem logItem = buildLog(
                "INFO",
                "User signed in",
                Map.of(
                        "userId", userId,
                        "email", email)
        );

        kafkaTemplate.send("auth_user_signin", logItem);
    }

    public void emitAuthUserUpdateLog(String userId, String email) {
        LogItem logItem = buildLog(
                "INFO",
                "Auth User updated",
                Map.of(
                        "userId", userId,
                        "email", email)
        );

        kafkaTemplate.send("auth_user_updated", logItem);
    }


    private LogItem buildLog(String level, String message, Map<String, Object> metadata) {
        return LogItem.builder()
                .timestamp(Instant.now().toString())
                .service_name("auth_service")
                .log_level(level)
                .message(message)
                .metadata(metadata)
                .environment("development")
                .build();
    }
}
