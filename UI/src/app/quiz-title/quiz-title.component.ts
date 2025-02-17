import { Component, OnInit } from '@angular/core';
import { ApiserviceService } from '../apiservice.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-quiz-title',
  templateUrl: './quiz-title.component.html',
  styleUrls: ['./quiz-title.component.css']
})
export class QuizTitleComponent implements OnInit {

  constructor(public apiservice: ApiserviceService, private router:Router) { }

  quizSections =[]
  questions = [];
  ngOnInit() {
   this.apiservice.getAllQuizTitle().subscribe((resp: any) =>{
    console.log('resp',resp);
    this.quizSections = resp.result
   })
  }
  navigateSection(quiz: any){
    this.router.navigate(['/quiz',quiz.id])
  }

}
