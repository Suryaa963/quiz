import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { QuizTitleComponent } from './quiz-title/quiz-title.component';
import { QuizComponent } from './quiz/quiz.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { AuthGuard } from './auth.guard';

const routes: Routes = [
  { path: '', redirectTo:'login',pathMatch:"full" },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'quiz', component: QuizTitleComponent,canActivate: [AuthGuard] },
 
  { path: 'quiz/:id', component: QuizComponent,canActivate: [AuthGuard] },
  { path: 'leaderboard', component: LeaderboardComponent,canActivate: [AuthGuard] }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
