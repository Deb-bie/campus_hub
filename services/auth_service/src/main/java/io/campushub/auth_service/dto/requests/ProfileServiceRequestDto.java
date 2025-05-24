package io.campushub.auth_service.dto.requests;

import lombok.*;

import java.util.UUID;

@Data
@NoArgsConstructor
@RequiredArgsConstructor
@AllArgsConstructor
@Builder
public class ProfileServiceRequestDto {
    private UUID userId;
    private String firstName;
    private String lastName;
    private String email;
}