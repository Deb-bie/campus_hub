package io.campushub.auth_service.dto.responses;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class SignInResponseDto {
    private String userId;
    private String email;
    private String firstName;
    private String lastName;
    private String token;
}
