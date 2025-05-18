package io.campushub.auth_service.dto.requests;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class SignUpRequestDto {
    private String firstName;
    private String lastName;
    private String email;
    private String password;
}
