import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  constructor(private authService: AuthService, private router: Router) { }
  message='';
  error= '';
  username = '';
  password = '';
  email = '';
  ngOnInit(): void {
  }
  onSignup() {
    let payload = {
      "username": this.username,
      "email": this.email,
      "password": this.password
    }
    this.authService.signup(payload).subscribe({
      next: (res) => {
        this.message = 'Signup successful! Please log in.';
        setTimeout(() => this.router.navigate(['/login']), 2000);
      },
      error: () => this.error = 'Signup failed. Please try again.'
    });
  }

}
