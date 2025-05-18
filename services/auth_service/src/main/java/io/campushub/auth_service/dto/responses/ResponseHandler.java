package io.campushub.auth_service.dto.responses;

import lombok.Builder;
import lombok.Data;
import org.springframework.http.HttpStatus;

@Data
@Builder
public class ResponseHandler<T> {
    private Integer statusCode;
    private HttpStatus status;
    private T message;
}
