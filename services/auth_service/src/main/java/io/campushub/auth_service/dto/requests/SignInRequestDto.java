package io.campushub.auth_service.dto.requests;


import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class SignInRequestDto {
    private String email;
    private String password;
}
