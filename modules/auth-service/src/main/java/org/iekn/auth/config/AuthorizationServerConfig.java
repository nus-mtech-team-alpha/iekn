package org.iekn.auth.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.oauth2.core.AuthorizationGrantType;
import org.springframework.security.oauth2.server.authorization.client.InMemoryRegisteredClientRepository;
import org.springframework.security.oauth2.server.authorization.client.RegisteredClient;
import org.springframework.security.oauth2.server.authorization.client.RegisteredClientRepository;
import org.springframework.security.oauth2.server.authorization.settings.ClientSettings;
import org.springframework.security.oauth2.server.authorization.settings.TokenSettings;

import java.util.UUID;

@Configuration
@EnableWebSecurity
public class AuthorizationServerConfig {

//    @Bean
//    public RegisteredClientRepository registeredClientRepository() {
//        RegisteredClient registeredClient = RegisteredClient.withId(UUID.randomUUID().toString())
//                .clientId("your-client-id")
//                .clientSecret(new BCryptPasswordEncoder().encode("your-client-secret"))
//                .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
//                .authorizationGrantType(AuthorizationGrantType.REFRESH_TOKEN)
//                .redirectUri("http://localhost:8080/login/oauth2/code/my-client")
//                .scope("read")
//                .scope("write")
//                .clientSettings(ClientSettings.builder().requireAuthorizationConsent(true).build())
//                .tokenSettings(TokenSettings.builder().build())
//                .build();
//
//        return new InMemoryRegisteredClientRepository(registeredClient);
//    }

}
