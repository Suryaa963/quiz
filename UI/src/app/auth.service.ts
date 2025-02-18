import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://127.0.0.1:5000';
  score: any;
  currentUser: any = null;
  constructor(private http: HttpClient) { 
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      this.currentUser = JSON.parse(storedUser);
    }
  }

  setScore(score: any){
    this.score = score;
  }
  getScore(){
    return this.score;
  }
  signup(data: any) {
    return this.http.post(`${this.apiUrl}/users/signup`, data, {withCredentials: true});
    
  }

  login(data: any){
    return this.http.post(`${this.apiUrl}/users/login`,data, {withCredentials: true}).pipe(
      tap(user => {
        localStorage.setItem('user', JSON.stringify(user));
        this.currentUser = user;
      })
    );
  }

  // Logout: clear stored user information
  logout() {
    localStorage.removeItem('user');
    this.currentUser = null;
  }

  getToken() {
    return this.currentUser ? this.currentUser.token : null;
  }

}
