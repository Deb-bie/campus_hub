package io.campushub.auth_service;

import org.junit.jupiter.api.Test;
import org.springframework.boot.autoconfigure.ImportAutoConfiguration;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
@ImportAutoConfiguration(exclude = {DataSourceAutoConfiguration.class})
class AuthServiceApplicationTests {

	@Test
	void contextLoads() {
	}

}
