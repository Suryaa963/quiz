import { Component, HostListener, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiserviceService } from '../apiservice.service';
import { interval, take } from 'rxjs';
import { AuthService } from '../auth.service';

let response: any[] = [];
let resultArr: any[] = [];

@Component({
  selector: 'app-quiz',
  templateUrl: './quiz.component.html',
  styleUrls: ['./quiz.component.css']
})


export class QuizComponent implements OnInit {
  quizId: any;
  questions : any =[];
  currentQuestionIndex = 0;
  responses: any[] = [];
  timer: number = 15 * 60; // 15 minutes in seconds
  currentTime: Date  = new Date(0,0,0,0,10,0);
  timerSubscription: any;
  warningCount: number = 0;
  totalQuestion=0;
  
  userSelectedOption = -1;
  userSelectedQuestion = -1;
  
  uniquebyid = new Map();
  quizSubmission: any;
  testSubmitted  = false;

  constructor(
    private route: ActivatedRoute,
    private quizService: ApiserviceService,
    private router: Router,
    private auth: AuthService
  ) { }

  ngOnInit() {
    this.quizId = this.route.snapshot.paramMap.get('id');
    console.log('this.quizid', this.quizId);

    this.quizService.getQuestionsForSection(this.quizId).subscribe((resp: any)=>{
      console.log('resppp',resp);
       this.questions = resp.result;
       this.totalQuestion = this.questions.length;
    });
    this.startTimer();
  }

  startTimer(){
    console.log('timer...')
    this.timerSubscription = interval(1000).
    pipe(
      take(this.timer)
    ).subscribe({
      next: ()=>{
        this.timer-=1;
        this.currentTime = new Date(this.currentTime.getTime()-1000)
        console.log('timer', this.timer);
      },
      complete:()=>{
        console.log('compleetd...');
        this.submitTest();
      }
    })
  }
  selectValue(option: any,questionid: any){
    console.log('selected val',+option.target.value,questionid);
    this.userSelectedOption = option.target.value;
    this.userSelectedQuestion = questionid;
    this.createAnswerResponses({
      "question_id": +this.userSelectedQuestion,
      "selected_option_id": +this.userSelectedOption
    })
  }
  

  goToNext(){
    if(this.currentQuestionIndex< this.questions.length){
      this.currentQuestionIndex+=1;
      console.log('quesi', this.questions[this.currentQuestionIndex])
    }
    
    // push records
  }
  goToPrevious(){
    if(this.currentQuestionIndex>0){
      this.currentQuestionIndex-=1;
    }

  }

  @HostListener('document:keydown', ['$event'])
  handleKeyboardEvent(event: KeyboardEvent) {
    // Disable Ctrl+C, Ctrl+V, and F12 (if needed)
    if(this.testSubmitted){
      return;
    }
    if ((event.ctrlKey && (event.key === 'c' || event.key === 'v')) || event.key === 'F12') {
      this.handleCheatAttempt();
      event.preventDefault();
    }
  }

  @HostListener('window:blur', ['$event'])
  onWindowBlur(event: FocusEvent) {
    // When the user switches tabs or windows
    if(this.testSubmitted){
      return;
    }
    this.handleCheatAttempt();
  }

  async handleCheatAttempt() {
    this.warningCount++;
    if (this.warningCount === 1) {
      alert('Warning: Cheating attempt detected. Further attempts will auto-submit the quiz.');
    } else if (this.warningCount >= 2) {
      alert('Cheating attempt exceeded. Auto-submitting the quiz.');
      await this.submitTest();
      return;
    }
  }




createAnswerResponses(userobj: any){
  console.log('resppp', response);
   response.push(userobj);
   response.forEach(resp =>{
    this.uniquebyid.set(resp.question_id, resp);
   })
   console.log('uniq', this.uniquebyid)
   resultArr = Array.from(this.uniquebyid.values())

}

async submitTest(){
  this.timerSubscription.unsubscribe();
  // post api call
  const payload = {
    "userdetail_id":this.auth.currentUser.user.id,
    "quiz_id": this.quizId,
    "response": resultArr
  }
  this.quizService.submitQuiz(payload).subscribe(async resp =>{
    console.log('resp',resp);
    this.quizSubmission = await resp
  })
  this.testSubmitted = true
  return;
}

  


  
}

// {
//   "userdetail_id": 1,
//   "quiz_id": 1,
//   "response": [
//    {  "question_id": 1, "selected_option_id": 3 }
//  ]
// }