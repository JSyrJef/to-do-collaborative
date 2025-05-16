import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Task } from '../models/task.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  constructor(private http: HttpClient) {}

  getTasks(status: string): Observable<Task[]> {
    let url = `${environment.apiUrl}/tasks/`;
    if (status) {
      url += `?status=${status}`;
    }
    return this.http.get<Task[]>(url);
  }

  getTask(id: number): Observable<Task> {
    return this.http.get<Task>(`${environment.apiUrl}/tasks/${id}/`);
  }

  createTask(task: Task): Observable<Task> {
    return this.http.post<Task>(`${environment.apiUrl}/tasks/`, task);
  }

  updateTask(id: number, task: Partial<Task>): Observable<Task> {
    return this.http.patch<Task>(`${environment.apiUrl}/tasks/${id}/`, task);
  }

  deleteTask(id: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/tasks/${id}/`);
  }

  addCollaborator(taskId: number, username: string): Observable<any> {
    return this.http.post<any>(`${environment.apiUrl}/tasks/${taskId}/add_collaborator/`, { username });
  }

  removeCollaborator(taskId: number, username: string): Observable<any> {
    return this.http.post<any>(`${environment.apiUrl}/tasks/${taskId}/remove_collaborator/`, {username});
  }
}
