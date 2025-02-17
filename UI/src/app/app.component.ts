import { Component, OnInit } from '@angular/core';
import { ApiserviceService } from './apiservice.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  constructor(public apiservice: ApiserviceService){}
  quizSections =[]
  questions = [];
  ngOnInit() {
  //  this.apiservice.getAllQuizTitle().subscribe((resp: any) =>{
  //   console.log('resp',resp);
  //   this.quizSections = resp.result
  //  })
  }
  title = 'UI';

  // navigateSection(section: any){
  //   this.apiservice.getQuestionsForSection(section.id).subscribe((resp: any)=>{
  //     console.log('resppp',resp);
  //     this.questions = resp.result
  //   })
  // }
}
