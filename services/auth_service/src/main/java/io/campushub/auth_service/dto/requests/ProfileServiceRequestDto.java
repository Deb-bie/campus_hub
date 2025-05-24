package io.campushub.auth_service.dto.requests;

import lombok.*;

import java.util.UUID;

@Data
@Builder
@AllArgsConstructor
@RequiredArgsConstructor
@NoArgsConstructor
public class ProfileServiceRequestDto {
    private UUID userId;
    private String firstName;
    private String lastName;
    private String email;
}