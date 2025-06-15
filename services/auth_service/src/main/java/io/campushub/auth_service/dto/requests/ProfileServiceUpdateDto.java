package io.campushub.auth_service.dto.requests;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProfileServiceUpdateDto {
    private String first_name;
    private String last_name;
    private String email;
}
