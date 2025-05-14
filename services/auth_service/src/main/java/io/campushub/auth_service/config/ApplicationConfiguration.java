package io.campushub.auth_service.config;

import io.campushub.auth_service.exceptions.NotFoundException;
import io.campushub.auth_service.repository.AuthRepository;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@Configuration
public class ApplicationConfiguration {
    private final AuthRepository authRepository;

    public ApplicationConfiguration (AuthRepository authRepository) {
        this.authRepository = authRepository;
    }

    @Bean
    UserDetailsService userDetailsService (){
        return username -> {
            try {
                return authRepository
                        .findByEmail(username)
                        .orElseThrow(
                                () -> new NotFoundException("User not found")
                        );
            } catch (NotFoundException e) {
                throw new RuntimeException(e);
            }
        };
    }

    @Bean
    BCryptPasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration configuration) throws Exception {
        return configuration.getAuthenticationManager();
    }

    @Bean
    AuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider daoAuthenticationProvider = new DaoAuthenticationProvider();
        daoAuthenticationProvider.setUserDetailsService(userDetailsService());
        daoAuthenticationProvider.setPasswordEncoder(passwordEncoder());

        return daoAuthenticationProvider;
    }

}
