package io.campushub.auth_service.kafka;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LogItem {
    private String timestamp;
    private String service_name;
    private String log_level;
    private String message;
    private Map<String, Object> metadata;
    private String request_id;
    private String trace_id;
    private String environment;
}
