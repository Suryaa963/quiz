import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http'
@Injectable({
  providedIn: 'root'
})
export class ApiserviceService {

  constructor(private http: HttpClient) { }
  url = 'http://127.0.0.1:5000'

  getAllQuizTitle(){
    return this.http.get(`${this.url}/user/quiz/`,{withCredentials: true});
  }

  getQuestionsForSection(quizid: any){
    return this.http.get(`${this.url}/user/quiz/${quizid}`,{withCredentials: true});
  }
  submitQuiz(quiz: any){
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });

    return this.http.post(`${this.url}/user/quiz/`,quiz,{headers})
  }
  getQuizUserAttemptStatus(quizid: any,userid: any){
    return this.http.get(`${this.url}/user/quiz/${quizid}/${userid}/status`,{withCredentials: true});
  }
}
