import { Component, OnInit } from '@angular/core';
import { ApiserviceService } from '../apiservice.service';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-leaderboard',
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.css']
})
export class LeaderboardComponent implements OnInit {

  constructor(private auth: AuthService) { 
   
  }
   historyScore = history.state.score
   score: any;
  ngOnInit(): void {
    this.score = localStorage.getItem('score');
    // if(this.historyScore){
    //   this.auth.setScore(history.state.score);
    // }
    // this.score = this.auth.getScore()
  }
  

  
}
