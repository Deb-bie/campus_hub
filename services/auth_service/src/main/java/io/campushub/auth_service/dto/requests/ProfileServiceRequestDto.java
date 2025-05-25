package io.campushub.auth_service.dto.requests;

import lombok.*;

import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProfileServiceRequestDto {
    private UUID user_id;
    private String first_name;
    private String last_name;
    private String email;
}