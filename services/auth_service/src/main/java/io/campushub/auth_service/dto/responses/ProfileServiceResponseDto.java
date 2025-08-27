package io.campushub.auth_service.dto.responses;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProfileServiceResponseDto {
        private String user_id;
        private String first_name;
        private String last_name;
        private String email;
}
