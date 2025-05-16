import { Component, OnInit} from '@angular/core';
import { Task } from '../../../core/models/task.model';
import { TaskService } from '../../../core/services/task.service';

@Component({
  selector: 'app-task-list',
  standalone: true,
  imports: [],
  templateUrl: './task-list.component.html',
  styleUrl: './task-list.component.css'
})
export class TaskListComponent implements OnInit {
  tasks: Task[] = [];
  loading = false;
  filter: string | undefined;

  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
    this.loadTasks();
  }

  loadTasks(status?: string): void {
    this.loading = true;
    this.filter = status;

    this.taskService.getTasks(status ?? '')
      .subscribe({
        next: (tasks) => {
        this.tasks = tasks;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  completeTask(task: Task): void {
    this.taskService.updateTask(task.id!, { status: 'completed' })
      .subscribe({
        next: (updatedTask) => {
          const index = this.tasks.findIndex(t => t.id === updatedTask.id);
          if (index !== -1) {
            this.tasks[index] = updatedTask;
          }
        }
      });
  }

  reopenTask(task: Task): void {
    this.taskService.updateTask(task.id!, { status: 'pending' })
      .subscribe({
        next: (updatedTask) => {
          const index = this.tasks.findIndex(t => t.id === updatedTask.id);
          if (index !== -1) {
            this.tasks[index] = updatedTask;
          }
        }
      });
  }

  deleteTask(taskId: number): void {
    if (confirm('Estas seguro de que quieres eliminar esta tarea?')) {
      this.taskService.deleteTask(taskId)
        .subscribe({
          next: () => {
            this.tasks = this.tasks.filter(task => task.id !== taskId);
          },
          error: (error) => {
            console.error('Error deleting task:', error);
          }
        });
    }
  }

}
