import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent{

  email = '';
  password = '';
  error: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  onLogin() {
    let payload=  {
      "email": this.email,
      "password": this.password
    }
    this.authService.login(payload).subscribe({
      next: () => this.router.navigate(['/quiz']),
      error: () => this.error = 'Login failed. Please try again.'
    });
  }

}
