package org.iekn.auth.controller;

import org.iekn.auth.entity.User;
import org.iekn.auth.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserRepository userRepository;

    @PostMapping("/login")
    public String login(@RequestBody User user) {
        try {
            User existingUser = userRepository.findByUsername(user.getUsername());
            if (existingUser != null && existingUser.getPassword().equals(user.getPassword())) {
                return "Login successful";
            } else {
                return "Invalid credentials";
            }
        } catch (Exception e) {
            return "Invalid credentials";
        }
    }

    @PostMapping("/signup")
    public String signup(@RequestBody User user) {
        try {
            user.setPassword(user.getPassword());
            userRepository.save(user);
            return "User registered successfully";
        } catch (Exception e) {
            return "User registration failed";
        }
    }

}