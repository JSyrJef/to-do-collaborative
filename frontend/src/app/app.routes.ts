import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login.component';
import { TaskFormComponent } from './features/tasks/task-form/task-form.component';
import { TaskListComponent } from './features/tasks/task-list/task-list.component';
import { AuthGuard } from './core/guards/auth.guard';
import { RegisterComponent } from './features/auth/register/register.component';
import { HomeComponent } from './features/home/home.component';
import { TaskDetailComponent } from './features/tasks/task-detail/task-detail.component';

export const routes: Routes = [
    {path: '', component: HomeComponent},
    {path: 'login', component: LoginComponent},
    {path: 'register', component: RegisterComponent},
    {path: 'tasks', component: TaskListComponent, canActivate: [AuthGuard]},
    {path: 'tasks/new', component: TaskFormComponent, canActivate: [AuthGuard]},
    {path: 'tasks/:id/edit', component: TaskFormComponent, canActivate: [AuthGuard]},
    {path: 'tasks/:id', component: TaskDetailComponent, canActivate: [AuthGuard]},
];
