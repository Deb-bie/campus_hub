package io.campushub.auth_service.config;

import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

@Component
public class WebClientFactory {

    public WebClient createClient(String baseUrl) {
        return WebClient
                .builder()
                .baseUrl(baseUrl)
                .build();
    }
}
